from flask import Flask, render_template, redirect, session, request,url_for,flash
from flask.globals import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt 



#--------------------Pagination 
def paginate(query):
    from flask_paginate import Pagination, get_page_args
    # Récupérer les paramètres de pagination de la requête
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Récupérer les données à paginer (par exemple, à partir d'une base de données)
    total_items = query.count() 
    data = query.offset(offset).limit(per_page).all()

    # Créer un objet Paginator avec les données paginées
    pagination = Pagination(page=page, total=total_items, per_page=per_page)
    
    return {'data':data,  'pagination':pagination}



app = Flask(__name__,template_folder="src/templates",static_folder="src/static")

app.config.from_pyfile("config/config.py")
app.app_context().push()

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db,render_as_batch=True)
bcrypt = Bcrypt(app) 


from src.controllers import *
from src.models import *


# Cette méthode sera exécutée avant chaque requête vers une route
@app.before_request
def avant_requete():
    session["path"]=request.path.split('/')[1]
    session["path_info"]=request.path
    g.user=current_user

#Mettre le g dans le context, il sera visible dans toutes les vues
@app.context_processor
def inject_globals():
    return {'global': g}



