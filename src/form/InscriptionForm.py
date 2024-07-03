
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FormField, StringField
from wtforms.validators import DataRequired
from .EtudiantForm import EtudiantForm


class InscriptionForm(FlaskForm):
    matricule = StringField(label="Matricule",
                        render_kw={'id':'matricule','class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    etudiant = FormField(EtudiantForm)
    classe = SelectField(label="Classe",
                        validators=[
                            DataRequired("Veuillez choisir la classe de l'étudiant"),
                            ],
                        render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})

