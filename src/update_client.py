from tkinter.messagebox import askyesno
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



with open('/home/polina/Test_Update_Folder_tmp/update_message', 'r') as message:
    text_message = message.read()

def ask_permition():
    result = askyesno(title="Подтвержение операции", message=text_message)
    if result:
        copy_command('/home/polina/Test_Update_Folder_tmp/bin', '/home/polina/Test_Update_Folder/bin')
        copy_command('/home/polina/Test_Update_Folder_tmp/etc', '/home/polina/Test_Update_Folder/etc')
        delete_command('/home/polina/Test_Update_Folder_tmp/bin')
        delete_command('/home/polina/Test_Update_Folder_tmp/etc')
        os.remove('/home/polina/Test_Update_Folder_tmp/update_message')

        host = '127.0.0.1'
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        message = "Updated"
        s.send(message.encode('utf-8'))
        s.close()
        #root2.destroy()
    else:
        host = '127.0.0.1'
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        message = "Canceled"
        s.send(message.encode('utf-8'))
        s.close()
        time.sleep(10)
        ask_permition()

    if __name__ == '__main__':
        ask_permition()
