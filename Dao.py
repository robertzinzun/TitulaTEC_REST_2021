from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, INTEGER, String, Date, ForeignKey, text, values
from sqlalchemy.orm import relationship
import datetime

import json
from flask import jsonify

db=SQLAlchemy()

class Opcion(db.Model):
    __tablename__='Opciones'
    idOpcion=Column(INTEGER,primary_key=True)
    nombre=Column(String(80),unique=True)
    descripcion=Column(String(200),nullable=True)
    estatus=Column(String(1),default='A')
    def consultaGeneral(self):
        dict_json = {"estatus": "", "mensaje": "", "opciones": []}
        try:
            dict_json['estatus'] = "Ok"
            lista = self.query.all()
            if len(lista)>0:
                dict_json['mensaje'] = "Listado de opciones"
                dict_json['opciones'] = self.to_json_list(lista)
            else:
                dict_json['mensaje'] = "No hay opciones registradas"
        except:
            dict_json['estatus'] = "Error"
            dict_json['mensaje'] = "Error al ejecutar la consulta de opciones"

        return json.dumps(dict_json)

    def to_json_list(self, lista):
        lista_opciones = []
        for o in lista:
            lista_opciones.append(self.to_json(o))

        return lista_opciones

    def consultaIndividual(self,id):
        dict_json = {"estatus": "", "mensaje": "", "opcion":{}}
        try:
            dict_json['estatus'] = "Ok"
            dict_json['mensaje'] = "Listado de la opcion"
            dict_json['opcion'] = self.to_json(self.query.get(id))
        except:
            dict_json['estatus'] = "Error"
            dict_json['mensaje'] = "Error al ejecutar la consulta de la opcion"

        return json.dumps(dict_json)

    def to_json(self,o):
        opcion = {"idOpcion": o.idOpcion, "nombre": o.nombre, "descripcion": o.descripcion}
        return opcion

    def insertar(self,json):
        dict_salida={"estatus":"","mensaje":""}
        try:
            self.from_json(json)
            db.session.add(self)
            db.session.commit()
            dict_salida['estatus']='Ok'
            dict_salida["mensaje"]='Opcion registrada con exito'
        except:
            db.session.rollback()
            dict_salida['estatus'] = 'Error'
            dict_salida["mensaje"] = 'Error al registrar la Opcion'
        return  jsonify(dict_salida)

    def from_json(self,o):
        if o.get("idOpcion")!=None:
            self.idOpcion=o['idOpcion']
        self.nombre=o['nombre']
        self.descripcion=o['descripcion']

    def modificar(self,json):
        dict_salida = {"estatus": "", "mensaje": ""}
        try:
            self.from_json(json)
            db.session.merge(self)
            db.session.commit()
            dict_salida['estatus'] = 'Ok'
            dict_salida["mensaje"] = 'Opcion modificada con exito'
        except:
            db.session.rollback()
            dict_salida['estatus'] = 'Error'
            dict_salida["mensaje"] = 'Error al modificar la Opcion'
        return jsonify(dict_salida)
    def eliminar(self,id):
        #db.session.delete(self.query.get(id))
        dict_salida = {"estatus": "", "mensaje": ""}
        try:
            self=self.query.get(id)
            self.estatus='I'
            db.session.merge(self)
            db.session.commit()
            dict_salida['estatus'] = 'Ok'
            dict_salida["mensaje"] = 'Opcion eliminada con exito'
        except:
            db.session.rollback()
            dict_salida['estatus'] = 'Error'
            dict_salida["mensaje"] = 'Error al eliminar la Opcion'
        return jsonify(dict_salida)
class Carrera(db.Model):
    __tablename__='Carreras'
    idCarrera=Column(INTEGER,primary_key=True)
    idAdministrativo=Column(INTEGER,ForeignKey('Administrativos.idAdministrativo'))
    nombre=Column(String(100),nullable=False)
    siglas=Column(String(20),nullable=False)
    creditos=Column(INTEGER,nullable=False)
    planEstudios=Column(String(20),nullable=False)
    especialidad=Column(String(80),nullable=False)
    estatus=Column(String,nullable=False)

class Usuario(db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(INTEGER,primary_key=True)
    nombre=Column(String(100),nullable=False)
    sexo=Column(String,nullable=False)
    telefono=Column(String(12),nullable=False)
    email=Column(String(100),unique=True)
    password=Column(String(20),nullable=False)
    tipo=Column(String,nullable=False,default='E')
    estatus=Column(String,nullable=False,default=True)

class Alumno(db.Model):
    __tablename__='Alumnos'
    idAlumno=Column(INTEGER,primary_key=True)
    noControl=Column(String(9),unique=True)
    anioEgreso=Column(INTEGER,nullable=False)
    creditos=Column(INTEGER,nullable=False)
    estatus=Column(String,nullable=False,default=True)
    idUsuario=Column(INTEGER,ForeignKey('Usuarios.idUsuario'))
    idCarrera=Column(INTEGER,ForeignKey('Carreras.idCarrera'))
    usuario=relationship(Usuario,lazy='select')
    carrera=relationship(Carrera,lazy='select')

    def consultaGeneral(self):
        return self.query.all()
    def agregar(self,ojson):
        dict_salida = {"estatus": "", "mensaje": ""}
        #try:
        self.from_json(ojson)
        db.session.add(self.usuario)
        db.session.add(self)
        db.session.commit()
        dict_salida['estatus'] = 'Ok'
        dict_salida["mensaje"] = 'Alumno registrado con exito'
        #except:
        #    db.session.rollback()
        #    dict_salida['estatus'] = 'Error'
        #    dict_salida["mensaje"] = 'Error al registrar al alumno'
        return jsonify(dict_salida)


    def from_json(self,ojson):
        usuario=Usuario()
        usuario.nombre=ojson['nombre']
        usuario.sexo = ojson['sexo']
        usuario.telefono = ojson['telefono']
        usuario.email = ojson['email']
        usuario.password = ojson['password']
        self.usuario=usuario
        self.noControl=ojson['nocontrol']
        self.anioEgreso=ojson['anioEgreso']
        self.creditos=ojson['creditos']
        self.idCarrera = ojson['idCarrera']



class Administrativo(db.Model):
    __tablename__='Administrativos'
    idAdministrativo=Column(INTEGER,primary_key=True)
    noEmpleado=Column(INTEGER,nullable=False)
    estatus=Column(String,nullable=False)
    idUsuario=Column(INTEGER,ForeignKey('Usuarios.idUsuario'))
    idPuesto=Column(INTEGER,ForeignKey('Puestos.idPuesto'))
    idDepartamento=Column(INTEGER,ForeignKey('Departamentos.idDepartamento'))
    usuario = relationship(Usuario, lazy='select')

class Solicitud(db.Model):
    __tablename__='Solicitudes'
    idSolicitud=Column(INTEGER,primary_key=True)
    fechaRegistro=Column(Date,default=datetime.date.today())
    fechaAtencion=Column(Date,nullable=True)
    tituloProyecto=Column(String(300),nullable=False)
    estatus=Column(String,nullable=False,default='P')
    idOpcion=Column(INTEGER,ForeignKey('Opciones.idOpcion'))
    idAdministrativo = Column(INTEGER, ForeignKey('Administrativos.idAdministrativo'))
    idAlumno = Column(INTEGER, ForeignKey('Alumnos.idAlumno'))
    opcion=relationship(Opcion,backref='solicitudes',lazy='select')
    alumno=relationship(Alumno,lazy='select')
    administrativo=relationship(Administrativo,lazy='select')
    def consultaGeneral(self):
        resp_json = {"estatus":"","mensaje":"","solicitudes":[]}
        try:
            lista=self.query.all()
            resp_json['estatus']='Ok'
            resp_json['mensaje']='Listado de solicitudes'
            lista_json=[]
            for s in lista:
                lista_json.append(self.toJson(s))
            resp_json['solicitudes']=lista_json
        except:
            resp_json['estatus'] = 'Error'
            resp_json['mensaje'] = 'Error al consultar las solicitudes'
        return jsonify(resp_json)

    def toJson(self,o):
        dict_solicitud = {"id": o.idSolicitud, "proyecto": o.tituloProyecto,"fechaRegistro":o.fechaRegistro,
                          "fechaAtencion":o.fechaAtencion,"estatus":o.estatus,
                          "opcion":{"id":o.opcion.idOpcion,"nombre":o.opcion.nombre},
                          "alumno":{"NC":o.alumno.noControl,"nombre":o.alumno.usuario.nombre},
                          "administrativo":{"id":o.administrativo.idAdministrativo,"nombre":o.administrativo.usuario.nombre},
                          "carrera":{"id":o.alumno.carrera.idCarrera,"nombre":o.alumno.carrera.nombre}
                          }
        return dict_solicitud

    def agregar(self,data):
        salida={"estatus":"","mensaje":""}
        try:
            db.session.execute('call sp_registrar_solicitud(:tituloProyecto,:opcion,:alumno,@p_estatus,@p_mensaje)',data)
            s=db.session.execute('select @p_estatus,@p_mensaje').fetchone()
            db.session.commit()
            salida['estatus']=s[0]
            salida['mensaje']=s[1]
        except:
            salida['estatus'] = 'Error'
            salida['mensaje'] = 'Error al agregar la solicitud'
        return jsonify(salida)

    def consultaIndividual(self,id):
        resp_json={"estatus":"","mensaje":""}
        try:
            resp_json['estatus']='Ok'
            resp_json['mensaje']='Listado de la solicitud'
            resp_json['solicitud']=self.toJson(self.query.get(id))
        except:
            resp_json['estatus']='Error'
            resp_json['mensaje']='Error al consultar la solicitud con id:'+str(id)
        return jsonify(resp_json)

    def modificar(self,data):
        salida = {"estatus": "", "mensaje": ""}
        try:
            db.session.execute('call sp_modificar_solicitud(:idSolicitud,:tituloProyecto,:estatus,:opcion,:administrativo,:tipoUsuario,@p_estatus,@p_mensaje)', data)
            s = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
            db.session.commit()
            salida['estatus'] = s[0]
            salida['mensaje'] = s[1]
        except:
            salida['estatus'] = 'Error'
            salida['mensaje'] = 'Error al modificar la solicitud'
        return jsonify(salida)

    def eliminar(self,id):
        data={"idSolicitud":id}
        salida = {"estatus": "", "mensaje": ""}
        try:
            db.session.execute('call sp_eliminar_solicitud(:idSolicitud,@p_estatus,@p_mensaje)', data)
            s = db.session.execute('select @p_estatus,@p_mensaje').fetchone()
            db.session.commit()
            salida['estatus'] = s[0]
            salida['mensaje'] = s[1]
        except:
            salida['estatus'] = 'Error'
            salida['mensaje'] = 'Error al eliminar la solicitud'
        return jsonify(salida)
