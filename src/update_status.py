from tkinter import *
from tkinter import ttk
import socket
from _thread import *
import threading

print_lock = threading.Lock()
host = ('localhost')
port = 12345

#TODO: отображение статуса обновления


class SOCKETS:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Socket Is Now Created")

    def load(self, text):
        self.history = text
        return


    def bind(self):
        self.s.bind((host, port))
        self.s.listen(5)
        while True:
            # establish connection with client
            conn, addr = self.s.accept()

            # lock acquired by client
            print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            start_new_thread(self.threaded, (conn,))
        # self.s.close()

    def threaded(self, conn):
        while True:

            # data received from client
            data = conn.recv(1024)
            start = self.history.index('end') + "-1l"
            self.history.insert("end", data)
            end = self.history.index('end') + "-1l"
            if not data:
                print('Bye')

                # lock released on exit
                print_lock.release()
                break

            # # send back string to client
            # c.send(data)

        # # connection closed
        # c.close()


class UpdateStatus(Frame):
    def __init__(self, parent, hostnames):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()
        self.hostnames = hostnames
        self.create_panel_for_widget()
        threading.Thread(target=self.socket_connections).start()

    def initialize_user_interface(self):
        self.parent.geometry("600x780")
        self.parent.title("Update Status")
        self.parent.resizable(False, True)
        self.parent.config(bg="white")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_panel_for_widget()

    def close(self):
        root.destroy()

    def create_panel_for_widget(self):
        # create panel frame
        self.panel = LabelFrame(self.parent, text="Статус обновления", font=("Arial", 15), padx=5,
                                pady=5)
        self.panel.grid_rowconfigure(0, weight=1)
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.rowconfigure(0, weight=1)
        self.panel.columnconfigure(0, weight=1)
        self.panel.grid(row=0, column=0, sticky="news")

        # hostnames
        print(self.hostnames)
        self.version_name_label = ttk.Label(self.panel, text=self.hostnames,
                                            font=("Arial", 13))
        self.version_name_label.grid(row=0, column=0, columnspan=2, sticky="news")
        self.history = Text(self.panel, font=('arial 12 bold italic'))
        self.history.grid(row=1, column=0, columnspan=2, sticky="news")
        return

    def socket_connections(self):
        self.s = SOCKETS()
        self.s.load(self.history)
        self.s.bind()


if __name__ == "__main__":
    root = Tk()
    root = UpdateStatus(root, hostnames='test',)
    root.mainloop()
