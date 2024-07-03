from app import app, current_user, render_template, login_required,session,request,redirect,paginate, db, flash
from ..models.AnneeScolaire import AnneeScolaire
from ..form.AnneeScolaireForm import AnneeScolaireForm

@app.route('/annee/scolaire')
@login_required
def anneeScolaire_list():
    session.pop("AnneeLibelle",None) # 
    query = AnneeScolaire.query.filter_by(isArchived=False)
    results = paginate(query)
    return render_template("models/annee_scolaire/index.html",annees=results.get('data'), pagination=results.get('pagination') )


@app.route('/annee/scolaire/save', methods=[ 'GET','POST'])
@app.route('/annee/scolaire/save/<int:id>', methods=[ 'GET','POST'])
@login_required
def saveAnneeScolaire(id=None):
    form = AnneeScolaireForm()
    isArchived = False
    error = None
    if id == None :
        anneeScolaire = AnneeScolaire()
    else :
        anneeScolaire = AnneeScolaire.query.filter_by(id=id).first()
        isArchived = True #pour afficher le champ
        if request.method == "GET" :
            form.libelle.data = anneeScolaire.libelle
            form.isActive.data = anneeScolaire.isActive

    if request.method=="POST" and form.validate_on_submit() :
        anneeScolaire.libelle = form.libelle.data
        anneeScolaire.isActive = form.isActive.data
        anneeScolaire.isArchived = form.isArchived.data

        #Si isActive, changer dans la bd et la session.
        if anneeScolaire.isActive :
            changeActiveToFalseInBD()

        try :
            # On enregistre
            db.session.add(anneeScolaire)
            db.session.commit()
            #change dans session
            anneesInSession = session.get("annees")
            anneeEncours = AnneeScolaire.query.filter_by(isActive=True).first()
            session['anneeEncours'] = anneeEncours.to_json()
            session['annees'] =  changeAnneeInSession(anneesInSession, anneeEncours.id)

            form.debut.data = ''
            form.libelle.data = ''
            form.isActive.data = False
            isArchived=False
            flash("L'annee scolaire a été enregistrée avec succès.", 'success')
        except :
            error = "Cette annee scolaire existe déjà !"
            # Faites ce que vous voulez avec l'erreur, par exemple, annulez la transaction
            db.session.rollback()
    return render_template("models/annee_scolaire/form.html", form=form, isArchived=isArchived, error=error)

def changeActiveToFalseInBD():
    annee = AnneeScolaire.query.filter_by(isActive=True).first()
    annee.isActive = False
    db.session.add(annee)
    db.session.commit()

def changeAnneeInSession(anneesInSession,id):
    for key, annee in enumerate(anneesInSession) : 
        anneesInSession[key]["isActive"] = anneesInSession[key]["id"]==id
    return anneesInSession

@app.route('/annee/scolaire/change/<int:id>')
@login_required
def changeAnneeEncours(id):
    anneesInSession = session.get("annees")
    anneeEncours = AnneeScolaire.query.filter_by(id=id).first()
    session['anneeEncours'] = anneeEncours.to_json()
    session['annees'] =  changeAnneeInSession(anneesInSession, id)
    session.pop('classeSelected',None)

    return redirect(session.get("path_to_go"))

    