from flask import Flask,request,jsonify
import json


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
    opciones={"estatus":"ok","mensaje":"Listado de opciones","opciones":[{"idOpcion":1,"nombre":"Tesis","descripcion":"Informe de Tesis"}]}
    return json.dumps(opciones)

@app.route('/opciones/<int:id>',methods=['GET'])
def opcion(id):
    opcion={"estatus":"ok","mensaje":"Listado de opciones","opcion":{"idOpcion":id,"nombre":"Tesis","descripcion":"Informe de Tesis"}}
    return json.dumps(opcion)

@app.route('/opciones',methods=['POST'])
def registroOpcion():
    opcion=request.get_json()
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
    app.run(debug=True,host='0.0.0.0',port=5000)