from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

class DeclarationForm(FlaskForm):
    motif = StringField("Motif",
                          validators=[
                              InputRequired("Le motif est requis"), 
                              Length(min=5, message="minimum {min} caractères pour le motif")
                           ],
                          render_kw={'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    description = TextAreaField("Description",
                          validators=[
                              InputRequired("La description est requise"), 
                              Length(min=10, message="minimum {min} caractères pour le motif")
                           ],
                          render_kw={'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    submit = SubmitField(label=('Enregistrer'), render_kw={'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})