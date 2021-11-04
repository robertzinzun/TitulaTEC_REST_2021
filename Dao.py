from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,INTEGER,String,Date,ForeignKey,text
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
            dict_salida['estatus']='ok'
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
            dict_salida['estatus'] = 'ok'
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
            dict_salida['estatus'] = 'ok'
            dict_salida["mensaje"] = 'Opcion eliminada con exito'
        except:
            db.session.rollback()
            dict_salida['estatus'] = 'Error'
            dict_salida["mensaje"] = 'Error al eliminar la Opcion'
        return jsonify(dict_salida)
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
    Opcion=relationship(Opcion,backref='solicitudes',lazy='select')

    def consultaGeneral(self):
        dict_solicitud={"idSolicitud":"","tituloProyecto":""}
        return self.query.all()
    def agregar(self):
        data={"titulo":'Prueba final 3',"opcion":1,"alumno":1}
        db.session.execute('call sp_registrar_solicitud(:titulo,:opcion,:alumno,@estatus,@mensaje)',data)
        s=db.session.execute('select @estatus,@mensaje').fetchone()
        print(s)
        db.session.commit()

