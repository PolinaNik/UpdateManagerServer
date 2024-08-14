from tkinter import *
from tkinter import ttk
import socket
from _thread import *
import threading
import os
print_lock = threading.Lock()
host = ('192.168.1.69')
port = 12345
import json



# команда, чтобы очистить процессы, завязанные на порте:
# sudo lsof -t -i tcp:12345 | xargs kill -9


#TODO: отображение статуса обновления

results = dict()

class SOCKETS:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] Socket Is Now Created")

    def load(self, text):
        self.history = text
        return


    def bind(self):
        try:
            self.s.bind((host, port))
        except:
            os.system("sudo lsof -t -i tcp:12345 | xargs kill -9")
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
            #data_split = data.decode('utf-8').split(' ')
            #if len(data_split) > 1:
                #results.update({data_split[0]: data_split[1]})
                #for key, value in results.items():
                #    if value == "updated\n":
                #        buttons[key].configure(bg='green')
                #    else:
                #        buttons[key].configure(bg='grey')
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
        #threading.Thread(target=update_client.ask_permition()).start()

    def initialize_user_interface(self):
        self.parent.geometry("600x600")
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
        json_file_path = "host_dict.json"
        with open(json_file_path, 'r') as j:
            host_dict = json.loads(j.read())
        # check connection
        no_connection = []
        for key, value in host_dict.items():
            if value == 'disconnected':
                no_connection.append(key)
        # create panel frame
        self.panel = LabelFrame(self.parent, text="Статус обновления", font=("Arial", 15), padx=5, pady=5)
        self.panel.grid_rowconfigure(0, weight=1)
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.rowconfigure(0, weight=1)
        self.panel.columnconfigure(0, weight=1)
        self.panel.grid(row=0, column=0, sticky="news")
        
        
        # hostnames
        text_message = 'Update for %s' %self.hostnames 
        self.version_name_label = ttk.Label(self.panel, text=text_message,
                                            font=("Arial", 13))
        self.version_name_label.grid(row=0, column=0, columnspan=2, sticky="news")
            
        self.history = Text(self.panel, font=('arial 12 bold italic'))
        self.history.grid(row=1, rowspan=10, column=0, columnspan=2, sticky="news")
        self.scrollbar = ttk.Scrollbar(self.panel, orient="vertical", command=self.history.yview)
        self.scrollbar.grid(row=1, rowspan=10, column=1, pady=5, sticky="nse")
        if len(no_connection) > 0:
            str_no_connection = ', '.join(el for el in no_connection)
            text_message2 = "No connection with: %s" %str_no_connection
            self.no_connection_label = ttk.Label(self.panel, text=text_message2, font=("Arial", 13), foreground='red')
            self.no_connection_label.grid(row=11,column=0, columnspan=2, sticky="news")
        

    def socket_connections(self):
        self.s = SOCKETS()
        self.s.load(self.history)
        self.s.bind()


if __name__ == "__main__":
    root = Tk()
    root = UpdateStatus(root, hostnames='test',)
    root.mainloop()
