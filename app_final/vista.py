from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import ttk
from tkcalendar import Calendar

# from tkinter import END
from tkinter.messagebox import showinfo

# from tkinter import *
# from modelo import alta
# from modelo import actualizar
# from modelo import borrar
# from modelo import conexion
# from modelo import crear_tabla

from modelo import Abmc
import os

# ####################################################
# VISTA
# ###################################################
class RegistroLogError(Exception):

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log.txt")

    def __init__(self, nombrelog, especialidadlog, sedelog, fecha):
        self.nombrelog = nombrelog
        self.especialidadlog = especialidadlog
        self.sedelog = sedelog
        self.fecha = fecha

    def registrar_error(self):
        log = open(self.ruta, "a")
        print(
            "Se ha dado un error:",
            self.nombrelog,
            self.especialidadlog,
            self.sedelog,
            self.fecha,
            file=log,
        )


class Ventana:
    def __init__(self, windows):
        self.objeto_base = Abmc()
        self.master = windows
        self.master.geometry("900x9000")
        self.master.title("Gestion de Turnos")
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=6)
        self.titulo = Label(
            self.master,
            text="Gestion de turnos médicos",
            bg="pink1",
            fg="ivory1",
            height=2,
            width=80,
        )
        self.titulo.grid(row=0, column=0, columnspan=5, padx=1, pady=1, sticky="w")

        self.nombre = Label(self.master, text="Nombre del Paciente")
        self.nombre.grid(row=1, column=0, sticky="w")
        self.especialidad = Label(self.master, text="Especialidad")
        self.especialidad.grid(row=2, column=0, sticky="w")
        self.sede = Label(self.master, text="Sede")
        self.sede.grid(row=3, column=0, sticky="w")
        self.fecha = Label(self.master, text="Fecha")
        self.fecha.grid(row=1, column=2, sticky="w")
        self.hora = Label(self.master, text="Hora")
        self.hora.grid(row=2, column=2, sticky="w")

        self.cal = Calendar(self.master, selectmode="day", year=2023, month=7, day=22)
        self.cal.grid(
            row=1,
            column=4,
            rowspan=5,
            padx=2,
            pady=2,
        )

        # Defino variables para tomar valores de campos de entrada

        self.a_val, self.b_val, self.c_val, self.d_val, self.e_val = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )
        w_ancho = 20
        w_ancho2 = 10

        self.entry_nombre = Entry(self.master, textvariable=self.a_val, width=w_ancho)
        self.entry_nombre.grid(row=1, column=1, sticky="w")
        self.entry_especialidad = Entry(
            self.master, textvariable=self.b_val, width=w_ancho
        )
        self.entry_especialidad.grid(row=2, column=1, sticky="w")
        self.entry_sede = Entry(self.master, textvariable=self.c_val, width=w_ancho)
        self.entry_sede.grid(row=3, column=1, sticky="w")
        self.entry_fecha = Entry(self.master, textvariable=self.d_val, width=w_ancho2)
        self.entry_fecha.grid(row=1, column=3, sticky="w")
        self.entry_hora = Entry(self.master, textvariable=self.e_val, width=w_ancho2)
        self.entry_hora.grid(row=2, column=3, sticky="w")

        # --------------------------------------------------
        # TREEVIEW
        # --------------------------------------------------
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.column("#0", width=90, minwidth=50, anchor="w")
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=90, minwidth=50)
        self.tree.column("col5", width=90, minwidth=50)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Paciente")
        self.tree.heading("col2", text="Especialidad")
        self.tree.heading("col3", text="Sede")
        self.tree.heading("col4", text="Fecha")
        self.tree.heading("col5", text="Hora")
        self.tree.grid(row=10, column=0, columnspan=5)

        self.boton_alta = Button(
            self.master,
            text="Alta",
            command=lambda: self.vista_alta(),
            height=1,
            width=8,
            bg="PaleGreen1",
            activebackground="SpringGreen2",
        )

        self.boton_alta.grid(row=2, column=4, padx=2, pady=2, sticky="w")

        self.boton_actualizar = Button(
            self.master,
            text="Actualizar",
            command=lambda: self.vista_actualizar(),
            height=1,
            width=8,
            activebackground="RoyalBlue1",
        )

        self.boton_actualizar.grid(row=3, column=4, padx=2, pady=2, sticky="w")

        self.boton_borrar = Button(
            self.master,
            text="Borrar",
            command=lambda: self.vista_borrar(self.tree),
            height=1,
            width=8,
            activebackground="red",
        )

        self.boton_borrar.grid(row=4, column=4, padx=2, pady=2, sticky="w")

        self.boton_fecha = Button(
            self.master,
            text="Fecha",
            command=lambda: self.grad_date(),
            height=1,
            width=8,
            activebackground="SpringGreen2",
        )
        self.boton_fecha.grid(row=4, column=3, padx=2, pady=2, sticky="w")

    def grad_date(
        self,
    ):
        self.entry_fecha.insert(0, self.cal.get_date())

    def vista_alta(
        self,
    ):
        retorno = self.objeto_base.alta(
            self.a_val, self.b_val, self.c_val, self.d_val, self.e_val, self.tree
        )
        print(retorno)
        # self.limpiar
        showinfo("El alta de registro ha sido confirmada", retorno[0])

    def vista_borrar(self, tree):
        retorno = self.objeto_base.borrar(tree)
        showinfo("El registro ha sido eliminado", retorno[0])

    def vista_actualizar(
        self,
    ):
        retorno = self.objeto_base.actualizar(
            self.a_val,
            self.b_val,
            self.c_val,
            self.d_val,
            self.e_val,
            self.tree,
        )
        showinfo("Confirmación de actualizacion de registro", retorno[0])

    def actualizar(
        self,
    ):
        self.objeto_base.actualizar_treeview(self.tree)

    #    self.limpiar()

    # def limpiar(self,):
    #    self.entry_nombre.delete(0, END)
    #    self.entry_especialidad.delete(0, END)
    #    self.entry_sede.delete(0, END)
    #    self.entry_fecha.delete(0, END)
    #    self.entry_hora.delete(0, END)


# if __name__ == "__main__":
#    master = Tk()
#    obj1 = Ventana(master)
#    master.mainloop()
