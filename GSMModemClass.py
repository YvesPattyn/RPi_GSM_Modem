import serial
import socket
import time
from time import sleep
from curses import ascii
from  os import system
from datetime import datetime
import logging

class GSMModem:
    def __init__(self):
        logging.debug('Instance of GSMModem created.')
        self.ser = serial.Serial(port="/dev/ttyUSB0",baudrate=460800,timeout=1)
        # ATtention - Set Echo Off
        logging.debug(self.serialCommand("ATE0\r\n"))
        # Preferred Message Storage
        logging.debug("Setting Preferred Message Storage to SIM card.")
        cmd = 'AT+CPMS="SM","SM","SM"\r\n'
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        # Show text mode parameters for AT+CMGR commands
        cmd = "AT+CSDH=1\r\n"
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        # Setting message intercept for Huawey
        logging.debug("Setting New Messages Intercept")
        cmd = "AT+CNMI=2,0,0,2,1\r\n"
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        # Check if PIN must be entered.
        logging.debug("Checking PIN status.")
        cmd = "AT+CPIN?\r\n"
        logging.debug(cmd)
        pinCheck = self.serialCommand(cmd)
        if ( ("+CPIN" in pinCheck) and ("READY" in pinCheck) ):
          logging.debug("PIN is still active. No need to enter it.")
        else:
          logging.info("PIN code is Required - Entering it now.")
          # Enter PIN code if required
          cmd = 'AT+CPIN="6604"\r\n'
          logging.debug(self.serialCommand(cmd))
        
    def serialCommand(self, cmd, message = ""):
        retval = ""
        if (message != ""):
            logging.debug("-- SEND --")
            logging.debug("  Command:%s" % cmd)
            logging.debug("---------")
            logging.debug("  Message:%s" % message)
            logging.debug("---------")
            message = message + ascii.ctrl('Z')
            self.ser.write(cmd.encode())
            self.ser.write(message.encode())
        else:
            self.ser.write(cmd.encode())
        line = self.ser.readline()
        while ( line != b'' ):
            retval = retval + line.decode()
            logging.debug(line)
            line = self.ser.readline()
        return retval
    
    def getAllMessages(self):
        # Text Mode on
        logging.debug("Switching to TEXT mode.")
        cmd = "AT+CMGF=1\r\n"
        logging.debug(self.serialCommand(cmd))
        # List all messages
        cmd = 'AT+CMGL="ALL"\r\n'
        return self.serialCommand(cmd)
        
    def deleteMessage(self,messageNumber):
        cmd ='AT+CMGD=' + messageNumber + '\r\n'
        logging.debug(self.serialCommand(cmd))

    def deleteAllMessages(self):
        cmd ='AT+CMGD=1,4\r\n'
        logging.debug(self.serialCommand(cmd))
            
    def readMessage(self,messageNumber):       
        # PDU Mode on
        logging.debug("Switching to PDU mode.")
        cmd = "AT+CMGF=0\r\n"
        self.serialCommand(cmd)
        # Read message nr
        cmd ='AT+CMGR=%s\r\n' % messageNumber
        self.ser.write(cmd.encode())
        line = self.ser.readline()
        strLine = line.decode()
        while ( (strLine != '') and (line != b'\x00') ):
            logging.debug(strLine)
            if('0791' in strLine):
                logging.debug('Line holding the message was found')
                retval = strLine
            line = self.ser.readline()
            strLine = line.decode()
        return retval

    def sendMessage(self,phoneNr,textMessage):
        logging.debug("Switching to TEXT mode.")
        cmd = "AT+CMGF=1\r\n"
        self.ser.write(cmd.encode())
        textMessage = textMessage + ascii.ctrl('Z')
        cmd ='AT+CMGS="%s"\r\n' % phoneNr
        logging.debug(cmd)
        self.ser.write(cmd.encode())
        logging.debug(textMessage)
        self.ser.write(textMessage.encode())
        line = self.ser.readline()
        strLine = line.decode()
        logging.debug(strLine)
        line = self.ser.readline()
        strLine = line.decode()
        logging.debug(strLine)

    def getStatus(self):
        retval = []
        # PIN Status
        cmd = "AT+CPIN?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        # New Messages Intercept"
        cmd = "AT+CNMI?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        cmd = "AT+CNMI=?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        # PDU status [1=Active]")
        cmd = "AT+CMGF?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        # Preffered Message Storage"
        cmd = "AT+CPMS?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        cmd = "AT+CPMS=?\r\n"
        logging.debug(cmd)
        retval.append(self.serialCommand(cmd))
        



    
