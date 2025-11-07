from flask import Flask, render_template, request, make_response, redirect, url_for, flash, jsonify
import math
import forms
import json
from datetime import datetime 
from json.decoder import JSONDecodeError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin'

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











#PIZZERIA


#Creamos las variables globales de precio y tamaño que no cambiaran
PRECIOS_TAMANIO = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
PRECIO_INGREDIENTE = 10

@app.route('/pizeria', methods=['GET', 'POST'])
def pizeria():
    pedido_form = forms.PedidoForm(request.form) #creamos el formulario WTForms

    pedido = [] #inicializamos la lista donde guardaremos las cookies de los pedidos
    pedido_str = request.cookies.get('pedido_actual') #obtenemos las cookies guardadas del pedido


    #convertimos la cookie Json en una lista de Python si existe
    if pedido_str:
        try:
            pedido = json.loads(pedido_str)
        except JSONDecodeError:
            pedido = []

    total = sum(item['subtotal'] for item in pedido) #calculamos el total actual, cumando el campo subtotal de cada pizza en la lista pedido



    #declaracion de funcionamiento de los botones
    if request.method == 'POST':
        
        # ===== BOTÓN QUITAR =====
        if request.form.get('quitar') is not None: #valida que se precione el boton "quitar"
            items_a_quitar = request.form.getlist('item_to_remove')#Obtiene la lista de checkboxes que se desean eliminar

            if not items_a_quitar:
                return redirect(url_for('pizeria')) #si no se selecciona algun pedido solo se carga de nuevo la pagina sin hacer nada manteniendo las cookies actuales


            #aqui eliminamos cada cookie guardada en la lista para eliminar eliminando las posiciones desde el final al inicio recorriendo los indices y eliminandoos con .pop
            indices_a_eliminar = sorted([int(i) for i in items_a_quitar], reverse=True)
            for index in indices_a_eliminar:
                if 0 <= index < len(pedido):
                    pedido.pop(index)
            
            
            redirect_response = make_response(redirect(url_for('pizeria')))#creamos una respuesta que redirige a la pagina principal despues de eliminar
            redirect_response.set_cookie('pedido_actual', json.dumps(pedido))#volvemos a guardar la lista de pedidos que quedaron en formato json de la cookie para cuando actualizemos se conserven las cookies
            return redirect_response


        # ===== BOTÓN AGREGAR =====
        if request.form.get('agregar') is not None: #validamos que se precione "agregar"

            tamanio = pedido_form.tamanio.data #obtenemos el radioboton del tamaño elegido
            ingredientes_seleccionados = request.form.getlist('ingredientes') #obtenemos la lista de los ingredientes elegidos
            num_pizzas = pedido_form.num_pizzas.data #obtenemos el num de pizzas a comprar

            # Validamos que se seleccionen los datos de la pizza, si no mandamos un script de alert y cargamos la pagina de nuevo
            if not tamanio or not num_pizzas:
                return make_response("""<script>alert('Selecciona tamaño y número de pizzas'); window.location='/pizeria';</script>""")
            
            #calculamos el subtotal
            precio_base = PRECIOS_TAMANIO.get(tamanio, 0) #obtenemos del diccionario de precios por tamaño el valor elegido
            costo_ing = len(ingredientes_seleccionados) * PRECIO_INGREDIENTE
            subtotal = (precio_base + costo_ing) * num_pizzas

            #contruimos el pedido y lo agregamos a la lista
            item = {
                'tamanio': tamanio,
                'ingredientes': ', '.join(ingredientes_seleccionados) if ingredientes_seleccionados else 'Ninguno',
                'num_pizzas': num_pizzas,
                'subtotal': subtotal
            }
            pedido.append(item) #añade la pizza a la cookie de pedidos

            #redirigimos a la misma pagina y guardamos la cookie una tras otra
            redirect_response = make_response(redirect(url_for('pizeria')))
            redirect_response.set_cookie('pedido_actual', json.dumps(pedido))
            return redirect_response
                

        # ===== BOTÓN TERMINAR =====
        if request.form.get('terminar') is not None: #validamos que se precione "terminar"

            #si no hay oedidos agregados saltara una alerta para agregar alguna pizza
            if not pedido:
                return make_response("""<script>alert('El pedido está vacío'); window.location='/pizeria';</script>""")

            # Validamos que se llenen los formularios del cliente para agregar la infor a la cookie, si no se manda una alerta
            if not pedido_form.nombre.data or not pedido_form.direccion.data or not pedido_form.telefono.data:
                return make_response("""<script>alert('Completa los datos del cliente para finalizar'); window.location='/pizeria';</script>""")
            
            #recogemos los datos del cliente necesarios
            nombre = pedido_form.nombre.data
            direccion = pedido_form.direccion.data
            telefono = pedido_form.telefono.data
            fecha = datetime.now().strftime("%d-%m-%Y")

            # Guardamos en cookie_ventas
            ventas_str = request.cookies.get("cookie_ventas") #validamos que exista la cookie_ventas
            ventas = json.loads(ventas_str) if ventas_str else [] #creamos una lista llamada ventas 
            
            #agregamos las ventas actuales como diccionario guardando los datos del cliente y el total
            ventas.append({
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "fecha": fecha,
                "total": total
            })

            # Mensaje de confirmacion al dar terminar y cargamos la misma pagina
            js = f"""<script>alert("Pedido Completado\\nCliente: {nombre}\\nTotal a pagar: ${total:.2f}");window.location = '/pizeria';</script>"""
            resp = make_response(js)
            # Guardar cookies en la misma respuesta (max_age y samesite para que se vean en Chrome)
            resp.set_cookie("cookie_ventas", json.dumps(ventas), max_age=86400, samesite="Lax")
            resp.set_cookie("pedido_actual", json.dumps([]), max_age=86400, samesite="Lax")
            return resp

        
    # GET
    # Si la peticion no fue POST renderizamos el html de pizeria y enviamos al html las variables:
    return render_template("pizeria.html",
        pedido_form=pedido_form,
        pedido=pedido,
        total=total,
        fecha_actual=datetime.now().strftime('%d-%m-%Y'))


#en la pantalla de ventas por dia podemos eliminar las cookies guardadas en ventas_dia
@app.route('/limpiar_ventas')
def limpiar_ventas():
    response = make_response(redirect(url_for('ventas_dia')))
    response.delete_cookie('cookie_ventas')
    flash("Historial de ventas eliminado correctamente", "warning")
    return response

#mostramos las ventas del dia de los clientes que compraron
@app.route('/ventas_dia')
def ventas_dia():
    ventas_str = request.cookies.get('cookie_ventas')
    ventas = json.loads(ventas_str) if ventas_str else []

    total_acumulado = sum(v['total'] for v in ventas)

    return render_template('ventas_dia.html', ventas=ventas, total_acumulado=total_acumulado)
    
    





























if __name__ == '__main__':
    app.run(debug=True)