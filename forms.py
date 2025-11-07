from flask_wtf import FlaskForm
from wtforms import EmailField, Form, StringField, IntegerField, BooleanField, PasswordField, validators, RadioField, SelectMultipleField, SubmitField
from datetime import date

class UserForm(Form):
    matricula = IntegerField('Matricula', [validators.DataRequired()])
    nombre = StringField('Nombre', [validators.DataRequired(), validators.length(min=1, max=50)])
    apellido = StringField('Apellido', [validators.DataRequired(), validators.length(min=1, max=50)])
    email = EmailField('email', [validators.Email(message='Ingrese un correo valido')])

class PedidoForm(Form):
    # --- DATOS DEL CLIENTE (Tomados de la antigua ClienteForm) ---
    nombre = StringField('Nombre completo', [validators.DataRequired()])
    direccion = StringField('Dirección', [validators.DataRequired()])
    telefono = StringField('Teléfono', [validators.DataRequired(), validators.length(min=7, max=15, message='Teléfono inválido')])

    # --- DATOS DE LA PIZZA (Tomados de la antigua PizzaForm) ---
    tamanio = RadioField(
        'Tamaño Pizza',
        choices=[
            ('Chica', 'Chica $40'),
            ('Mediana', 'Mediana $80'),
            ('Grande', 'Grande $120')
        ],
        validators=[validators.DataRequired()]
    )
    

    # Número de Pizzas (IntegerField)
    num_pizzas = IntegerField('Núm. de Pizzas', [
        validators.DataRequired(), 
        validators.NumberRange(min=1, message='Debe ser al menos 1 pizza')
    ])
    
    # Botones
    agregar = SubmitField('Agregar') # Botón para agregar a la tabla
    terminar = SubmitField('Terminar') # Botón para calcular y guardar venta
    quitar = SubmitField('Quitar') # Botón para eliminar item de la tabla