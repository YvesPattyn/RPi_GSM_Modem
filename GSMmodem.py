import serial
import socket
from relay import relay
import time
from time import sleep
from curses import ascii
from  os import system
from datetime import datetime
from PDUClass import GSMMessage
import logging

def getIPaddress():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  IPaddress = s.getsockname()[0]
  s.close()
  return IPaddress

def serialCommand(ser, cmd, message = ""):
  retval = ""
  if (message != ""):
    logging.debug("-- SEND --")
    logging.debug("  Command:%s" % cmd)
    logging.debug("---------")
    logging.debug("  Message:%s" % message)
    logging.debug("---------")
    message = message + ascii.ctrl('Z')
    ser.write(cmd.encode())
    ser.write(message.encode())
  else:
    ser.write(cmd.encode())
  line = ser.readline()
  while ( line != b'' ):
    retval = retval + line.decode()
    logging.debug(line)
    line = ser.readline()
  return retval

logging.basicConfig(level=logging.ERROR)

system('clear')

print('Python GSM control module')
print('by Yves Pattyn,  June 2019')
print('--------------------------')

now = datetime.now()
logging.info("Current date is : %s" % now.strftime("%d-%m-%y %H:%M:%S"))
logging.info("IP Address of this RaspberryPi is: %s" % getIPaddress())

r = relay(12,"Testing")
r.off()
try:
  out = system('ls /dev/ttyU*')
except:
  logging.error('Failed system call')

ser = serial.Serial(port="/dev/ttyUSB0",baudrate=460800,timeout=1)
# ATtention - Set Echo Off
serialCommand(ser,"ATE0\r\n")

# Preferred Message Storage
logging.info("Setting Preferred Message Storage to SIM card.")
cmd = 'AT+CPMS="SM","SM","SM"\r\n'
serialCommand(ser,cmd)

# Show text mode parameters for AT+CMGR commands
cmd = "AT+CSDH=1\r\n"
serialCommand(ser,cmd)

# Setting message inytercept for Huawey
logging.info("Setting New Messages Intercept")
cmd = "AT+CNMI=2,0,0,2,1\r\n"
logging.info(serialCommand(ser,cmd))

# Check if PIN must be entered.
logging.info("Checking PIN status.")
cmd = "AT+CPIN?\r\n"
pinCheck = serialCommand(ser,cmd)
if ( ("+CPIN" in pinCheck) and ("READY" in pinCheck) ):
  logging.info("PIN is still active. No need to enter it.")
else:
  logging.info("PIN code is Required - Entering it now.")
  # Enter PIN code if required
  cmd = 'AT+CPIN="6604"\r\n'
  serialCommand(ser,cmd)

choice = 99
while (choice != '0'):
  print('-----------------------------\r\n')
  print('1. List all messages')
  print('2. Delete one message')
  print('3. Detele all messages')
  print('4. Wait for incoming message')
  print('5. Send a message')
  print('6. Read a message')
  print('7. Clear Screen')
  print('8. Send PIN')
  print('9. Display Status')
  print('0. Exit')
  choice = input('Enter choice: ')
  print("")
  if (choice == '1'):
    # Text Mode on
    logging.info("Switching to TEXT mode.")
    cmd = "AT+CMGF=1\r\n"
    logging.info(serialCommand(ser,cmd))
    # List all messages
    print('Getting all messages')
    cmd = 'AT+CMGL="ALL"\r\n'
    logging.info(serialCommand(ser,cmd))
  if (choice =='2'):
    msgnr = input('Message number to delete : ')
    cmd ='AT+CMGD=' + msgnr + '\r\n'
    print(serialCommand(ser,cmd))
    print("Message has been deleted.")
  if (choice == '3'):
    print ('Deleting ALL messages')
    cmd ='AT+CMGD=1,4\r\n'
    print(serialCommand(ser,cmd))
  if (choice == '4'):
    print('Listening for messages . . . ')
    print("Switching to TEXT mode.")
    cmd = "AT+CMGF=1\r\n"
    serialCommand(ser,cmd)
    keepgoing = True
    while(keepgoing):
      cmd = 'AT+CMGL="ALL"\r\n'
      strLine = serialCommand(ser,cmd)
      print(strLine)
      # Remove all messages
      cmd ='AT+CMGD=1,4\r\n'
      serialCommand(ser,cmd)
      if ("LIGHTOFF" in strLine):
        r.off()
      if ("LIGHTON" in strLine):
        r.on()
      if ("CONFIG" in strLine):
        keepgoing = True
      if ("STOP" in strLine):
        keepgoing = False
      sleep(2)
    system('clear')
  if (choice == '5'):
    phoneNr = input('Enter phoneNr : ')
    message = input('Enter message : ')
    message = message + ascii.ctrl('Z')
    cmd ='AT+CMGS="%s"\r\n' % phoneNr
    print(cmd)
    ser.write(cmd.encode())
    ser.write(message.encode())
    line = ser.readline()
    strLine = line.decode()
    print(line)
    line = ser.readline()
    strLine = line.decode()
    print(line)
  if (choice == '6'):
    # PDU Mode on
    print("Switching to PDU mode.")
    cmd = "AT+CMGF=0\r\n"
    serialCommand(ser,cmd)
    # Read message nr
    msgNr = input('Enter message Nr : ')
    cmd ='AT+CMGR=%s\r\n' % msgNr
    ser.write(cmd.encode())
    line = ser.readline()
    strLine = line.decode()
    while ( (strLine != '') and (line != b'\x00') ):
      if('0791' in strLine):
        print('Line holding the message was found')
        msg = GSMMessage(strLine)
        print("Message: %s " % msg.getMessage())
        print("Received from %s " % msg.OANum)
        print("Switching to TEXT mode prior to sending.")
        cmd = "AT+CMGF=1\r\n"
        serialCommand(ser,cmd)
        cmd ='AT+CMGS="%s"\r\n' % msg.OANum
        response = "IP address : %s" % getIPaddress()
        print(serialCommand(ser, cmd, response ))
        #msg.dumpData()
      line = ser.readline()
      strLine = line.decode()
  if (choice == '7' ):
    system('clear')
  if (choice == '8' ):
    # Forced enter of PIN code
    cmd = 'AT+CPIN="6604"\r\n'
    print(serialCommand(ser,cmd))
  if (choice == '9' ):
    print("PIN Status")
    cmd = "AT+CPIN?\r\n"
    print(serialCommand(ser,cmd))

    print("New Messages Intercept")
    cmd = "AT+CNMI?\r\n"
    print(serialCommand(ser,cmd))
    cmd = "AT+CNMI=?\r\n"
    print(serialCommand(ser,cmd))

    print("PDU status [1=Active]")
    cmd = "AT+CMGF?\r\n"
    print(serialCommand(ser,cmd))

    print("Preffered Message Storage")
    cmd = "AT+CPMS?\r\n"
    print(serialCommand(ser,cmd))
    cmd = "AT+CPMS=?\r\n"
    print(serialCommand(ser,cmd))

r.off()
exit(0)
