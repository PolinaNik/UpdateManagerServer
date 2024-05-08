import shutil
import os

#import paramiko
# ssh = paramiko.SSHClient()
# ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
# ssh.connect(server, username=username, password=password)
# sftp = ssh.open_sftp()
# sftp.put(localpath, remotepath)
# sftp.close()
# ssh.close()

def copy_command(src_folder, dst_folder):
    src_files = os.listdir(src_folder)
    for file_name in src_files:
        full_file_name = os.path.join(src_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst_folder)

def copy_files_tmp(test_msg):
    print(test_msg)
    copy_command('/home/polina/PycharmProjects/UpdateManagerServer/UpdateFiles/bin', '/home/polina/Test_Update_Folder_tmp/bin')
    copy_command('/home/polina/PycharmProjects/UpdateManagerServer/UpdateFiles/etc', '/home/polina/Test_Update_Folder_tmp/etc')
    shutil.copy('/home/polina/PycharmProjects/UpdateManagerServer/UpdateFiles/update_message', '/home/polina/Test_Update_Folder_tmp')





