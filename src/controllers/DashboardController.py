from app import app, current_user, render_template, login_required,session, request
from ..models.Etudiant import Etudiant
from ..models.Inscription import Inscription
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..models.Cours import Cours
from ..models.Declaration import Declaration
from ..models.Module import Module
from ..models.Professeur import Professeur
from ..models.Etudiant import Etudiant
from ..models.Absence import Absence
from ..models.Seance import Seance
from ..models.Enseignement import Enseignement


@app.route('/home')
@login_required
def home():
    # session["path"]=request.path.split('/')[1]
    # app.logger.debug()
    anneeActuelle = AnneeScolaire.query.filter_by(isActive=True).first()
    
    from datetime import timedelta
    import datetime
    # Obtenir la date d'aujourd'hui
    aujourdhui = datetime.date.today()
    # Calculer le lundi de cette semaine
    lundi = aujourdhui - timedelta(days=aujourdhui.weekday())
    # Calculer le samedi de cette semaine
    samedi = lundi + timedelta(days=5)  # Ajoute 5 jours à partir du lundi pour arriver au samedi
    
    if current_user.role.libelle in ["ROLE_ADMIN","ROLE_RP","ROLE_AC"] :
        nbreInscription = Inscription.query.filter_by(anneeScolaire=anneeActuelle,isArchived=False).count()
        nbreClasse = Classe.query.filter_by(isArchived=False).count()
        nbreModule = Module.query.filter_by(isArchived=False).count()
        nbreProfesseur = Professeur.query.filter_by(isArchived=False).count()
        donnees = getFiveBestAbsents(anneeActuelle)
        return render_template("home/indexAdmin.html", admin=current_user, nbreInscription=nbreInscription,donnees=donnees,
                                 nbreClasse=nbreClasse, nbreModule=nbreModule, nbreProfesseur=nbreProfesseur)
    
    if current_user.role.libelle == "ROLE_PROFESSEUR" :
        professeur = Professeur.query.filter_by(id=current_user.id).first()
        nbreClasse = Classe.query.filter_by(isArchived=False).join(Enseignement).filter_by(anneeScolaire=anneeActuelle).join(Professeur).filter_by(id=professeur.id).count()
        modules = Module.query.filter_by(isArchived=False).join(Enseignement,Module.enseignements).filter_by(anneeScolaire=anneeActuelle).join(Professeur).filter_by(id=professeur.id).all()
        nbreModule = len(modules)
        seancesP = Seance.query.filter_by(isArchived=False,professeur=None).join(Cours).filter(Cours.professeur==professeur,Seance.date.between(lundi, samedi)).filter_by(anneeScolaire=anneeActuelle).all()
        seancesO = Seance.query.filter_by(isArchived=False,professeur=professeur).filter(Seance.date.between(lundi, samedi)).join(Cours).filter_by(anneeScolaire=anneeActuelle).all()
        print(seancesP)
        print(seancesO)
        nbreCours = len(seancesO)+len(seancesP)
        nbreDeclaration = Declaration.query.filter_by(user=professeur).join(Seance).join(Cours).filter_by(anneeScolaire=anneeActuelle).count()
        classes = Classe.query.filter_by(isArchived=False).join(Enseignement).filter_by(anneeScolaire=anneeActuelle).join(Professeur).filter_by(id=professeur.id).all()
        return render_template("home/indexProfesseur.html",professeur=professeur, nbreClasse=nbreClasse, classes=classes, 
                               nbreModule=nbreModule, nbreCours=nbreCours, nbreDeclaration=nbreDeclaration )
    
    if current_user.role.libelle == "ROLE_ETUDIANT" :
        etudiant = Etudiant.query.filter_by(id=current_user.id).first()
        inscription = Inscription.query.filter_by(etudiant=etudiant, anneeScolaire=anneeActuelle).first() # Inscription en cours
        nbreCours = Seance.query.filter_by(isArchived=False).join(Cours).filter(Cours.classes.contains(inscription.classe),Seance.date.between(lundi, samedi)).filter_by(anneeScolaire=anneeActuelle).count()        
        nbreAbsence = Absence.query.filter_by(isArchived=False, etudiant=etudiant).join(Seance).join(Cours).filter_by(anneeScolaire=anneeActuelle).count()
        nbreDeclaration = Declaration.query.filter_by(user=etudiant).join(Seance).join(Cours).filter_by(anneeScolaire=anneeActuelle).count()
        return render_template("home/indexEtudiant.html",etudiant=etudiant,nbreCours=nbreCours,
                               nbreAbsence=nbreAbsence,nbreDeclaration=nbreDeclaration,inscription=inscription  )
    

def getFiveBestAbsents(anneeActuelle):
    donnees = {}
    etudiants = Etudiant.query.filter_by(isArchived=False).join(Absence.etudiant).join(Seance).join(Cours).filter_by(anneeScolaire=anneeActuelle).all()
    for etu in etudiants :
        nbreAbsence = Absence.query.filter_by(isArchived=False, etudiant=etu).join(Seance).join(Cours).filter_by(anneeScolaire=anneeActuelle).count()
        donnees[str(etu.id)]=nbreAbsence 
    
    donnees_triees = dict(sorted(donnees.items(), key=lambda item: item[1], reverse=True)) 
    data = []
    i = 0
    for key, value in donnees_triees.items() :
        if i==5 :
            break
        etudiant = Etudiant.query.filter_by(id=int(key)).first() 
        inscription = Inscription.query.filter_by(etudiant=etudiant, anneeScolaire=anneeActuelle).first()
        data.append({
            'id': etudiant.id,
            'matricule': etudiant.matricule,
            'nomComplet': etudiant.nomComplet,
            'email':etudiant.login,
            'classe':inscription.classe.libelle,
            'nbreAbsence':value
        })
        i=i+1
    return data

