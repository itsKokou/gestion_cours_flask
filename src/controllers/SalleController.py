from app import app, current_user, render_template, login_required,session, request,db,flash
from flask_paginate import Pagination, get_page_args
from ..models.Salle import Salle
from ..form.SalleForm import SalleForm


@app.route('/salle')
@login_required
def salle_list():
    query = Salle.query.filter_by(isArchived=False)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total_items = query.count() 
    
    salles = query.offset(offset).limit(per_page).all()
    
    pagination = Pagination(page=page, total=total_items, per_page=per_page)
    
    return render_template('models/salle/index.html',pagination= pagination, salles=salles)

@app.route('/salle/save', methods=['GET','POST'])
@app.route('/salle/save/<int:id>', methods=['GET','POST'])
@login_required
def saveSalle(id=None):
    form = SalleForm()
    isArchived = False
    error=None
    if id == None :
        salle = Salle()
    else :
        salle = Salle.query.filter_by(id=id).first()
        isArchived = True #pour afficher le champ
        if request.method == "GET" :
            form.libelle.data = salle.libelle
            form.nbrePlace.data = salle.nbrePlace

    if request.method=="POST" and form.validate_on_submit() :
        salle.libelle = form.libelle.data
        salle.nbrePlace = form.nbrePlace.data
        salle.isArchived = form.isArchived.data
        try :
            db.session.add(salle)
            db.session.commit()
            form.libelle.data = ''
            form.nbrePlace.data = ''
            isArchived=False
            app.logger.debug(salle.__dict__)
            flash('La salle a été enregistrée avec succès.', 'success')
        except:
            error = "Cette salle existe déjà !"
            db.session.rollback()

    return render_template("models/salle/form.html", form=form, isArchived=isArchived, error=error)