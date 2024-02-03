from tkinter import Tk
from vista import Ventana
import vista
import observador


class Controller:
    def __init__(self, master):
        self.master_controller = master
        self.objeto_vista = vista.Ventana(self.master_controller)
        self.el_observador = observador.ConcreteObserverA(self.objeto_vista.objeto_base)


if __name__ == "__main__":
    master_tk = Tk()
    application = Controller(master_tk)
    application.objeto_vista.actualizar()
    master_tk.mainloop()
