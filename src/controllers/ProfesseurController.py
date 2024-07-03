from app import app,bcrypt, current_user, render_template, login_required,session, request,url_for,paginate,redirect,db, flash
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..models.Module import Module
from ..models.Professeur import Professeur
from ..models.Enseignement import Enseignement
from ..form.ProfesseurForm import ProfesseurForm
from ..form.AffectationForm import AffectationForm


@app.route('/professeur')
@login_required
def professeur_list():
    htmlValueClasse = session.pop('htmlClasse',None)
    htmlValueModule = session.pop('htmlModule',None)
    module = None
    classe = None
    grade = None
    
    query = Professeur.query.filter_by(isArchived=False)

    if 'moduleSelected' in session :
        module= Module.query.filter_by(id=session.get('moduleSelected')).first()
        query = query.join(Enseignement).filter(Enseignement.modules.contains(module))
    
    if 'classeSelected' in session :
        classe= Classe.query.filter_by(id=session.get('classeSelected')).first()
        query = query.join(Enseignement).filter_by(classe=classe)
    
    if 'gradeSelected' in session :
        grade= session.get('gradeSelected')
        query = query.filter(Professeur.grade==grade)
    
    
    selected={
        'classe' : classe,
        'module' : module,
        'grade' : grade,
    }

    classes = Classe.query.filter_by(isArchived=False).all()
    modules = Module.query.filter_by(isArchived=False).all()
    results = paginate(query)
    professeurs = results.get('data')
    # Récupérer uniquement les valeurs distinctes de l'attribut 'grade' des professeurs
    grades = [grade[0] for grade in db.session.query(Professeur.grade).distinct()]
    pagination = results.get('pagination')
    
    return render_template('models/professeur/index.html', professeurs=professeurs, pagination=pagination,
                           selectedValue=selected, grades=grades, classes=classes, modules=modules,
                           htmlValueClasse=htmlValueClasse, htmlValueModule=htmlValueModule)


@app.route('/professeur/filtre/classe/<int:idC>')
@login_required
def showProfesseurByClasse(idC):
    if idC != 0 :
        session["classeSelected"] = idC
    else :
        session.pop("classeSelected",None)
    return redirect(url_for("professeur_list"))


@app.route('/professeur/filtre/module/<int:idM>')
@login_required
def showProfesseurByModule(idM):
    if idM != 0 :
        session["moduleSelected"] = idM
    else :
        session.pop("moduleSelected",None)
    return redirect(url_for("professeur_list"))


@app.route('/professeur/filtre/grade/<string:grade>')
@login_required
def showProfesseurByGrade(grade):
    if grade != '0' :
        session["gradeSelected"] = grade
    else :
        session.pop("gradeSelected",None)
    return redirect(url_for("professeur_list"))


@app.route('/professeur/details/<int:id>')
@login_required
def showProfesseurDetails(id):
    htmlClasse=None
    htmlModule=None

    if id !=0 : 
       prof = Professeur.query.filter_by(id=id).first()
       anneeScolaire = AnneeScolaire.query.filter_by(isActive=True).first()
       classes = Classe.query.filter_by(isArchived=False).join(Enseignement,Enseignement.classe_id==Classe.id).filter_by(professeur=prof,anneeScolaire=anneeScolaire).all()
       modules = Module.query.filter_by(isArchived=False).join(Enseignement.modules).filter(Enseignement.professeur_id ==prof.id, Enseignement.anneeScolaire_id==anneeScolaire.id).all()
       htmlClasse = render_template('models/professeur/detailClasse.html',professeur=prof, classes=classes)
       htmlModule = render_template('models/professeur/detailModule.html',professeur=prof, modules=modules)
    
    session['htmlClasse'] = htmlClasse
    session['htmlModule'] = htmlModule
    return redirect(url_for("professeur_list")) 

@app.route('/professeur/save', methods=['GET', 'POST'])
@app.route('/professeur/save/<int:id>', methods=['GET', 'POST'])
@login_required
def saveProfesseur(id=None):
    form = ProfesseurForm()
    isArchived = False
    error=None
    if id == None :
        professeur = Professeur()
    else :
        professeur = Professeur.query.filter_by(id=id).first()
        isArchived = True 
        if request.method == "GET" :
            form.login.data = professeur.login
            form.nomComplet.data = professeur.nomComplet
            form.portable.data = professeur.portable
            form.grade.data = professeur.grade
   
    if request.method=="POST" and form.validate_on_submit() :
        professeur.login = form.login.data 
        professeur.password = bcrypt.generate_password_hash (form.password.data).decode('utf-8')
        professeur.nomComplet = form.nomComplet.data 
        professeur.portable = form.portable.data
        professeur.grade = form.grade.data 
        professeur.isArchived = form.isArchived.data
        try :
            db.session.add(professeur)
            db.session.commit()
            form.login.data = ''
            form.password.data = ''
            form.nomComplet.data = ''
            form.portable.data = ''
            form.grade.data = ''
            isArchived=False
            app.logger.debug(professeur.__dict__)
            flash('Le professeur a été enregistrée avec succès.', 'success')
        except:
            error = "Cet email/numéro existe déjà, vueillez changer le login/numéro du professeur!"
            db.session.rollback()
    return render_template("models/professeur/form.html", form=form, isArchived=isArchived, error=error)


@app.route('/professeur/affectation/<int:id>', methods=['GET', 'POST'])
@login_required
def affectEnseignement(id):
    professeur = Professeur.query.filter_by(id=id).first()
    classesDuProfesseur = Classe.query.filter_by(isArchived=False).join(Enseignement).join(Professeur).filter_by(id=professeur.id).all()
    classesAll = Classe.query.filter_by(isArchived=False).all()
    classesNonAffectees = [item for item in classesAll if item not in classesDuProfesseur]
    modules = [(str(id),libelle) for id, libelle in db.session.query(Module.id, Module.libelle).all()]
    classes = [("","")]
    classes.extend([(str(classe.id),classe.libelle) for classe in classesNonAffectees])

    form = AffectationForm()
    form.classe.choices = classes
    form.modules.choices = modules
    error = None
    if request.method=="POST" and form.validate_on_submit() :
        enseignement = Enseignement()
        enseignement.professeur = professeur
        enseignement.anneeScolaire = AnneeScolaire.query.filter_by(isActive=True).first()
        enseignement.classe = Classe.query.filter_by(id=form.classe.data).first()
        for id in form.modules.raw_data :
            module = Module.query.filter_by(id=int(id)).first()
            # modules =[]
            enseignement.modules.append(module)
            
        try :
            db.session.add(enseignement)
            db.session.commit()
            form.classe.data = ''
            form.modules.data = ''
            flash('La classe a été enregistrée avec succès pour enseignement', 'success')
        except:
            error = "Erreur d'enregistrement "
            db.session.rollback()
    return render_template("models/professeur/affectation.html", form=form,error=error)



@app.route('/professeur/change/<int:idProf>')
@login_required
def changeProfesseurEncours(idProf):
    #Au chargement, effacer les operations en cours du prof
    session.pop('sessionId',None) 
    session.pop("voir",None)
    if idProf != 0 :
        session['profEncoursID'] = idProf
    else :
        session.pop('profEncoursID',None)
    return redirect(url_for("seance_list"))
