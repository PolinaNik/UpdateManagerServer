from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo,showerror
from read_config import rc_osnov, rc_reserv
from textwrap import wrap

#TODO: разобраться с добавлением аргумента в класс из другого модуля
# TypeError: Tk.__init__() got an unexpected keyword argument 'hostnames'

class UpdateStatus(Tk):
    def __init__(self, hostnames, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Update Status")
        self.geometry("600x780")
        self.resizable(False, True)
        self.config(bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()
        self.hostnames = ''

    def create_widgets(self):
        self.create_panel_for_widget()


    def close(self):
        root.destroy()

    def create_panel_for_widget(self):
        # create panel frame
        self.panel = LabelFrame(self, text="Статус обновления", font=("Arial", 15), padx=5,
                                pady=5)
        self.panel.grid_rowconfigure(0, weight=1)
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.rowconfigure(0, weight=1)
        self.panel.columnconfigure(0, weight=1)
        self.panel.grid(row=0, column=0, sticky="news")

        # hostnames
        self.version_name_label = ttk.Label(self.panel, text=self.hostnames,
                                            font=("Arial", 13))
        self.version_name_label.grid(row=0, column=0, columnspan=2, sticky="news")


if __name__ == "__main__":
    root = UpdateStatus()
    root.mainloop()