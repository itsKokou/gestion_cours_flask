
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired, NumberRange
from datetime import datetime
annees = [("","")]
annees.extend([(str(year), str(year)) for year in range(datetime.now().year, datetime.now().year+5)])
    

class AnneeScolaireForm(FlaskForm):
    debut = SelectField(label="Année de début",
                        choices= annees,
                        validators=[DataRequired("Veuillez choisir une année")],
                        render_kw={'id':"debut", 'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    libelle = StringField("Libelle",
                          render_kw={'id':"libelle",'readonly': True, 'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
                )
    isActive = BooleanField(label=('Actuelle'), render_kw={'class':"rounded mt-1 w-3.5 h-3.5 mr-3" })
    isArchived = BooleanField(label=('Archivé'), render_kw={'class':"rounded mt-1 w-3.5 h-3.5 mr-3" })
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"}
                )

