from GSMModemClass import GSMModem
from PDUClass import GSMMessage
from time import sleep
import datetime
import logging
from LcdDisplay import lcdDisplay
import Adafruit_DHT
from DTH11 import DTH11

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

logging.basicConfig(level=logging.INFO)
logging.info("Initialisation of the modem in progress.")
modem = GSMModem()
modem.deleteAllMessages()

logging.info("Initialisation of the LCD display.")
lcd = lcdDisplay()

logging.info("Initialisation of the DHT (Temperature and Humidity probe).")
d = DTH11(21 ,Adafruit_DHT.DHT11)

while True:
  hexmsg = "Dummy"
  replyNumber = "Dummy"
  readableMessage = "DummyDummy"
  logging.info("* Start list All Messages *")
  modem.getAllMessages()
  logging.info("* End list All Messages *")
  now = datetime.datetime.now()
  lcd.showString("Awaiting SMS ...",LCD_LINE_1)
  lcd.showString( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) ,LCD_LINE_2)
  for msgNumber in range(5):
    logging.info("READING MSG %s" % msgNumber)
    hexmsg = modem.readMessage(msgNumber)
    logging.info("hexmsg=%s" % hexmsg)
    if ("791" in hexmsg):
      modem.deleteMessage(msgNumber)
      gsmMessage = GSMMessage(hexmsg)
      replyNumber = gsmMessage.OANum
      # gsmMessage.dumpData()
      readableMessage = gsmMessage.getMessage()
      logging.info(readableMessage)
      logging.info(replyNumber)
      if ("TEMP" in readableMessage.upper()):
        temp = d.getTemperature()
        hum = d.getHumidity()
        textMessage = 'Temp={0:0.2f}C  Humidity={1:0.2f}%'.format(temp, hum)
        logging.info(textMessage)
        if ("Dummy" not in replyNumber):
          logging.info("Send Message - Temporarily Enabled.")
          modem.sendMessage(replyNumber,textMessage)
  
    logging.info("END OF READING MSG %s" % msgNumber)
  
lcd.close()
exit()




print("Modem ready.")
msgnr = 0
while True:
    print("Waiting for a new message to come in...")
    AllMessages = modem.getAllMessages()
    while ("UNREAD") not in AllMessages:
        sleep(3)
        AllMessages = modem.getAllMessages()
        print(AllMessages)

    hexmsg = modem.readMessage(msgnr)
    msg = GSMMessage(hexmsg)
    print(' Message : %s' % msg.getMessage())
    print(' Received on %s %s' % (msg.getDate(),msg.getTime()) )
    print("This is where treating the incoming message comes...")
    print()
    msgnr = msgnr + 1

# modem.deleteMessage(0)


# modem.sendMessage("+32471569206","Testing modem classes...")

