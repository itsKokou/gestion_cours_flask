from app import app, current_user, render_template, login_required,session, request,redirect,url_for, db, flash
from datetime import datetime, timedelta
from ..models.Etudiant import Etudiant
from ..models.Inscription import Inscription
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..models.Cours import Cours
from ..models.Declaration import Declaration
from ..models.Salle import Salle
from ..models.Professeur import Professeur
from ..models.Etudiant import Etudiant
from ..models.Absence import Absence
from ..models.Seance import Seance
from ..models.Enseignement import Enseignement
from ..form.SeanceForm import SeanceForm
from ..form.DeclarationForm import DeclarationForm
from ..helpers.List_tojson import listToJson

def findSeanceByProfesseurAndClasse(idProf, idClasse, anneeEnCours) :
    professeur = Professeur.query.filter_by(id=idProf).first()
    seances = []
    if idClasse != 0 :
        classe = Classe.query.filter_by(id=idClasse).first()
        seancesP = Seance.query.filter_by(isArchived=False,professeur=None).join(Cours).filter(Cours.professeur==professeur).filter(Cours.anneeScolaire==anneeEnCours,Cours.classes.contains(classe)).all()
        seancesO = Seance.query.filter_by(isArchived=False,professeur=professeur).join(Cours).filter(Cours.anneeScolaire==anneeEnCours,Cours.classes.contains(classe)).all()
    else :
        seancesP = Seance.query.filter_by(isArchived=False,professeur=None).join(Cours).filter(Cours.professeur==professeur).filter_by(anneeScolaire=anneeEnCours).all()
        seancesO = Seance.query.filter_by(isArchived=False,professeur=professeur).join(Cours).filter_by(anneeScolaire=anneeEnCours).all()

    seances.extend(seancesO)
    seances.extend(seancesP)
    seancesProf = []
    for seance in seances :
        if seance.professeur == None :
            if seance.cours.professeur.id == idProf :
                seancesProf.append(seance)
        else :
            if seance.professeur.id == idProf :
                seancesProf.append(seance)
    return seancesProf

def prepareEvents(seances) :
    colors = ['da974b', '#E8B01F', '#DBCB89', '#71BCF3', '#E0474C', '#7FB8B4', '#B2B1B1', '#9F4C9D', '#0073BC', '#94918d', '#5dffe3', '#1d96d5', '#FFFA00', '#e40090', '#21FF19', '#f20089', '#41dfa8', '#FF1493', '#6A5ACD', '#FFDEAD', '#7FFF00', '#00FA9A', '#00FFFF', '#00CED1', '#1E90FF', '#FF6347', '#DA70D6'];
    events = []
    import random
    for seance in seances :
        prof = seance.professeur if seance.professeur != None else seance.cours.professeur
        li =  "SALLE "+ seance.salle.libelle if seance.salle != None else seance.codeSeance
        lieu = "Lieu : " + li
        desc = prof.nomComplet
        color = colors[random.randint(0, len(colors) - 1)]
        date = seance.date.strftime('%Y-%m-%d') + ' ' + seance.heureD.strftime('%H:%M:%S')
        newdate = seance.date.strftime('%Y-%m-%d') + ' ' + seance.heureF.strftime('%H:%M:%S') #date("Y-m-d H:i:s", strtotime('+1 day', strtotime(seance->getDate()->format('y-m-d H:i:s'))))

        event = {
            'id' : seance.id,
            'start' : date,
            'end' : newdate,
            'title' : seance.cours.module.libelle,
            'description' : desc,
            'location' : lieu,
            'color' : color,
            'textColor' : "#000000",
            'allDay' : False,
        }
        if current_user.role.libelle != "ROLE_ETUDIANT" :
            event['url'] = "/seance/click/"+ str(seance.id)
        else :
            # Peut declarer absence seulement une heure avant le debut du cours
            dateToday = datetime.now() 
            d = datetime.strptime(date,'%Y-%m-%d %H:%M:%S') #Date de la seance avec heure
            une_heure_avant = d - timedelta(hours=1) #Une heure Avant la seance
            # app.logger.debug(dateToday < une_heure_avant)
            # app.logger.debug(dateToday)
            # app.logger.debug(une_heure_avant)
            if dateToday < une_heure_avant :
                event['url'] = "/seance/click/" + str(seance.id)
             
        events.append(event)
    
    return events
    

@app.route('/seance')
def seance_list():
    #----------------Index Affichage 
    anneeActuelle = AnneeScolaire.query.filter_by(isActive=True).first()
    seances = Seance.query.filter_by(isArchived=False).join(Cours).filter_by(anneeScolaire=anneeActuelle).all()
    # Recuperer seance specifique à prof ou etudiant
    if current_user.role.libelle == "ROLE_ETUDIANT" :
        etudiant = Etudiant.query.filter_by(id=current_user.id).first()
        inscriptionActuelle = Inscription.query.filter_by(etudiant=etudiant,anneeScolaire=anneeActuelle).first()
        seances =Seance.query.filter_by(isArchived=False).join(Cours).filter(Cours.anneeScolaire==anneeActuelle, Cours.classes.contains(inscriptionActuelle.classe)).all()
    elif current_user.role.libelle == "ROLE_PROFESSEUR" :
        if 'classeEncoursID' in session :
            idClasse =  session.get('classeEncoursID')
        else :
            idClasse = 0

        seances = findSeanceByProfesseurAndClasse(current_user.id, idClasse, anneeActuelle)
        
    # Recuperer seance specifique prof ou classe pour admin
    if current_user.role.libelle != "ROLE_ETUDIANT" and current_user.role.libelle != "ROLE_PROFESSEUR" :
        
        if 'classeEncoursID' in session :
            idClasse = session.get('classeEncoursID')
            classe = Classe.query.filter_by(id=idClasse).first()
            seances = seances = Seance.query.filter_by(isArchived=False).join(Cours).filter(Cours.anneeScolaire==anneeActuelle,Cours.classes.contains(classe)).all()
        else :
            idClasse = 0
            seances = seances = Seance.query.filter_by(isArchived=False).join(Cours).filter(Cours.anneeScolaire==anneeActuelle).all()
        
        if 'profEncoursID' in session : 
            seances = findSeanceByProfesseurAndClasse(session.get('profEncoursID'), idClasse, anneeActuelle)

    events = prepareEvents(seances)
    import json
    donnees = json.dumps(events)
    #--------------------------------------------------
    #----------------Faire declaration-----------------
    htmlDeclaration = None
    htmlDeclarationError = None
    succes = None
    htmlEtudiant = None
    htmlAbsence = None
    finSession = None
    debutSession = None
    if 'seanceId' in session and (current_user.role.libelle == "ROLE_ETUDIANT" or current_user.role.libelle == "ROLE_PROFESSEUR") :
        
        declarationExist = Declaration.query.filter(Declaration.seance_id==session.get('seanceId'),Declaration.user_id==current_user.id).first()
        if declarationExist != None :
            session.pop('seanceId',None)
            htmlDeclarationError = "Vous avez déjà effectué une déclaration pour cette seance de cours"
        else :
            declaration = Declaration()

            seance = Seance.query.filter_by(id=session.get('seanceId')).first()
            declaration.seance = seance
            declaration.user = current_user
            form = DeclarationForm()
            error = None

            if form.validate_on_submit(): 
                declaration.motif = form.motif.data
                declaration.description = form.description.data

                try :
                    db.session.add(declaration)
                    db.session.commit()
                    flash('La déclaration a bien été enregistrée !','success')

                    if  current_user.role.libelle == "ROLE_PROFESSEUR" :
                    
                        #checker si session pas commencer pour annuler 
                        dateD = seance.date.strftime('%Y-%m-%d') + ' ' + seance.heureD.strftime('%H:%M:%S')
                        dateToday =  dateToday = datetime.now() 
                        dateDebutSession = datetime.strptime(dateD,'%Y-%m-%d %H:%M:%S')
                        debutSession = dateDebutSession > dateToday
                        if debutSession == True :
                            return redirect(url_for("ArchiverSeance"))

                    session.pop('seanceId',None)
                    
                except Exception as e :
                    error = "Erreur d'enregistrement de la déclaration"
                    db.session.rollback()
    
            htmlDeclaration = render_template("models/declaration/form.html",form=form,error=error)

    else :
        #---demander faire absence ou voir liste étudiants
        if 'seanceId' in session and current_user.role.libelle != "ROLE_ETUDIANT" and current_user.role.libelle != "ROLE_PROFESSEUR" :
            seance = Seance.query.filter_by(id=session.get('seanceId')).first()
            isAbsence = seance.isAbsence

            # checker si session est fini avant marquer absence ou si session pas fini pour annuler 
            # dateD = seance->getDate()->format('Y-m-d') . ' ' . seance->getHeureD()->format('H:i:s');
            dateToday = datetime.now() 
            dateF = seance.date.strftime('%Y-%m-%d')+ ' '+ seance.heureF.strftime('%H:%M:%S')
            # dateDebutSession = new DateTime(dateD, new \DateTimeZone("GMT"));
            dateFinSession = datetime.strptime(dateF,'%Y-%m-%d %H:%M:%S')

            finSession = dateFinSession <= dateToday

            #montrer marquer absence ou liste etudiants
            htmlEtudiant = render_template('models/seance/etudiant.html',classes=seance.cours.classes,absences = seance.absences,
                                           isAbsence=isAbsence, finSession=finSession)
   
    return render_template('models/seance/index.html',donnees=donnees,htmlDeclaration=htmlDeclaration,
                           htmlDeclarationError=htmlDeclarationError,htmlEtudiant=htmlEtudiant,htmlAbsence=htmlAbsence)


@app.route('/seance/vider/session')
@login_required
def viderSession():
    session.pop("seanceId",None)
    session.pop("voir",None)
    return redirect(url_for("seance_list"))

@app.route('/seance/click/<int:id>')
@login_required
def clickSeance(id):
    session['seanceId'] = id
    return redirect(url_for("seance_list"))

   
@app.route('/seance/voir/<element>')
@login_required
def VoirSeanceElements(element):
    session['voir'] = element
    return redirect(url_for("seance_list"))


@app.route('/seance/absences/save')
@app.route('/seance/absences/save/<presences>')
@login_required
def SaveSeanceAbsences(presences=None):
    anneeEnCours = AnneeScolaire.query.filter_by(isActive=True).first()
    seance = Seance.query.filter_by(id=session.get("seanceId")).first()
    # Mis à jour des nbreHeures réalisées du cours
    cours = seance.cours
    diff = seance.heureF - seance.heureD
    nbreHeure = int(diff.seconds/3600)
    cours.nbreHeureRealise = cours.nbreHeureRealise + nbreHeure

    #Absences
    seance.isAbsence = True
    tabPresences = list(map(int, presences.split(',')))
    classes = seance.cours.classes
    for cl in classes :
        for ins in cl.inscriptions :
            if ins.etudiant.id not in tabPresences  and ins.anneeScolaire.id == anneeEnCours.id :
                absence =  Absence()
                absence.isArchived = False
                absence.etudiant = ins.etudiant
                absence.seance = seance
                #si l'étudiant a fait une déclaration, son absence n'est pas enregistrée
                declaration = Declaration.query.filter_by(user=ins.etudiant, seance=seance).first()
                if declaration == None :
                    pass
                    #Enregistrer Absence
                    db.session.add(absence)
                    db.session.commit()      
    session.pop("seanceId",None)
    session.pop("voir",None)
    return redirect(url_for("seance_list"))


@app.route('/seance/archiver')
@login_required
def ArchiverSeance():
    seance = Seance.query.filter_by(id=session.get("seanceId")).first()
    #Mis à jour des nbreHeures Planifié et restant de cours
    cours = seance.cours
    diff = datetime.strptime(seance.heureF.strftime("%H:%M"), "%H:%M") - datetime.strptime(seance.heureD.strftime("%H:%M"), "%H:%M")
    nbreHeure = int(diff.seconds/3600)
    cours.nbreHeurePlanifie = cours.nbreHeurePlanifie - nbreHeure
    cours.nbreHeureRestantPlan = cours.nbreHeureRestantPlan + nbreHeure
    seance.isArchived = True
    #Enregistrer Seance
    db.session.add(seance)
    db.session.add(cours)
    db.session.commit()
    session.pop("seanceId",None)
    session.pop("voir",None)
    return redirect(url_for("seance_list"))
    

def disponibilite(seances, date, heureD, heureF) :
    isDispo = 1

    for session in seances:
        sessionDate = session.date
        sessionHeureD = session.heureD
        sessionHeureF = session.heureF

        if date == sessionDate :
            if sessionHeureD < heureF and heureF < sessionHeureF :
                isDispo = 0
            else :
                if sessionHeureD < heureD and heureD < sessionHeureF :
                    isDispo = 0
                else :
                    if heureD <= sessionHeureD and sessionHeureD <= sessionHeureF and sessionHeureF <= heureF :
                        isDispo = 0
                    else :
                        if sessionHeureD <= heureD and heureD <= heureF and heureF <= sessionHeureF :
                            isDispo = 0    
    return isDispo
    

@app.route('/seance/save/<int:id>', methods=['GET','POST'])
@login_required
def saveSeance(id):
    form = SeanceForm()
    error = None
    salles = listToJson(Salle.query.filter_by(isArchived=False).all())
    seances = listToJson(Seance.query.filter_by(isArchived=False,isAbsence=False).all())
    cours = Cours.query.filter_by(id=id).first()
    classes = listToJson(cours.classes)
    anneeScolaire = AnneeScolaire.query.filter_by(isActive=True).first()
    enseignements = listToJson(Enseignement.query.filter_by(anneeScolaire=anneeScolaire).all())
    courss = listToJson(Cours.query.filter_by(isArchived=False, anneeScolaire=anneeScolaire).all())
    professeurs = listToJson(Professeur.query.filter_by(isArchived=False).all())
    
    if form.is_submitted():
        seancesClasse = []
        for cl in cours.classes :
            seancesClasse.extend( Seance.query.filter_by(isArchived=False,).join(Cours, Seance.cours).filter(Cours.classes.contains(cl)).all())
            
        disponible = disponibilite(seancesClasse,form.date.data, form.heureD.data,form.heureF.data)
        if disponible==1 :
            seance = Seance()
            seance.isAbsence = False
            seance.isArchived =False
            seance.cours_id = cours.id
            seance.date = form.date.data
            seance.heureD =  form.heureD.data
            seance.heureF =  form.heureF.data
            seance.codeSeance = form.code.data

            if form.salle.data != None :
                seance.salle_id = form.salle.data

            if form.professeur.data != None :
                seance.professeur_id = form.professeur.data
            

            
            try :

                diff = datetime.strptime(seance.heureF.strftime("%H:%M"), "%H:%M") - datetime.strptime(seance.heureD.strftime("%H:%M"), "%H:%M")
                nbreHeure = int(diff.seconds/3600)
                cours.nbreHeurePlanifie = cours.nbreHeurePlanifie + nbreHeure
                cours.nbreHeureRestantPlan = cours.nbreHeureRestantPlan - nbreHeure

                db.session.add(seance)
                db.session.add(cours)
                db.session.commit()


                form.date.data = ""
                form.heureD.data = ""
                form.heureF.data = ""
                form.code.data = ""
                form.salle.data = ""
                form.professeur.data = ""
                

                flash("La séance a été enregistrée avec succès.", 'success')
            except:
                error = "Erreur d'enregistrement de la séance"
                db.session.rollback()
        else:
            error = "Les classes du cours sont occupées à ces horaires de ce jour"
    else :
        app.logger.debug(form.errors)

    return render_template("models/seance/form.html", form=form, error=error, salles=salles, seances=seances,
                           cours=cours.to_json(),classes=classes,courss=courss, enseignements=enseignements,
                           professeurs=professeurs)
