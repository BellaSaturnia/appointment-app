import re

# import sqlite3
# from tkinter import END
from peewee import SqliteDatabase
from peewee import Model
from peewee import CharField
import os
import datetime
from tkinter.messagebox import showinfo
from observador import Sujeto

# En esta sección integro los decoradores


class RegistroLogDecoradores:
    """
    La clase RegistroLogError permite registrar los errores en
    el archivo log.txt mediante el uso de Excepciones.
    """

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log_deco.txt")

    def __init__(self, tipolog, nombrelog, especialidadlog, sedelog, fecha):
        self.tipolog = tipolog
        self.nombrelog = nombrelog
        self.especialidadlog = especialidadlog
        self.sedelog = sedelog
        self.fecha = fecha

    def registrar_evento(self):
        log_deco = open(self.ruta, "a")
        print(
            "Se ha generado un cambio:",
            self.tipolog,
            self.nombrelog,
            self.especialidadlog,
            self.sedelog,
            self.fecha,
            file=log_deco,
        )


def decorador_nuevo_registro(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = RegistroLogDecoradores(
            "Nueva Alta",
            "paciente:" + retorno[1],
            "especialidad:" + retorno[2],
            "sede:" + retorno[3],
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner


def decorador_actualizacion(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = RegistroLogDecoradores(
            "Registro Modificado",
            "paciente:" + retorno[1],
            "especialidad:" + retorno[2],
            "sede:" + retorno[3],
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner


def decorador_eliminar(f):
    def inner(*args):
        retorno = f(*args)
        log_deco = RegistroLogDecoradores(
            "Registro Eliminado",
            "paciente:" + retorno[1],
            "especialidad:" + retorno[2],
            "sede:" + retorno[3],
            datetime.datetime.now(),
        )
        log_deco.registrar_evento()
        return retorno

    return inner


# Este código es independiente de la base con la que me voy a manejar
db = SqliteDatabase("mibase4.db")


class BaseModel(Model):
    class Meta:
        database = db


class Pacientes(BaseModel):
    paciente = CharField()
    especialidad = CharField()
    sede = CharField()
    fecha = CharField()
    hora = CharField()


db.connect()
db.create_tables([Pacientes])


class Abmc(Sujeto):
    def __init__(
        self,
    ):
        pass

    @decorador_nuevo_registro
    def alta(self, paciente, especialidad, sede, fecha, hora, tree):
        datos_turno = Pacientes()
        datos_turno.paciente = paciente.get()
        cadena = datos_turno.paciente
        datos_turno.especialidad = especialidad.get()
        datos_turno.sede = sede.get()
        datos_turno.fecha = fecha.get()
        datos_turno.hora = hora.get()
        datos_turno.save()
        patron = "^[A-Za-z0-9]*$"  # regex para el campo paciente
        if re.match(patron, cadena):
            datos_turno.save()
            self.actualizar_treeview(tree)
            self.notificar(paciente.get(), especialidad.get(), sede.get())
            paciente = paciente.set("")
            especialidad = especialidad.set("")
            sede = sede.set("")
            fecha = fecha.set("")
            hora = hora.set("")
            return (
                "El alta fue realizada con exito",
                datos_turno.paciente,
                datos_turno.especialidad,
                datos_turno.sede,
            )
        else:
            return (
                "Error",
                datos_turno.paciente,
                datos_turno.especialidad,
                datos_turno.sede,
            )

    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        for fila in Pacientes.select():
            mitreview.insert(
                "",
                0,
                text=fila.id,
                values=(
                    fila.paciente,
                    fila.especialidad,
                    fila.sede,
                    fila.fecha,
                    fila.hora,
                ),
            )

    @decorador_eliminar
    def borrar(self, tree):
        valor = tree.selection()
        # print(valor)
        item = tree.item(valor)
        registro = item.get("values")
        borrar = Pacientes.get(Pacientes.id == item["text"])
        borrar.delete_instance()
        self.actualizar_treeview(tree)
        return (
            "Confirmación de registro eliminado",
            registro[0],
            registro[1],
            registro[2],
        )
        # print(item)  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
        # print(item["text"])
        # data = (mi_id,)
        # tree.delete(valor)

    @decorador_actualizacion
    def actualizar(self, paciente, especialidad, sede, fecha, hora, tree):
        valor = tree.selection()
        print(valor)
        item = tree.item(valor)
        registro = item.get("values")
        actualizar = Pacientes.update(
            paciente=paciente.get(),
            especialidad=especialidad.get(),
            sede=sede.get(),
            fecha=fecha.get(),
            hora=hora.get(),
        ).where(Pacientes.id == item["text"])
        actualizar.execute()
        # print(item)
        # print(item["text"])
        # mi_id = item["text"]
        self.actualizar_treeview(tree)
        return (
            "Modificacion realizada con exito",
            registro[0],
            registro[1],
            registro[2],
        )


# Acá intento integrar la excepción


class RegistroLogError(Exception):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(BASE_DIR, "log.text")

    # db_conn = sqlite3.connect("mibase4.db")
    # db_cursor = db_conn.cursor()
    # db_cursor.execute(Pacientes)

    def __init__(self, paciente, fecha, hora):
        self.paciente = paciente
        self.fecha = fecha
        self.hora = hora

    def registrar_error(self):
        log = open(self.ruta, "a")
        print("Se ha dado un error: ", self.paciente, self.fecha, self.hora, file=log)


def registrar():
    raise RegistroLogError("25", "archivo.txt", datetime.datetime.now())


try:
    registrar()
except RegistroLogError as log:
    log.registrar_error()
