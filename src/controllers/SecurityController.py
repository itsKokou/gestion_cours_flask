from app import app,bcrypt, request, session,redirect, render_template
#---------Login
#login_required protege les route
from flask_login import (LoginManager, UserMixin, login_user , login_required, current_user,logout_user)
from ..models.User import User
from ..models.AnneeScolaire import AnneeScolaire
from ..models.Classe import Classe
from ..models.Professeur import Professeur
from ..models.Enseignement import Enseignement
from ..models.AnneeScolaire import AnneeScolaire


login_manager = LoginManager(app)
#Redirige dans login si pas connecté mais veut aller loin
login_manager.login_view = "login"
#Changer le message du please à la redirection vers connexion là
login_manager.login_message = "Veuillez vous connecter !"


#Recupère le user connecté pour le truc de login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return redirect("/login")

@app.route('/login', methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        login = request.form["login"]
        password = request.form.get("password")
        user = User.query.filter_by(login=login).first()
        if not user :
            error="Login ou mot de passe incorrect"
        else:
            is_valid = bcrypt.check_password_hash(user.password , password)
            if is_valid == False :
                error="Login ou mot de passe incorrect"
            else:
                # Mettre user dans la session
                login_user(user)

                #Charger les select de base, annee, professeur, classe
                annees = AnneeScolaire.query.filter_by(isArchived=False).all()
                anneeEncours = AnneeScolaire.query.filter_by(isArchived=False, isActive=True).first()
                professeurs = Professeur.query.filter_by(isArchived=False).all()
                classes = Classe.query.filter_by(isArchived=False).all()
                if user.role.libelle == "ROLE_PROFESSEUR":
                    anneeActuelle = AnneeScolaire.query.filter_by(isActive=True).first()
                    classes = Classe.query.filter_by(isArchived=False).join(Enseignement).filter_by(anneeScolaire=anneeActuelle).join(Professeur).filter_by(id=current_user.id).all()
                    pass
                
                
                annees_disct = []
                classes_dict = []
                professeurs_dict = []
                for index,an in enumerate(annees) :
                    annees_disct.append(an.to_json()) 
                for index,cl in enumerate(classes) :
                    classes_dict.append(cl.to_json())
                for index,prof in enumerate(professeurs) :
                    professeurs_dict.append(prof.to_json())

                session['anneeEncours'] = anneeEncours.to_json()
                session['annees'] = annees_disct
                session['classes'] = classes_dict
                session['professeurs'] = professeurs_dict
                if 'next' in session :
                    next = session["next"]
                    if next is not None :
                        return redirect(next)
                else:
                    return redirect("/home")
                session["next"] = request.args.get("next")
    return render_template("security/login.html", error=error)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect("/login")

