from app import app, current_user, render_template, login_required,session, request,redirect,paginate,url_for, flash, db
from ..models.Classe import Classe
from ..models.Niveau import Niveau
from ..models.Filiere import Filiere
from ..form.ClasseForm import ClasseForm

@app.route('/classe')
@login_required
def classe_list():
    filiere=None
    niveau=None
    
    query = Classe.query.filter_by(isArchived=False)
    if 'niveauSelected' in session:
        niveau = Niveau.query.filter_by(id=session.get('niveauSelected')).first()
        query = query.filter_by(niveau=niveau)
    
    if 'filiereSelected' in session :
        filiere = Filiere.query.filter_by(id=session.get('filiereSelected')).first()
        query = query.filter_by(filiere=filiere)

    selected={
        'filiere' : filiere,
        'niveau' : niveau
    }

    results = paginate(query)
    classes = results.get('data')
    pagination = results.get('pagination')

    niveaux = Niveau.query.all()
    filieres = Filiere.query.all()
    return render_template("models/classe/index.html", classes= classes, pagination=pagination, niveaux=niveaux,
                           filieres=filieres ,selectedValue=selected) 

@app.route('/classe/filtre/filiere/<int:idF>')
@login_required
def showClasseByFiliere(idF):
    if  idF != 0 : 
        session["filiereSelected"] = idF
    else :
        session.pop("filiereSelected",None)
    
    return redirect("/classe") 

@app.route('/classe/filtre/niveau/<int:idN>')
@login_required
def showClasseByNiveau(idN):
    if  idN != 0 : 
        session["niveauSelected"] = idN
    else :
        session.pop("niveauSelected",None)
    
    return redirect("/classe") 

@app.route('/classe/save', methods=['GET', 'POST'])
@app.route('/classe/save/<int:id>', methods=['GET', 'POST'])
@login_required
def saveClasse(id=None):
    form = ClasseForm()
    isArchived = False
    error=None
    if id == None :
        classe = Classe()
    else :
        classe = Classe.query.filter_by(id=id).first()
        isArchived = True 
        if request.method == "GET" :
            form.libelle.data = classe.libelle
            form.effectif.data = classe.effectif
            form.niveau.data = classe.niveau.id
            form.filiere.data = classe.filiere.id
   
    if request.method=="POST" and form.validate_on_submit() :
        classe.libelle = form.libelle.data
        classe.effectif = form.effectif.data if form.effectif.data!=None else 0
        classe.niveau = Niveau.query.filter_by(id=form.niveau.data).first()
        classe.filiere = Filiere.query.filter_by(id=form.filiere.data).first()
        classe.isArchived = form.isArchived.data
        try :
            db.session.add(classe)
            db.session.commit()
            form.libelle.data = ''
            form.effectif.data = ''
            form.niveau.data = ''
            form.filiere.data = ''
            isArchived=False
            app.logger.debug(classe.__dict__)
            flash('La classe a été enregistrée avec succès.', 'success')
        except:
            error = "Cette classe existe déjà !"
            db.session.rollback()
    return render_template("models/classe/form.html", form=form, isArchived=isArchived, error=error)



@app.route('/classe/change/<int:id>')
def changeClasseEncours(id):
    session.pop('sessionId',None) #Au chargement, effacer la déclaration en cours du prof
    if id != 0 :
        classeEncours =Classe.query.filter_by(id=id).first()
        session['classeEncoursID'] = classeEncours.id
    else :
        session.pop('classeEncoursID',None)


    return redirect(url_for("seance_list"))
