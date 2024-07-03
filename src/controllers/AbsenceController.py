from app import app, current_user, render_template, login_required,session,request,redirect,paginate
from ..models.Etudiant import Etudiant
from ..models.Inscription import Inscription
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Cours import Cours
from ..models.Seance import Seance
from ..models.Etudiant import Etudiant
from ..models.Absence import Absence
from ..models.Semestre import Semestre

@app.route('/absence')
@login_required
def absence_list():
    semestre = None
    etudiant = None
    anneeEncours = AnneeScolaire.query.filter_by(id=session.get("anneeEncours")['id']).first()
    if 'semestreSelected' in session :
        semestre = Semestre.query.filter_by(id=session.get('semestreSelected')).first()
    

    if  current_user.role.libelle == 'ROLE_ETUDIANT':
        etudiant = Etudiant.query.filter_by(id=current_user.id).first()
        inscription = Inscription.query.filter_by(etudiant=etudiant, anneeScolaire=anneeEncours).first()
        semestres = inscription.classe.niveau.semestres
    else:
        semestres = Semestre.query.all()
        if "etudiantSelected" in session :
            etudiant = Etudiant.query.filter_by(id=session.get('etudiantSelected')).first()
        
    selected = {
        'anneeScolaire' : anneeEncours,
        'etudiant' : etudiant,
        'semestre' : semestre,
    }

    query = Absence.query.filter_by(isArchived=False).join(Seance).join(Cours).filter_by(anneeScolaire=anneeEncours)
    if selected.get("semestre") != None:
        query = query.join(Semestre, Semestre.id==Cours.semestre_id).filter_by(id=selected.get('semestre').id)

    if selected.get("etudiant") != None:
        query = query.join(Etudiant, Etudiant.id==Absence.etudiant_id).filter_by(id=selected.get('etudiant').id)

    etudiants = Etudiant.query.filter_by(isArchived=False).all()
    results = paginate(query)
    absences = results.get('data')
    pagination = results.get('pagination')

    return render_template("models/absence/index.html", connectedUser=current_user,absences=absences,pagination=pagination,
                           selectedValue=selected,etudiants=etudiants,semestres=semestres,anneeEncours=anneeEncours)



@app.route('/absence/filtre/semestre/<int:id>')
@login_required
def showAbsenceBySemestre(id):
    if id != 0 :
        session["semestreSelected"] = id
    else :
        session.pop("semestreSelected",None)

    return redirect("/absence")


@app.route('/absence/filtre/etudiant/<int:id>')
@login_required
def showAbsenceByEtudiant(id):
    if id != 0 :
        session["etudiantSelected"]=id
    else :
        session.pop("etudiantSelected",None)
    
    return redirect("/absence")