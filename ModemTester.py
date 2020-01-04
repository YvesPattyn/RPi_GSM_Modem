from GSMModemClass import GSMModem
from PDUClass import GSMMessage
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)
print("Initialisation of the modem in progress...")
modem = GSMModem()
# modem.deleteAllMessages()
print("READING MSG 0")
hexmsg = modem.readMessage(0)
print(hexmsg)
print("END OF READING MSG 0")

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

