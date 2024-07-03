
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, EmailField,PasswordField
from wtforms.validators import DataRequired, Length, Email, InputRequired, Regexp
from ..models.Professeur import Professeur
from app import db


grades = [("","")]
grades.extend([(grade[0],grade[0]) for grade in db.session.query(Professeur.grade).distinct().all()])

class ProfesseurForm(FlaskForm):

    login = EmailField(label="Identifiant",
                        validators=[
                            DataRequired("Le login est requis"),
                            Email("Le login doit être un email")
                            ],
                        render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    password = PasswordField(label="Mot de passe",
                        validators=[
                            DataRequired("Veuillez choisir une filière"),
                            Length(min=4, message="Le mot de passe doit avoir au minimun {min} caractères")
                            ],
                        render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    nomComplet = StringField("Nom et Prénoms",
                          validators=[
                              InputRequired("Le libelle est requis"), 
                              Length(min=5, message="minimum {min} caractères pour le nom complet")
                           ],
                          render_kw={'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    portable = StringField("Téléphone",
                          validators=[
                              InputRequired("Le téléphone est requis"), 
                              Regexp('^\d{9}$', message="Veuillez entrer uniquement des chiffres"),
                              Length(min=9, max=9, message="Le numéro doit avoir 9 chiffres")
                           ],
                          render_kw={'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    grade = SelectField(label="Grade",
                        choices= grades,
                        validators=[
                            DataRequired("Veuillez choisir un grade"),
                            ],
                        render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    isArchived = BooleanField(label=('Archivé'), render_kw={'class':"rounded mt-1 w-3.5 h-3.5 mr-3" })
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})

