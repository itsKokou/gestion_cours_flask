from app import app,bcrypt, current_user, render_template, login_required,session, request,redirect,paginate,url_for,db,flash
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
from ..form.EtudiantForm import EtudiantForm


@app.route('/etudiant')
@login_required
def etudiant_list():
    #Le modal de absence et dossier
    htmlAbsence = session.pop("htmlAbsence",None)
    htmlDossier = session.pop("htmlDossier",None)
    session["path_to_go"] = "/etudiant" #Annnee scolaire pour redirect apres change select
    classe = None
    anneeScolaire = AnneeScolaire.query.filter_by(id=session['anneeEncours']['id']).first()
    query = Etudiant.query.filter_by(isArchived=False).join(Inscription).filter_by(isArchived=False, anneeScolaire=anneeScolaire)
    
    if 'classeEtudiant' in session :
        classe=Classe.query.filter_by(id= session.get('classeEtudiant')).first()
        query = query.filter_by(classe=classe)
    
    selected={
        'anneeScolaire' : anneeScolaire,
        'classe' : classe,
    }
    
    results = paginate(query)
    etudiants = results.get('data')
    pagination = results.get('pagination')
    classes = Classe.query.filter_by(isArchived=False).all()
    return render_template("models/etudiant/index.html", selectedValue=selected, etudiants=etudiants,pagination=pagination,
                           classes=classes,htmlAbsence=htmlAbsence,htmlDossier=htmlDossier)


@app.route('/etudiant/filtre/classe/<int:idC>')
@login_required
def showEtudiantByClasse(idC):
    if idC != 0 :
        session["classeEtudiant"] = idC
    else :
        session.pop("classeEtudiant",None)
    return redirect(url_for('etudiant_list'))


@app.route('/etudiant/absences/<int:id>')
@login_required
def showEtudiantAbsences(id):
    htmlAbsence = None

    if id != 0 :
        anneeScolaire = AnneeScolaire.query.filter_by(id=session['anneeEncours']['id']).first()
        etudiant = Etudiant.query.filter_by(id=id).first()
        absences = query = Absence.query.filter_by(isArchived=False,etudiant=etudiant).join(Seance).join(Cours).filter_by(anneeScolaire=anneeScolaire).all()
        htmlAbsence = render_template('models/etudiant/absence.html', etudiant=etudiant,absences=absences,
                                      anneeEncours=anneeScolaire)
    session['htmlAbsence'] = htmlAbsence
    return redirect(url_for('etudiant_list'))


@app.route('/etudiant/dossier/<int:id>')
@login_required
def showEtudiantDossier(id):
    htmlDossier = None

    if id != 0 :
        anneeScolaire = AnneeScolaire.query.filter_by(id=session['anneeEncours']['id']).first()
        etudiant = Etudiant.query.filter_by(id=id).first()
        inscription = Inscription.query.filter_by(etudiant=etudiant, anneeScolaire=anneeScolaire).first() # Inscription en cours
        htmlDossier = render_template('models/etudiant/dossier.html', etudiant=etudiant,inscription=inscription)
    session['htmlDossier'] = htmlDossier
    return redirect(url_for('etudiant_list'))

@app.route('/etudiant/save/<int:id>', methods=['GET', 'POST'])
@login_required
def saveEtudiant(id):
    form = EtudiantForm()
    isArchived = False
    error=None

    etudiant = Etudiant.query.filter_by(id=id).first()
    isArchived = True

    if request.method == "GET" :
        form.login.data = etudiant.login
        form.nomComplet.data = etudiant.nomComplet
        form.tuteur.data = etudiant.tuteur
        form.photo.data = etudiant.photo
   
    if request.method=="POST" and form.validate_on_submit() :
        etudiant.login = form.login.data 
        etudiant.password = bcrypt.generate_password_hash (form.password.data).decode('utf-8') 
        etudiant.nomComplet = form.nomComplet.data 
        etudiant.tuteur = form.tuteur.data
        etudiant.isArchived = form.isArchived.data
        
        try :
            db.session.add(etudiant)
            db.session.commit()
            #Enregistrer la photo
            if form.photo.data != "" :
                from ..helpers.upload import uploadPhoto
                uploadPhoto(form.photo.data,etudiant.matricule)

            form.password.data = ''
            isArchived=False
            flash('Le etudiant a été enregistrée avec succès.', 'success')
        except:
            error = "Erreur d'enregistrement de l'étudiant"
            db.session.rollback()
    return render_template("models/etudiant/form.html", form=form, isArchived=isArchived, error=error)

