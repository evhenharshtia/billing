import telnetlib
import time
import sys
import mysql.connector
import json
import requests
import re

def get_date_telnet(mac,ip_a,command):
	try:
		file=open('devices.txt','r')
		for line in file:
			info = {}
			#info['ip'] = line.split(' ')[0]
			info['login'] = line.split(' ')[1]
			info['passw'] = line.split(' ')[2]
			
			login_a = info['login']
			password_a = info['passw']
			# print (type(ip_a))
			# print (type(login_a))
			# print (type(password_a))
			# print (type(mac))
			connect=telnetlib.Telnet(ip_a)
			#comm = 'show mac address-table  '+mac+'\n'
			comm = command+mac+'\n'

			#connect.read_until(b"Username: ")
			connect.write(login_a.encode('ascii')+b"\n")
			connect.write(password_a.encode('ascii')+b"\n")
			connect.write('Enable\n'.encode('ascii'))
			connect.write(comm.encode('ascii'))
			connect.read_until('show'.encode('ascii'))

			time.sleep(3)
			print ('##################################################################')
			return connect.read_very_eager()
			connect.close()
	except ValueError as err:
        	return print('Error')

#new = get_date_telnet('c89c.1d98.73d9')
def get_date_user(login):
	
		db = mysql.connector.connect(host = '192.168.10.1',user = 'username',password = 'USERpass',database = 'billing' )

		cursor = db.cursor()

		cursor.execute("SELECT `userpswd`,`ballance`,`maconu`,`mac` FROM `alldata` WHERE `username` = '"+ login+"'")

		#data = cursor.fetchone()
		data = cursor.fetchall()
		if not data:
			data = 'НІчого не знайдено'
		else:
			for x in data:
				userpswd, ballance, maconu, mac = x
				print(login, userpswd, ballance)
				data = '|Логін: '+login+'|\r\n|Пароль: '+userpswd+'|\r\n|Мак адреса: '+mac+'|\r\n|МакОну: '+maconu+'|\r\n|Баланс: '+str(ballance)+'|'
				#data = 'Логін: '+login+'|  Пароль: '+userpswd+'|  МакОну: '+maconu+'|  Баланс: '+str(ballance)
		return data
	
		db.close()
def get_date_account(acc_number):
	
		db = mysql.connector.connect(host = '192.168.10.1',user = 'username',password = 'USERpass',database = 'billing' )

		cursor = db.cursor()

		cursor.execute("SELECT `username`,`userpswd`,`ballance`,`maconu`,`mac` FROM `alldata` WHERE `status` = "+ acc_number)

		#data = cursor.fetchone()
		data = cursor.fetchall()
		for x in data:
			username, userpswd, ballance, maconu, mac= x
			print(username, userpswd, ballance)
			data = '|Логін: '+username+'|\r\n|Пароль: '+userpswd+'|\r\n|Мак адреса: '+mac+'|\r\n|МакОну: '+maconu+'|\r\n|Баланс: '+str(ballance)+'|'
		return data
	
		db.close()

def format_mac(mac: str) -> str:
    mac = re.sub(':', '', mac).upper()
    mac = ''.join(mac.split())
    assert len(mac) == 12
    assert mac.isalnum()
    mac = ".".join(["%s" % (mac[i:i+4]) for i in range(0, 12, 4)])
    return mac
