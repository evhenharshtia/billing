import telnetlib
import time

import sys

if __name__ == "__main__":
    if len (sys.argv) > 1:
        host=sys.argv[1] 
        port=sys.argv[2]
        com=sys.argv[3]
    else:
        print ("Not enough parameters!!!")



#host='192.168.10.92'
connect=telnetlib.Telnet(host)
connect.write('admin\n')
connect.write('rtl8186\n')
connect.write('Enable\n')

if com=="-c" : 
	connect.write('show running-config interface epoN'+ port +'\n')
elif com=="-m":
	connect.write('show mac address-table interface epoN'+ port +'\n')
elif com=="-o":
	connect.write('show epon interface epoN '+ port +' onu ctc optical-transceiver-diagnosis\n')

elif com=="-f":
    connect.write('config\n')
    #connect.write('interface epon'+ port+'\n')
    connect.write('filter enable\n')
    connect.write('exit\n')
    connect.write('write ifindex\n')
    connect.write('write all\n')


#connect.write('show ip interface\n')
else: 
	print ("Not enought parameters!!!")


time.sleep(1)
print '##################################################################'
print connect.read_very_eager()
connect.close()
