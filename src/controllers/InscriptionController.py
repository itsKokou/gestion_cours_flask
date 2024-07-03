from app import app, current_user, render_template, login_required,session, request,paginate,url_for,redirect, flash, db
from ..models.Etudiant import Etudiant
from ..models.Inscription import Inscription
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..form.InscriptionForm import InscriptionForm
from datetime import datetime

        


@app.route('/inscription')
@login_required
def inscription_list():
    session["path_to_go"] = "/inscription" #Pour année change
    classe = None
    date = None
    
    anneeScolaire = AnneeScolaire.query.filter_by(id=session['anneeEncours']['id']).first()
    query = Inscription.query.filter_by(isArchived=False,anneeScolaire=anneeScolaire)
    if 'classeSelected' in session :
        classe = Classe.query.filter_by(id=session.get('classeSelected')).first()
        query = query.filter_by(classe=classe)

    if 'dateSelected' in session :
        date = datetime.strptime(session.get('dateSelected'),"%Y-%m-%d").date()
        query = query.filter_by(createAt=date)
    

    selected = {
        'anneeScolaire' : anneeScolaire,
        'classe' : classe,
        'date' : date
    }

    results = paginate(query)
    inscriptions = results.get('data')
    pagination = results.get('pagination')
    classes = Classe.query.filter_by(isArchived=False).all()

    return render_template('models/inscription/index.html',selectedValue=selected,pagination=pagination,
                           inscriptions=inscriptions,classes=classes,htmlSwal=session.get("ArchiverSwal"))


@app.route('/inscription/classe/<int:id>')
@login_required
def showInscriptionByClasse(id):
    if id != 0 :
        session["classeSelected"] = id
    else :
        session.pop("classeSelected",None)
    return redirect(url_for('inscription_list'))


@app.route('/inscription/date')
@app.route('/inscription/date/<string:date>')
@login_required
def showInscriptionByDate(date):
    if date != '0' :
        session["dateSelected"] = date
    else :
        session.pop("dateSelected",None)
    return redirect(url_for('inscription_list'))


@app.route('/inscription/archiver/vider')
@login_required
def viderArchiverInscription():
    session.pop("ArchiverSwal",None)
    session.pop("inscriptionArchiver",None)
    return redirect(url_for('inscription_list'))


@app.route('/inscription/archiver')
@app.route('/inscription/archiver/<int:id>')
@login_required
def archiverInscription(id=None):
    if "inscriptionArchiver" in session :
        #Deuxieme : Archiver maintenant
        ins = Inscription.query.filter_by(id=session.get("inscriptionArchiver")).first()
        ins.isArchived = True
        #db.session.commit()
        session.pop("ArchiverSwal",None)
        session.pop("inscriptionArchiver",None)
    else :
        #Premier : afficher la vue
        ins = Inscription.query.filter_by(id=id).first()
        swal = {
            "etudiant" : ins.etudiant.nomComplet,
            "matricule" : ins.etudiant.matricule,
            "classe" : ins.classe.libelle
        }
        session["inscriptionArchiver"] = id
        session["ArchiverSwal"] = swal
    return redirect(url_for('inscription_list'))


#==================== Calcul de matricule
 
def generateMatricule( ):
    pos_etudiant = Etudiant.query.filter_by(isArchived=False).count() + 1 
    nbre_caracteres = 3
    # Convertir le nombre en chaîne de caractères
    pos_str = str(pos_etudiant)
    
    # Calculer le nombre de zéros à ajouter
    nbre_zeros = max(0, nbre_caracteres - len(pos_str))
    
    # Aligner en ajoutant les zéros nécessaires
    matricule = "MAT" + '0' * nbre_zeros + pos_str
    
    return matricule



@app.route('/inscription/save', methods=['GET', 'POST'])
@login_required
def saveInscription():
    from wtforms.validators import DataRequired
    form = InscriptionForm()
    classes = [("","")]
    classes.extend([(str(classe.id),classe.libelle) for classe in Classe.query.filter_by(isArchived=False).all()])
    form.classe.choices = classes
    form.etudiant.photo.validators = [DataRequired("Veuillez téléverser la photo de l'étudiant")]
    error=None
    
    if form.validate_on_submit() :
        inscription = Inscription()
        inscription.isArchived = False
        inscription.createAt = datetime.now().date()
        inscription.anneeScolaire = AnneeScolaire.query.filter_by(isActive=True).first()
        classe = Classe.query.filter_by(id=form.classe.data).first()
        etudiant = Etudiant()
        etudiant.matricule = generateMatricule()
        etudiant.nomComplet = form.etudiant.nomComplet.data 
        etudiant.login = form.etudiant.login.data
        etudiant.password = form.etudiant.password.data 
        etudiant.tuteur = form.etudiant.tuteur.data
        etudiant.isArchived = False
        try :
            #Enregistrer la photo
            if form.etudiant.photo.data != "" :
                from ..helpers.upload import uploadPhoto
                etudiant.photo = uploadPhoto(form.etudiant.photo.data,etudiant.matricule)

            
            classe.effectif = classe.effectif + 1
            inscription.etudiant = etudiant
            inscription.classe = classe
    
            db.session.add(inscription)
            db.session.commit()

            form.etudiant.nomComplet.data = ''
            form.etudiant.login.data = ''
            form.etudiant.password.data = ''
            form.etudiant.tuteur.data = ''
            form.etudiant.photo.data = ''
            form.classe.data = ''
            flash("L'inscription a été enregistrée avec succès.", 'success')
        except:
            error = "Erreur d'enregistrement de l'incription"
            db.session.rollback()
   
    return render_template("models/inscription/form.html", form=form, error=error,entete="Inscription")


@app.route('/reinscription', methods=['GET', 'POST'])
@app.route('/reinscription/<string:mat>', methods=['GET', 'POST'])
@login_required
def saveReinscription(mat=None):
    from wtforms.validators import DataRequired
    form = InscriptionForm()
    classes = [("0","")]
    classes.extend([(str(classe.id),classe.libelle) for classe in Classe.query.filter_by(isArchived=False).all()])
    form.classe.choices = classes
    form.matricule.validators = [DataRequired("Veuillez saisir le matricule de l'étudiant")]
    form.etudiant.nomComplet.render_kw['readonly'] = True
    form.etudiant.login.render_kw['readonly'] = True
    form.etudiant.tuteur.render_kw['readonly'] = True
    error=None
    etudiant = None
    anneeEncours = AnneeScolaire.query.filter_by(isActive=True).first()

    if mat != None:
        etudiant  = Etudiant.query.filter_by(matricule=mat.upper( )).first()
        if etudiant != None:
            form.etudiant.nomComplet.data = etudiant.nomComplet
            form.etudiant.login.data = etudiant.login
            form.etudiant.tuteur.data = etudiant.tuteur
            lastInscription  = sorted(Inscription.query.filter_by(etudiant=etudiant).all(),key=lambda x :x.id, reverse=True)[0]
            if lastInscription != None :
                form.classe.coerce = int
                form.classe.data = lastInscription.classe.id
        else:
            error = "Aucun étudiant ne correspond  à ce matricule."
        form.matricule.data = mat.upper()

    if form.validate_on_submit() :
        inscription = Inscription()
        inscription.isArchived = False
        inscription.createAt = datetime.now().date()
        inscription.anneeScolaire = anneeEncours
        classe = Classe.query.filter_by(id=form.classe.data).first()
        etudiant.password = form.etudiant.password.data 
        inscription.etudiant = etudiant
        
        try :
            #Enregistrer la photo
            if form.etudiant.photo.data != "" :
                from ..helpers.upload import uploadPhoto
                etudiant.photo = uploadPhoto(form.etudiant.photo.data,etudiant.matricule)

            
            app.logger.debug(classe.__dict__)
            classe.effectif = classe.effectif + 1
            inscription.etudiant = etudiant
            inscription.classe = classe

            db.session.add(inscription)
            db.session.commit()
            
            form.matricule.data = ''
            form.etudiant.nomComplet.data = ''
            form.etudiant.login.data = ''
            form.etudiant.password.data = ''
            form.etudiant.tuteur.data = ''
            form.etudiant.photo.data = ''
            form.classe.data = ''
            flash("La réinscription a été enregistrée avec succès.", 'success')
        except:
            error = "Erreur d'enregistrement de la réincription"
            db.session.rollback()
    
    return render_template("models/inscription/form.html", form=form, error=error,entete="Réinscription")

        
