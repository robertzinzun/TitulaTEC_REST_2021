from flask import Flask,request,jsonify
import json
from Dao import Opcion,db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://titulatec_soa:Hola.123@localhost:3306/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def inicio():
    return 'Escuchando el servicio REST de Opciones'

@app.route('/alumnos')
def productos():
    return 'Alumnos'

@app.route('/alumnos/<string:nc>')
def alumno(nc):
    return 'alumno con numero de control:'+nc

@app.route('/solicitudes')
def solicitudes():
    return 'Solicitudes'
#Seccion del servicios de opciones
@app.route('/opciones', methods=['GET'])
def opciones():
    o=Opcion()
    lista=o.consultaGeneral()
    print(lista)
    return lista

@app.route('/opciones/<int:id>',methods=['GET'])
def opcion(id):
    #opcion={"estatus":"ok","mensaje":"Listado de opciones","opcion":{"idOpcion":id,"nombre":"Tesis","descripcion":"Informe de Tesis"}}
    o=Opcion()
    return o.consultaIndividual(id)

@app.route('/opciones',methods=['POST'])
def registroOpcion():
    ojson=request.get_json()
    o=Opcion()
    o.insertar(ojson)
    salida={"estatus":"ok","mensaje":"Opcion registrada con exito"}
    return json.dumps(salida)

@app.route('/opciones',methods=['PUT'])
def modificarOpcion():
    opcion=request.get_json()
    salida = {"estatus": "ok", "mensaje": "Opcion modificada con exito"}
    return jsonify(salida)

@app.route('/opciones/<int:id>',methods=['DELETE'])
def eliminarOpcion(id):
    salida = {"estatus": "ok", "mensaje": "Opcion con id: "+str(id)+" eliminada con exito"}
    return jsonify(salida)

#fin de la sección del servicio de opciones

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0',port=5000)