from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField ,RadioField ,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,InputRequired
from ecert.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nom D\'Utilisateur',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    confirm_password = PasswordField('Valider Mot de Passe',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Inscription')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    remember = BooleanField('Se Souvient De Moi')
    submit = SubmitField('Connexion')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nom D\'Utilisateur',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Modifier photo de profile', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Modifier')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Nom D\'Utilisateur existe deja.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email existe deja.')
class SurveyForm(FlaskForm):

    critere1 =RadioField('Quelle était votre impression globale de notre nouveau service :',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
    
    critere2= RadioField('Facilité d’accès :',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere3 = RadioField('Facilité d’accès:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere4 = RadioField('Rapidité de prise en compte de votre demande:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere5 = RadioField('Les délais de livraison du certificat:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere6 = RadioField('Facilité de l’utilisation du certificat électronique:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere7 = RadioField('La sécurité de vos données en utilisant le certificat électronique sur token:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere8 = RadioField('Facilité de contact du service client:',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere9 = RadioField('Rapidité des réponses (e-mail, tél):',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
                    
    critere10 = RadioField('Professionnalisme de votre interlocuteur (patient, enthousiaste, à l’écoute, réactif, amical, courtois…):',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
    critere11 = RadioField('Quelle est votre impression sur l’authentification avec (login+Mot de passe+ Certificat sur token)  contre l’authentification avec (login+Mot de passe) seulement ?',
                    choices=[(4,'Très satisfait'),(3,'Satisfait'),(2,'Peu Satisfait'),(1,'Non Satisfait')],
                    validators=[InputRequired()])
    opinion = TextAreaField('Merci de nous dire ce que nous pourrions améliorer :', validators=[DataRequired()])
    submit = SubmitField('Submit')

    
