from app import app, current_user, render_template, login_required,session, request, redirect,paginate, flash, db
from ..models.Etudiant import Etudiant
from ..models.Semestre import Semestre
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..models.Cours import Cours
from ..models.Niveau import Niveau
from ..models.Module import Module
from ..models.Professeur import Professeur
from ..models.Etudiant import Etudiant
from ..models.Enseignement import Enseignement
from ..models.Seance import Seance
from ..form.CoursForm import CoursForm
from datetime import datetime
from ..helpers.List_tojson import listToJson


@app.route('/cours')
@login_required
def cours_list():
    session["path_to_go"] ="/cours" #for annee change

    #*------------------- For save
    session.pop('semestreChosen', None)
    session.pop('moduleChosen', None)
    session.pop('profChosen', None)
    #*------------Vider session après save seance ou en cas de non save
    session.pop("coursID", None)
    session.pop("dateChosen", None)
    session.pop("heureDChosen", None)
    session.pop("heureFChosen", None)
    session.pop("isProf", None)
    session.pop("profChosen", None)
    session.pop('lieu', None)
    session.pop('salleChosen', None)
    session.pop('codeChosen', None)
    #*----------------------------------------

    classe = None
    niveau = None
    semestre = None
    anneeScolaire = AnneeScolaire.query.filter_by(id=session.get("anneeEncours")['id']).first()

    query = Cours.query.filter_by(isArchived=False,anneeScolaire=anneeScolaire)

    if 'classeSelected' in session:
        ids = session.get('classeSelected')
        classe = list(map(int, ids.split(','))) # Une liste d'id 
        for id in classe :
            cl = Classe.query.filter_by(id=id).first()
            query = query.filter(Cours.classes.contains(cl))
    
    if 'semestreSelected' in session:
        semestre = Semestre.query.filter_by(id=session.get('semestreSelected')).first()
        query = query.filter_by(semestre=semestre)

    if 'niveauSelected' in session :
        niveau = Niveau.query.filter_by(id=session.get('niveauSelected')).first()
        query = query.join(Semestre, Cours.semestre_id==Semestre.id).join(Niveau,Semestre.niveau_id==Niveau.id).filter_by(id=niveau.id)
    

    selected = {
        'anneeScolaire' : anneeScolaire ,
        'classe' : classe,
        'niveau' : niveau,
        'semestre' : semestre,
    }
    
    results = paginate(query)
    cours = results.get('data')
    pagination = results.get('pagination')

    classes = Classe.query.filter_by(isArchived=False).all()
    niveaux = Niveau.query.all()
    semestres = Semestre.query.all()
    return render_template("models/cours/index.html",cours=cours, pagination=pagination,selectedValue=selected,
                           classes=classes, niveaux=niveaux,semestres=semestres)
   


@app.route('/cours/filtre/classe/<string:id>')
@login_required
def showCoursByClasse(id):
    if len(id)!=0 and id != '0':
        session["classeSelected"] = id
    else :
        session.pop("classeSelected",None)
    return redirect("/cours")
    

@app.route('/cours/filtre/niveau/<int:id>')
@login_required
def showCoursByNiveau(id):
    if id != 0 :
        session["niveauSelected"] = id
    else :
        session.pop("niveauSelected",None)
    return redirect("/cours")



@app.route('/cours/filtre/semestre/<int:id>')
@login_required
def showCoursBySemestre(id):
    if id != 0 :
        session["semestreSelected"] = id
    else :
        session.pop("semestreSelected",None)
    return redirect("/cours")





@app.route('/cours/save', methods=['GET','POST'])
@app.route('/cours/save/<int:id>', methods=['GET','POST'])
@login_required
def saveCours(id=None):
    from wtforms.validators import DataRequired
    form = CoursForm()
    semestresList = Semestre.query.all()
    semestres = [("0","")]
    semestres.extend([(str(semestre.id),semestre.libelle) for semestre in semestresList])
    modules = [("0","")]
    modules.extend([(str(module.id),module.libelle) for module in Module.query.filter_by(isArchived=False).all()])
    

    form.semestre.coerce = int
    form.semestre.choices = semestres
    form.module.coerce = int
    form.module.choices = modules
    form.professeur.choices = []
    form.classes.choices = []
    form.module.render_kw["disabled"] = True
    form.submit.render_kw["disabled"] = True
    form.professeur.render_kw["disabled"] = True
    form.classes.render_kw["disabled"] = True

    error=None
    isArchived=False
    cours = Cours()

    anneeScolaire = AnneeScolaire.query.filter_by(isActive=True).first()
    enseignements = listToJson(Enseignement.query.filter_by(anneeScolaire=anneeScolaire).all())
    professeurs = listToJson(Professeur.query.filter_by(isArchived=False).all())
    classes = listToJson(Classe.query.filter_by(isArchived=False).all())
    semestresArray = listToJson(semestresList)
    courss = listToJson(Cours.query.filter_by(anneeScolaire=anneeScolaire,isArchived=False).all())
    
    # if id !=None :
    #     cours:Cours = Cours.query.filter_by(id=id).first()
    #     form.module.data = cours.module_id
    #     form.semestre.data = cours.semestre_id
    #     form.professeur.data = cours.professeur_id
    #     form.nbreHeureTotal.data = cours.nbreHeureTotal
    #     isArchived = True
    
    if form.is_submitted():

        cours.anneeScolaire = anneeScolaire
        cours.isArchived = form.isArchived.data
        cours.createAt = datetime.now().date()
        cours.module = Module.query.filter_by(id=form.module.data).first()
        cours.professeur = Professeur.query.filter_by(id=form.professeur.data).first()
        cours.semestre = Semestre.query.filter_by(id=form.semestre.data).first()
        cours.nbreHeureTotal = form.nbreHeureTotal.data
        cours.nbreHeurePlanifie = 0
        cours.nbreHeureRestantPlan = 0
        cours.nbreHeureRealise = 0
        for id in form.classes.raw_data :
            classe = Classe.query.filter_by(id=int(id)).first()
            cours.classes.append(classe)
        
        try :

            db.session.add(cours)
            db.session.commit()

            form.nbreHeureTotal.data = ""
            flash("Le cours a été enregistrée avec succès.", 'success')
        except:
            error = "Erreur d'enregistrement de l'incription"
            db.session.rollback()
    else :
        app.logger.debug(form.errors)

    return render_template("models/cours/form.html",form=form, error=error, isArchived=isArchived, cours=courss, 
                           enseignements=enseignements, classes=classes, professeurs=professeurs,semestres=semestresArray)

