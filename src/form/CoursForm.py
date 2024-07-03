
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class CoursForm(FlaskForm):
    semestre = SelectField(label="Semestre",
                        validators=[
                            DataRequired("Veuillez choisir le semestre du cours"),
                            ],
                        render_kw={'id':"semestre",'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    module = SelectField(label="Module",
                        validators=[
                            DataRequired("Veuillez choisir le module"),
                            ],
                        render_kw={'id':"module",'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    professeur = SelectField(label="Professeur",
                        validators=[
                            DataRequired("Veuillez choisir le professeur du cours"),
                            ],
                        render_kw={'id':"professeur",'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    nbreHeureTotal = IntegerField(label="Total heure", 
                                  validators=[
                                        DataRequired("Veuillez saisir le nombre d'heure total du module "),
                                        NumberRange(min=16, max=40, message="Le nombre d'heure doit être entre {min} et {max} inclus")
                                    ],
                            render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    classes = SelectMultipleField(label="Classes",
                        validators=[
                            DataRequired("Veuillez choisir au moins une classe pour ce cours"),
                            ],
                        render_kw={'id':'classe','class':"select2 w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    isArchived = BooleanField(label=('Archivé'), render_kw={'class':"rounded mt-1 w-3.5 h-3.5 mr-3" })
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'id':'submit','class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})

            
            
