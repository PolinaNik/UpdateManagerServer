from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo,showerror
from read_config import rc_osnov, rc_reserv
from textwrap import wrap
from src import update_status

#TODO: функция для обработки текста названия версии, при отсутсвии - текущая дата и время
#TODO: подключение базы данных


class UpdateWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Update Manager")
        self.geometry("600x780")
        self.resizable(False, True)
        self.config(bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()
        self.test = 'test'

    def create_widgets(self):
        self.create_panel_for_widget()

    def select_hosts(self, event):
        # получаем индексы выделенных элементов
        selected_indices = self.comp_listbox.curselection()
        # получаем сами выделенные элементы
        self.selected_comps = ",".join([self.comp_listbox.get(i) for i in selected_indices])
        msg = "Вы выбрали: %s" % self.selected_comps
        self.selection_label["text"] = msg
        self.hostnames = ''
        if self.selected_comps == "РЦ-основные места":
            self.hostnames = rc_osnov
        elif self.selected_comps == "РЦ-резервные места":
            self.hostnames = rc_reserv
        elif self.selected_comps == "АДЦ-основные места":
            self.hostnames = '[adc_osnov]'
        elif self.selected_comps == "АДЦ-резервные места":
            self.hostnames = '[adc_reserv]'
        text_hostnames = str(self.hostnames)[1:-1]
        if len(text_hostnames) > 100:
            char_width = len(text_hostnames) / 100
            wrapped_text = '\n'.join(wrap(text_hostnames, int(250 / char_width)))
            self.selection_hostnames["text"] = wrapped_text
        else:
            self.selection_hostnames["text"] = text_hostnames

    def select_mode(self):
        self.header_mode.config(text="Выбран %s" % self.mode.get())
        # print(self.mode.get())
        # if self.mode.get() == "режим с подтверждением":
        #     print('ok')

    def select_process(self):
        self.header_process.config(text="Выбран %s" % self.process.get())

    def ask_question(self):
        # try:
            result = askyesno(title="Подтвержение операции", message="Выполнить обновление на %s" % self.selected_comps)
            if result:
                if self.mode.get() == "режим без подтверждения (тихий)":
                    question2 = askyesno(title="Подтверждение операции", message="Вы уверены, что обновление будет в тихом режиме (без подтверждения)?")
                    if question2:
                        showinfo("Результат", "Операция подтверждена")
                        self.close()
                    else:
                        showinfo("Результат", "Операция отменена")
                if not self.process.get():
                    showerror("Ошибка", "Вы не выбрали процессы для перезагрузки")
                showinfo("Результат", "Операция подтверждена")
                self.update()
            else:
                showinfo("Результат", "Операция отменена")
        # except AttributeError:
        #     showerror("Ошибка", "Вы не выбрали рабочие места для обновления")

    def update(self):
        text_hostnames = str(self.hostnames)[1:-1]
        root.destroy()
        new_root = Tk()
        new_window = update_status.UpdateStatus(new_root, hostnames=text_hostnames)
        new_window.mainloop()

    def close(self):
        root.destroy()


    def create_panel_for_widget(self):
        # create panel frame
        self.panel = LabelFrame(self, text="Ввод информации для обновления", font=("Arial", 15), padx=5,
                                pady=5)
        self.panel.grid_rowconfigure(0, weight=1)
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.rowconfigure(0, weight=1)
        self.panel.columnconfigure(0, weight=1)
        self.panel.grid(row=0, column=0, sticky="news")

        # version label name
        self.version_name_label = ttk.Label(self.panel, text="Введите название версии (например: cartography_10_24):",
                                            font=("Arial", 13))
        self.version_name_label.grid(row=0, column=0, columnspan=2, sticky="news")
        self.version_name_entry = Entry(self.panel)
        self.version_name_entry.grid(row=1, column=0, columnspan=2, sticky="news")

        # host selection
        self.select_host_label = ttk.Label(self.panel, text="Выберите рабочие места из списка:",
                                           font=("Arial", 13))
        self.select_host_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="news")
        self.group_hosts = ["РЦ-основные места", "РЦ-резервные места",
                            "АДЦ-основные места", "АДЦ-резервные места"]
        self.comps_var = Variable(value=self.group_hosts)
        self.comp_listbox = Listbox(self.panel, listvariable=self.comps_var, selectmode=EXTENDED)
        self.comp_listbox.grid(row=3, column=0, columnspan=2, pady=5, sticky="news")
        self.comp_listbox.bind("<<ListboxSelect>>", self.select_hosts)
        self.selection_label = ttk.Label(self.panel)
        self.selection_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="news")
        self.selection_hostnames = ttk.Label(self.panel)
        self.selection_hostnames.grid(row=5, column=0, columnspan=2, pady=5, sticky="news")

        # mode selection
        self.select_mode_label = ttk.Label(self.panel, text="Выберите режим:", font=("Arial", 13))
        self.select_mode_label.grid(row=6, column=0, columnspan=2, pady=5, sticky="news")
        regular = "режим с подтверждением"
        silence = "режим без подтверждения (тихий)"
        self.mode = StringVar()
        self.regular_btn = ttk.Radiobutton(self.panel, text="Режим с подтверждением", value=regular, variable=self.mode,
                                           command=self.select_mode)
        self.regular_btn.grid(row=7, column=0, pady=5, sticky="nw")

        self.silence_btn = ttk.Radiobutton(self.panel, text="Режим без подтверждения (тихий)", value=silence,
                                           variable=self.mode, command=self.select_mode)
        self.silence_btn.grid(row=7, column=1, pady=5, sticky="nw")
        self.header_mode = ttk.Label(self.panel)
        self.header_mode.grid(row=8, column=0, columnspan=2, pady=5, sticky="news")

        # restart process
        self.select_process_label = ttk.Label(self.panel,
                                              text="Выберите какой из процессов перезагрузить после обновления:",
                                              font=("Arial", 13))
        self.select_process_label.grid(row=9, column=0, columnspan=2, pady=5, sticky="news")
        self.process = StringVar()
        process1 = "process1"
        process2 = "process2"
        process3 = "process3"
        process4 = "process4"
        self.process1_btn = ttk.Radiobutton(self.panel, text="Process1", value=process1,
                                            variable=self.process, command=self.select_process)
        self.process1_btn.grid(row=10, column=0, pady=5, sticky="nw")
        self.process2_btn = ttk.Radiobutton(self.panel, text="Process2", value=process2,
                                            variable=self.process, command=self.select_process)
        self.process2_btn.grid(row=10, column=1, pady=5, sticky="nw")
        self.process3_btn = ttk.Radiobutton(self.panel, text="Process3", value=process3,
                                            variable=self.process, command=self.select_process)
        self.process3_btn.grid(row=11, column=0, pady=5, sticky="nw")
        self.process4_btn = ttk.Radiobutton(self.panel, text="Process4", value=process4,
                                            variable=self.process, command=self.select_process)
        self.process4_btn.grid(row=11, column=1, pady=5, sticky="nw")
        self.header_process = ttk.Label(self.panel)
        self.header_process.grid(row=12, column=0, columnspan=2, pady=5, sticky="news")

        # comment field
        self.comment_label = ttk.Label(self.panel, text="Напишите комментарий (отобразится на экране клиента):",
                                       font=("Arial", 13))
        self.comment_label.grid(row=13, column=0, columnspan=2, pady=5, sticky="news")
        self.comment_field = Text(self.panel, height=5, wrap="word")
        self.comment_field.grid(row=14, column=0, columnspan=2, pady=5, sticky="news")
        self.scrollbar = ttk.Scrollbar(self.panel, orient="vertical", command=self.comment_field.yview)
        self.scrollbar.grid(row=14, column=1, pady=5, sticky="nse")
        self.comment_field["yscrollcommand"] = self.scrollbar.set

        # update button
        self.update_btn = Button(self.panel, text="Запуск обновления", command=self.ask_question,
                                 activebackground="green2")
        self.update_btn.grid(row=15, column=1, pady=5, sticky="news")

        # close button
        self.close_btn = Button(self.panel, text="Отменить", command=self.close, activebackground="coral1")
        self.close_btn.grid(row=15, column=0, pady=5, sticky="news")


if __name__ == "__main__":
    root = UpdateWindow()
    root.mainloop()
