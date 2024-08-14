from tkinter.messagebox import askquestion
import os
import shutil
import socket
import time
import tkinter as tk


def copy_command(src_folder, dst_folder):
    src_files = os.listdir(src_folder)
    for file_name in src_files:
        full_file_name = os.path.join(src_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst_folder)


def delete_command(src_folder):
    src_files = os.listdir(src_folder)
    for file_name in src_files:
        full_file_name = os.path.join(src_folder, file_name)
        os.remove(full_file_name)



with open('/home/client1/Desktop/files_for_update_tmp/update_message', 'r') as message:
    text_message = message.read()

def ask_permition():
    root = tk.Tk()
    root.geometry("1x1")
    root.resizable(False, False)
    result = askquestion(title="Подтвержение операции", message=text_message)
    if result == 'yes':
        copy_command('/home/client1/Desktop/files_for_update_tmp/bin', '/home/client1/Desktop/files_for_update/bin')
        #copy_command('/home/polina/Test_Update_Folder_tmp/etc', '/home/polina/Test_Update_Folder/etc')
        delete_command('/home/client1/Desktop/files_for_update_tmp/bin')
        #delete_command('/home/polina/Test_Update_Folder_tmp/etc')
        os.remove('/home/client1/Desktop/files_for_update_tmp/update_message')

        host = '192.168.1.69'
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        message = socket.gethostname()+" updated\n"
        s.send(message.encode('utf-8'))
        s.close()
    else:
        root.destroy()
        host = '192.168.1.69'
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        message = socket.gethostname()+" canceled by user\n"
        s.send(message.encode('utf-8'))
        s.close()
        time.sleep(10)
        ask_permition()


ask_permition()
