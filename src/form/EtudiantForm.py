
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, BooleanField, FileField, EmailField,PasswordField
from wtforms.validators import DataRequired, Length, Email, InputRequired,  ValidationError
from werkzeug.utils import secure_filename

# Liste des extensions d'image autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class EtudiantForm(FlaskForm):

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
    tuteur = StringField("Tuteur",
                          validators=[
                              InputRequired("Le nom complet du tuteur est requis"), 
                              Length(min=5, message="minimum {min} caractères pour le nom complet du tuteur")
                           ],
                          render_kw={'class':'w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'}
            )
    photo = FileField(label="Photo",
                        render_kw={'class':"w-full px-4 h-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}
                )
    def validate_photo(self, field):
        if field.data.filename != '' and not self.is_extension_allowed(field.data.filename):
            raise ValidationError('Seules les images avec les extensions suivantes sont autorisées: png, jpg, jpeg')

    def is_extension_allowed(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    isArchived = BooleanField(label=('Archivé'), render_kw={'class':"rounded mt-1 w-3.5 h-3.5 mr-3" })
    submit = SubmitField(label=('Enregistrer'), 
                         render_kw={'class' : "px-4 cursor-pointer py-2 text-sm font-medium leading-5 text-red-600 transition-colors duration-150 bg-transparent border border-red-600 rounded-lg hover:text-white hover:bg-red-600 focus:outline-none focus:shadow-outline-red"})
