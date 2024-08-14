import os
from paramiko import SSHClient
import threading
import socket
import logging
import json


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'

logging.basicConfig(format=FORMAT, filename="update.log",filemode="a+", level=logging.INFO)

localpath = '/home/server/Desktop/UpdateManagerServer_ubuntu/UpdateFiles/update_message'

global host_dict
host_dict = {}

def copy_command(src_folder, dst_folder, hostname, username):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    try:
        ssh.connect(hostname=hostname, username=username)
        sftp = ssh.open_sftp()
        remotepath = '/home/%s/Desktop/files_for_update_tmp/update_message' % hostname
        sftp.put(localpath, remotepath)
        src_files = os.listdir(src_folder)
        for file_name in src_files:
            full_file_name = os.path.join(src_folder, file_name)
            if os.path.isfile(full_file_name):
                sftp.put(full_file_name, '%s/%s'% (dst_folder, file_name))
        sftp.close()
        ssh.close()
        print(hostname)
        host_dict[hostname] = "connected"
        message = "Files were copied to %s" % hostname
        logging.info(message)
    except:
        host_dict[hostname] = "disconnected"
        message = "NO CONNECTION with %s" % hostname
        logging.warning(message)
    with open("host_dict.json", "w") as fp:
        json.dump(host_dict, fp)
    
def ssh_command(host):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    try:
        ssh.connect(hostname=host, username=host)
        command = 'export DISPLAY=:0; python3.5 /home/%s/Desktop/UpdateManagerServer_ubuntu/src/update_client.py &' %host
        ssh.exec_command(command)
    except:
        print('No connection with host %s' % host)

def copy_files_tmp(hostnames):
    hostnames = hostnames.split(',')
    threads = []
    for host in hostnames:
        copy_command('/home/server/Desktop/UpdateManagerServer_ubuntu/UpdateFiles/bin', '/home/%s/Desktop/files_for_update_tmp/bin' %host, hostname=host, username=host)
        print(host_dict)
        thread = threading.Thread(target=ssh_command, args=(host,))
        threads.append(thread)
        thread.start()




