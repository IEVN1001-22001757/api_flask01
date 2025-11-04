from wtforms import EmailField, Form, StringField, IntegerField, BooleanField, PasswordField, validators

class UserForm(Form):
    matricula = IntegerField('Matricula', [validators.DataRequired()])
    nombre = StringField('Nombre', [validators.DataRequired(), validators.length(min=1, max=50)])
    apellido = StringField('Apellido', [validators.DataRequired(), validators.length(min=1, max=50)])
    email = EmailField('email', [validators.Email(message='Ingrese un correo valido')])

