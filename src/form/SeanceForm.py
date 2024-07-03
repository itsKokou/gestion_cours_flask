
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length

class SeanceForm(FlaskForm):
    date = DateField(label="Date",
                        validators=[
                            DataRequired("Veuillez choisir la date de la séance"),
                            ],
                        render_kw={'id':"date",'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
        )
    heureD = TimeField(label="Heure début",
                        validators=[
                            DataRequired("Veuillez choisir l'heure de début de la séance"),
                            ],
                        render_kw={'id':"heureD",'disabled':True, 'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
        )
    heureF = TimeField(label="Heure fin",
                        validators=[
                            DataRequired("Veuillez choisir l'heure de fin de la séance"),
                            ],
                        render_kw={'id':"heureF",'disabled':True,'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
        )
    code = StringField("Code session",
                          render_kw={'id':"code",'disabled':True,'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    salle = SelectField(label="Salle",
                        render_kw={'id':"salle",'disabled':True,'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    professeur = SelectField(label="Professeur",
                        render_kw={'id':"professeur",'disabled':True,'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'id':'submit','disabled':True,'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})

            
            
