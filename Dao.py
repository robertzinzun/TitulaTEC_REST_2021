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

            dict_json=self.to_json_list(self.query.all())

        except:
            dict_json['estatus']="Error"
            dict_json['mensaje']="Error al ejecutar la consulta de opciones"

        return json.dumps(dict_json)

    def to_json_list(self,lista):
        dict_json = {"estatus": "ok", "mensaje": "Listado de Opciones", "opciones": []}
        lista_opciones=[]
        for o in lista:
            dict_opcion={"idOpcion":o.idOpcion,"nombre":o.nombre,"descripcion":o.descripcion}
            lista_opciones.append(dict_opcion)
        dict_json['opciones']=lista_opciones
        if len(lista_opciones)==0:
            dict_json['mensaje']='No hay opciones registradas'
        return dict_json

    def consultaIndividual(self,id):
        dict_json = {"estatus": "", "mensaje": "", "opcion":{}}
        try:
            dict_json = self.to_json(self.query.get(id))
        except:
            dict_json['estatus'] = "Error"
            dict_json['mensaje'] = "Error al ejecutar la consulta de la opcion"

        return json.dumps(dict_json)

    def to_json(self,o):
        dict_json = {"estatus": "ok", "mensaje": "Listado de la opcion", "opcion": {}}
        opcion = {"idOpcion": o.idOpcion, "nombre": o.nombre, "descripcion": o.descripcion}
        dict_json['opcion']=opcion
        return dict_json
    def insertar(self,json):
        self.from_json(json)
        db.session.add(self)
        db.session.commit()

    def from_json(self,o):
        #self.idOpcion=o['idOpcion']
        self.nombre=o['nombre']
        self.descripcion=o['descripcion']