#!/usr/bin/env python
# -*- coding: utf_8 -*-

# підключаємо модулі для роботи з протоколом ssh
from paramiko import SSHClient
from paramiko import AutoAddPolicy
import datetime
import time
import sys
import os
Version = datetime.date.today()

FtpdIP = '192.168.10.202'
ftpUser = "ftpuser"
ftpPass = "ftpPassword2020"
path = "/Public/ftpBackup/mt"
# ip = '192.168.10.254'
# login = 'root'
# password = 'c17h35coona'
# port = '2184'
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
file=open('/home/feldsher/scripts/devices.txt','r')
for line in file:
    info = {}
    info['ip'] = line.split(' ')[0]
    info['login'] = line.split(' ')[1]
    info['passw'] = line.split(' ')[2]
    info['port'] = line.split(' ')[3]
    ip_a= info['ip']
    login_a = info['login']
    password_a = info['passw']
    port1 = int(info['port'])
    def connector():
        print ("connecting.." + str(ip_a) + "@"  + str(login_a) + ":" + str(password_a))
        ssh.connect(ip_a, port=port1, username=login_a, password=password_a, look_for_keys=False)
        print ("connected..")
        


    try:
        path_n=path+"/"+ip_a
        print(path_n)
	commandEx = "export file="+ip_a+"-"+str(Version)
        UploadToFtp = "tool fetch address=" + str(FtpdIP) + " mode=ftp dst-path=" + path_n +"/"+ str(ip_a) + "-" + str(Version) + ".rsc src-path=" + str(ip_a) + "-" + str(Version)+ ".rsc" + " user=" + str(ftpUser) + " password=" + str(ftpPass) + " upload=yes"
        print(UploadToFtp)
	RemoveLocalBckp = 'file remove "' + str(ip_a) + "-" + str(Version) + ".rsc" + '"'
        connector()
        channel  = ssh.invoke_shell()
        print ("creating local backup.. /" + commandEx)
        stdin,stdout,stderr = ssh.exec_command(commandEx)
        time.sleep(5)
        print ("local backup created..")
        stdin1,stdout1,stderr1 = ssh.exec_command(UploadToFtp)
        time.sleep(5)
        print ("backup uploaded to remote location..")
        print ("removing local backup.. /" + RemoveLocalBckp)
        stdin2,stdout2,stderr2 = ssh.exec_command(RemoveLocalBckp)
        print ("local backup removed.."+ip_a)
        time.sleep(2)
        print stdout.read()
        #channel.send(commandEx)
        #print ("uploading local backup to ftp.. /" + UploadToFtp)
        #channel.send(UploadToFtp)
        #print ("backup uploaded to remote location..")
        #print ("removing local backup.. /" + RemoveLocalBckp)
        #channel.send(RemoveLocalBckp)
    except Exception as e:
        error_log=str(e)
        print (error_log+ "\n")











# print ("connecting.." + str(ip_a) + "@"  + str(login_a) + ":" + str(password_a))
# ssh.connect(ip_a, port=port1, username=login_a, password=password_a, look_for_keys=False)
# print ("connected..")
# # creating local backup
# print ("creating local backup.. /" + commandEx)
# ssh.exec_command(commandEx)
# # sleep after each command because mikrotik can not do it so fast as script executes
# time.sleep(3)
# print ("local backup created..")
# # uloading local backup to ftp
# print ("uploading local backup to ftp.. /" + UploadToFtp)
# ssh.exec_command(UploadToFtp)
# time.sleep(5)
# print ("backup uploaded to remote location..")
# # removing local backup
# time.sleep(5)
# print ("removing local backup.. /" + RemoveLocalBckp)
# ssh.exec_command(RemoveLocalBckp)
# time.sleep(2)
# print ("local backup removed.."+ip_a)
# ssh.close()
# #finally:
file.close()


# ssh.connect(mip, port=2184, username=ml, password=mp, look_for_keys=False)
# exe = ":log info message=\"It is authorised\""
# excmd2 = ssh.exec_command(exe)[1].read()
# ssh.close()
