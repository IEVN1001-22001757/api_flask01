from flask import Flask, render_template, request
import math
import forms
from flask import make_response, jsonify
import json




app = Flask(__name__)

@app.route('/')
def home():
    return  'hOLA' #redirect(url_for('resultadoD'))

@app.route("/index")
def index():
    titulo="IEVN1001"
    listado=["Python", "Flask", "HTML", "CSS", "JavaScript"]
    return render_template('index.html', titulo=titulo, listado=listado)

@app.route("/aporb")
def aporb():
    return render_template('aporb.html')

@app.route("/resultado", methods=['POST'])
def resultado():
    n1=request.form.get("a")
    n2=request.form.get("b")
    return "La multiplicacion de {} y {} es {}".format(n1, n2, int(n1)*int(n2))

@app.route("/distancia", methods=['POST', 'GET'])
def distancia():
    X1 = float(request.form.get("x1", 0))
    Y1 = float(request.form.get("y1", 0))
    X2 = float(request.form.get("x2", 0))
    Y2 = float(request.form.get("y2", 0))

    res=math.sqrt(((X2-X1)**2) + ((Y2-Y1)**2))
    
    return render_template('distancia.html', res=res)
    
@app.route("/hola")
def func():
    return "<h1>Hola tq :c</h1>"

@app.route("/adios/<string:user>")
def user(user):
    return "<h1>Adios {} :c</h1>".format(user)

@app.route("/square/<int:num>")
def square(num):
    return "<h1> El cuadrado de {} is {}".format(num, num**2)

@app.route("/repeat/<string:text>/<int:times>")
def repeat(text, times):
    return "<h1>" + " ".join([text] * times) + "</h1>"

@app.route('/suma/<float:a>/<float:b>')
def suma(a,b):
    return "<h1>La suma de {} y {} es {} </h1>".format(a, b, a+b)

@app.route("/figuras", methods=['POST', 'GET'])
def figuras():

    resultado = 0
    area_seleccinada= request.form.get("area")

    if area_seleccinada == "cuadrado":
        lado= float(request.form.get("lado",0))
        resultado= lado*lado
    
    elif area_seleccinada == "triangulo":
        base= float(request.form.get("base",0))
        altura = float(request.form.get("altura",0))
        resultado = (base*altura)/2
    
    elif area_seleccinada == "circulo":
        radio = float(request.form.get("radio",0))
        resultado= math.pi * (radio ** 2)
    
    elif area_seleccinada == "rectangulo":
        base= float(request.form.get("base",0))
        altura = float(request.form.get("altura",0))
        resultado = base*altura

    elif area_seleccinada == "pentagono":
        lado= float(request.form.get("lado",0))
        apotema = float(request.form.get("apotema", 0))
        resultado= (5 * lado * (2*math.tan(math.radians(30))))/2

    return  render_template('figuras.html', resultado=resultado, area=area_seleccinada)

@app.route("/alumnos", methods=['POST', 'GET'])
def alumnos():
    mat=0
    nom=''
    apell=''
    email=''
    estudiantes=[]
    datos={}

    alumno_class=forms.UserForm(request.form)
    if request.method=='POST' and alumno_class.validate():
        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('alumnos.html',))
            response.delete_cookie('usuario')


        mat=alumno_class.matricula.data
        nom=alumno_class.nombre.data
        apell=alumno_class.apellido.data
        email=alumno_class.email.data

        datos={'matricula':mat, 'nombre':nom.strip(), 'apellido':apell.rstrip(), 'email':email.strip()}

        data_str=request.cookies.get("usuario")

        if not data_str:
            return "No hay cookie guardada", 404
        
        estudiantes=json.loads(data_str)
        estudiantes.append(datos)
    response=make_response(render_template('alumnos.html', form=alumno_class, mat=mat, nom=nom, apell=apell, email=email))

    if request.method!='GET':
        response.set_cookie('usuario', json.dumps(estudiantes))

    return response
    #return render_template('alumnos.html', form=alumno_class, mat=mat, nom=nom, apell=apell, email=email)

@app.route("/get_cookie")
def get_cookie():
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No hay cookie guardada", 404
    
    estudiantes=json.loads(data_str)
    return jsonify(estudiantes)





























if __name__ == '__main__':
    app.run(debug=True)