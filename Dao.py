from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,INTEGER,String
import json

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
            dict_json['opcion'] = self.query.get(id).to_json()
        except:
            dict_json['estatus'] = "Error"
            dict_json['mensaje'] = "Error al ejecutar la consulta de la opcion"

        return json.dumps(dict_json)

    def to_json(self):
        opcion = {"idOpcion": self.idOpcion, "nombre": self.nombre, "descripcion": self.descripcion}
        return opcion

    def insertar(self,json):
        self.from_json(json)
        db.session.add(self)
        db.session.commit()

    def from_json(self,o):
        #self.idOpcion=o['idOpcion']
        self.nombre=o['nombre']
        self.descripcion=o['descripcion']