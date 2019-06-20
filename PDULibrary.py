
from bitstring import Bits
from bitstring import ConstBitStream

class GSMMessage:

    def __init__(self,HexMessage):
        self.fullStream = ConstBitStream('0x' + HexMessage)
        #Service Centre Address
        #######################

        #  Read SCA Length [1]
        self.SCALen = self.fullStream.read('int:8') - 1

        #  Read Type [1]
        self.SCATyp = self.fullStream.read('hex:8')

        #  Read Address [SCALen x 8]
        temp = self.fullStream.read('hex:%i' % (self.SCALen *8) )

        #  Format to readable phone number
        result= ""
        for x in range(1,len(temp),2):
            result = result + temp[x] + temp[x-1]
        self.SCANum = "+" + result[:result.find('f')]

        #PDU Type [1]
        self.PDUTyp = self.fullStream.read('bin:8')
        self.Multipart = self.PDUTyp[1:2]

        #Origination Address
        ####################

        #  Read Length [1]
        self.OALen = self.fullStream.read('int:8') - 5

        #  Read Type [1]
        self.OATyp = self.fullStream.read('hex:8')

        #  Read Address [OALen x8]
        temp = self.fullStream.read('hex:%i' % (self.OALen *8) )

        #  Format to readable phone number
        result= ""
        for x in range(1,len(temp),2):
            result = result + temp[x] + temp[x-1]
        self.OANum = "+" + result[:result.find('f')]

        #PDU PID [1]
        self.PID = self.fullStream.read('hex:8')

        #PDU DCS [1]
        self.DCS = self.fullStream.read('hex:8')

        #Timestamp
        ##########
        temp = self.fullStream.read('hex:56')
        #  Format Timestamp
        result= ""
        for x in range(1,len(temp),2):
            result = result + temp[x] + temp[x-1]
        self.SCTS = "20" + result
        #User Data
        ##########

        #User Data Length
        self.UDL = self.fullStream.read('uint:8')
        #User Data Header if Multipart
        if (self.Multipart == '1'):
          self.UDHL = self.fullStream.read('int:8')
          self.UDH = self.fullStream.read('hex:40')
        else:
          self.UDHL = 0
          self.UDH = ''
        #Calculate number of bits to read, make sure to read full 8 bytes.
        if ( (self.UDL % 8)!=0 ):
          bitsToRead = (self.UDL * 7) + ( 8 - (self.UDL * 7) % 8 )
        else:
          bitsToRead = self.UDL * 7
        if (self.UDHL != 0):
          bitsToRead = bitsToRead - ( 8 * (self.UDHL+1))
        print("PDU bitsToRead = %i" % bitsToRead)
        temp = self.fullStream.read('hex:%i' % bitsToRead )
        #Read User Data
        print("PDU Bytes = %s" % temp)
        #Format User Data and reverse order.
        result=''
        for x in range(0,len(temp),2):
            result = temp[x] + temp[x+1] + result
        print(result)
        print("PDU Reversed Bytes = %s" % result)
        self.UD = ConstBitStream('0x' + result)
        #Make a Bits format string in UDbin
        print("PDU len(result) = %i" %  len(result) )
        self.UDbinL = len(result) * 4
        self.UDbin = self.UD.read('bin:%i' % (self.UDbinL ))
        print("PDU UDBin = %s" % self.UDbin)
        #print('Failed to decode UD')
        #self.UDbin = '0000'
        #self.UD = 'Error'

    def getMessage(self):
        temp = self.UDbin
        Message = ''
        for x in range(0,len(self.UDbin),7):
            b = temp[x:x+7]
            t = Bits(bin='0'+b)
            Message = chr(t.int) + Message
        return Message

    def getDate(self):
        t = self.SCTS
        return t[6:8] + "-" + t[4:6] + "-" + t[0:4]

    def getTime(self):
        t = self.SCTS
        return t[8:10] + ":" + t[10:12] + ":" + t[12:14]

    def dumpData(self):
        print('SCALen    : %i' % self.SCALen)
        print('SCATyp    : %s' % self.SCATyp)
        print('SCANum    : %s' % self.SCANum)
        print('PDUTyp    : %s' % self.PDUTyp)
        print('OALen     : %i' % self.OALen)
        print('OATyo     : %s' % self.OATyp)
        print('OANum     : %s' % self.OANum)
        print('PID       : %s' % self.PID)
        print('DCS       : %s' % self.DCS)
        print('SCTS      : %s' % self.SCTS)
        print('UDHL      : %i' % self.UDHL)
        print('UDH       : %s' % self.UDH)
        print('UDL       : %i' % self.UDL)
        print('UD        : %s' % self.UD)
        print('UDbin     : %s' % self.UDbin)
        print('UDbinL    : %i' % self.UDbinL)
        print('UDbinChars: %s' % str(len(self.UDbin)/7))
        print('Date      : %s' % self.getDate())
        print('Time      : %s' % self.getTime())
        print('Message   : %s' % self.getMessage())
        print('Multipart : %s' % self.Multipart)

    def dumpShort(self):
        print('----')
        print('  Message   : %s' % self.getMessage())
        print('  Received on %s %s' % (self.getDate(),self.getTime()) )
        print('  From %s' % self.OANum)
        print('----')
