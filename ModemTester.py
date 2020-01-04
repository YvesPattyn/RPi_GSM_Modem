from GSMModemClass import GSMModem
from PDUClass import GSMMessage
from time import sleep
import datetime
import logging
from LcdDisplay import lcdDisplay

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

logging.basicConfig(level=logging.INFO)
print("Initialisation of the modem in progress...")
modem = GSMModem()
modem.deleteAllMessages()

print("Initialisation of theLCD display...")
lcd = lcdDisplay()
while True:
  now = datetime.datetime.now()
  lcd.showString("Awaiting SMS .  ",LCD_LINE_1)
  lcd.showString( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) ,LCD_LINE_2)
  sleep(0.2)
  lcd.showString("Awaiting SMS .. ",LCD_LINE_1)
  sleep(0.2)
  lcd.showString("Awaiting SMS ...",LCD_LINE_1)
  sleep(0.2)
  print("READING MSG 0")
  hexmsg = modem.readMessage(0)
  if ("791" in hexmsg):
      msg = GSMMessage(hexmsg)
      print(msg.getMessage())
  print("END OF READING MSG 0")
  modem.deleteMessage(0)
  sleep(0.5)

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

