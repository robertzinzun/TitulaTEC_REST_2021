from flask import Flask,request
from Dao import Opcion, db, Solicitud, Alumno, Usuario

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://titulatec_soa:Hola.123@localhost:3306/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def inicio():
    return 'Escuchando servicios REST de TitulaTEC'

@app.route('/alumnos',methods=['post'])
def alumnos():
    ojson=request.get_json()
    a=Alumno()
    return a.agregar(ojson)

@app.route('/alumnos/autenticar',methods=['get'])
def alumno():
    datos=request.get_json()
    u=Usuario()
    salida=u.autenticar(datos['email'],datos['password'])
    if salida['estatus']=='Ok':
        a=Alumno()
        usuario=salida['usuario']
        if usuario['tipo']=='E':
            salida=a.consultarPorIdUsuario(usuario['id'])
    return salida

#seccion de solicitudes
@app.route('/solicitudes',methods=['GET'])
def solicitudes():
    s=Solicitud()
    return s.consultaGeneral()
@app.route('/solicitudes',methods=['POST'])
def agregarSolicitud():
    json=request.get_json()
    s = Solicitud()
    salida=s.agregar(json)
    return salida

@app.route('/solicitudes',methods=['PUT'])
def editarSolicitud():
    json=request.get_json()
    s = Solicitud()
    salida=s.modificar(json)
    return salida

@app.route('/solicitudes/<int:id>',methods=['DELETE'])
def eliminarSolicitud(id):
    s = Solicitud()
    salida=s.eliminar(id)
    return salida

@app.route('/solicitudes/<int:id>',methods=['GET'])
def consultarSolicitud(id):
    s=Solicitud()
    return s.consultaIndividual(id)

@app.route('/solicitudes/alumno/<int:id>',methods=['GET'])
def consultarSolicitudesAlumno(id):
    s = Solicitud()
    return s.consultaPorAlumno(id)
#fin de seccion de solicitudes

#Seccion del servicios de opciones
@app.route('/opciones', methods=['GET'])
def opciones():
    o=Opcion()
    lista=o.consultaGeneral()
    return lista

@app.route('/opciones/<int:id>',methods=['GET'])
def opcion(id):
    o=Opcion()
    return o.consultaIndividual(id)

@app.route('/opciones',methods=['POST'])
def registroOpcion():
    ojson=request.get_json()
    o=Opcion()
    salida=o.insertar(ojson)
    return salida

@app.route('/opciones',methods=['PUT'])
def modificarOpcion():
    opcion=request.get_json()
    o=Opcion()
    salida=o.modificar(opcion)
    return salida

@app.route('/opciones/<int:id>',methods=['DELETE'])
def eliminarOpcion(id):
    o=Opcion()
    salida=o.eliminar(id)
    return salida

#fin de la sección del servicio de opciones

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0',port=8000)