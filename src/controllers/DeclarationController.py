from app import app, current_user, render_template, login_required,session, request, db, flash, redirect, url_for
from flask_paginate import Pagination, get_page_args
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
from ..form.DeclarationForm import DeclarationForm


@app.route('/declaration')
def declaration_list():
    pass

@app.route('//declaration/save', methods=["GET", "POST"])
@login_required
def saveDeclaration():
    form = DeclarationForm()
    declaration = Declaration()
    error = None
    if 'sessionId' in session :
        declaration.seance_id = session.get("sessionId")
        declaration.user_id = current_user.id

    if form.validate_on_submit(): 
        declaration.motif = form.motif.data
        declaration.description = form.description.data

        try :
            db.session.add(declaration)
            db.session.commit()
            flash('La déclaration a bien été enregistrée !','success')
        except Exception as e :
            error = "Erreur d'enregistrement de la déclaration"
            db.session.rollback()
    
    htmlDeclaration = render_template("models/declaration/form.html",form=form,error=error)
    session["htmlDeclaration"] = htmlDeclaration
    return redirect(url_for("seance_list"))