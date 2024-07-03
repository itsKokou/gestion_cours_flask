from app import app, current_user, render_template, login_required,session, request,paginate,db,flash
from ..models.Module import Module
from ..form.ModuleForm import ModuleForm
from sqlalchemy.exc import IntegrityError

@app.route('/module', methods=['GET','POST'])
@app.route('/module/<int:id>', methods=['GET','POST'])
def module_list(id=None):
    
    form = ModuleForm()
    isArchived = False
    error = None
    if id == None :
        module = Module()
    else :
        module = Module.query.filter_by(id=id).first()
        isArchived = True #pour afficher le champ
        if request.method == "GET" :
            form.libelle.data = module.libelle

    if request.method=="POST" and form.validate_on_submit() :
        module.libelle = form.libelle.data.upper()
        module.isArchived = form.isArchived.data
        try :
            db.session.add(module)
            db.session.commit()
            form.libelle.data = ''
            isArchived=False
            flash('Le module a été enregistré avec succès.', 'success')
        except :
            error = "Ce module existe déjà !"
            # Faites ce que vous voulez avec l'erreur, par exemple, annulez la transaction
            db.session.rollback()
    
    query = Module.query.filter_by(isArchived=False)
    results = paginate(query)
    modules = results['data']
    pagination = results['pagination']
    return render_template("models/module/index.html", modules=modules, pagination=pagination, form=form, isArchived=isArchived, error=error)