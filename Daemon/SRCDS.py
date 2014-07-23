import socket
import struct
import time


class SourceServerError(Exception): pass


class SourceServer(object):
   # <!-- m --><a class="postlink" href="http://developer.valvesoftware.com/wiki/Source_Server_Query_Library">http://developer.valvesoftware.com/wiki ... ry_Library</a><!-- m -->
   S2C_CHALLENGE = '\x41'
   S2A_PLAYER = '\x44'
   S2A_RULES = '\x45'
   S2A_INFO = '\x49'
   A2A_ACK = '\x6A'

   A2S_INFO = '\xFF\xFF\xFF\xFF\x54Source Engine Query'
   A2S_PLAYER = '\xFF\xFF\xFF\xFF\x55'
   A2S_RULES = '\xFF\xFF\xFF\xFF\x56'
   A2S_SERVERQUERY_GETCHALLENGE = '\xFF\xFF\xFF\xFF\x57'
   A2A_PING = '\xFF\xFF\xFF\xFF\x69'

   SERVERDATA_EXECCOMMAND = 2
   SERVERDATA_AUTH = 3
   SERVERDATA_RESPONSE_VALUE = 0
   SERVERDATA_AUTH_RESPONSE = 2

   """ Class functions """
   # <!-- m --><a class="postlink" href="http://developer.valvesoftware.com/wiki/Server_Queries">http://developer.valvesoftware.com/wiki/Server_Queries</a><!-- m -->

   def __init__(self, network, port):
      self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.tcp.connect((network, port))

      self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.udp.connect((network, port))

      self.password = ''

   def settimeout(self, value):
      self.tcp.settimeout(value)
      self.udp.settimeout(value)

   def disconnect(self):
      """Disconnects from server"""
      self.tcp.close()
      self.udp.close()

   def raw_send_tcp(self, data):
      """Sends raw tcp data to the server"""
      if data:
         self.tcp.send(data)
      return self.parsePacket(self.tcp.recv(4108))

   def raw_send_udp(self, data):
      """Sends raw udp data to the server"""
      if data:
         self.udp.send(data)
      return self.udp.recv(4096)

   """ TCP """

   def setRconPassword(self, password):
      """Sets the server RCON password"""
      self.password = password

      self.raw_send_tcp(self.packet(self.SERVERDATA_AUTH, password, 1234))
      return self.raw_send_tcp(None)[1] == 1234

   def rcon(self, command):
      """Sends an RCON command to the server and returns the result"""
      # Authenticate
      if not self.setRconPassword(self.password): raise SourceServerError, 'Bad RCON password'

      # Send RCON command
      result = filter(bool, self.raw_send_tcp(self.packet(self.SERVERDATA_EXECCOMMAND, command, 1))[~0])
      return result[~0] if result else None

   """ UDP """

   def ping(self):
      """Returns the server ping in seconds"""
      starttime = time.time()
      result = self.raw_send_udp(self.A2A_PING)

      if result.startswith('\xFF\xFF\xFF\xFF') and result[4] == self.A2A_ACK:
         return time.time() - starttime

      raise SourceServerError, 'Unexpected server response \'%s\'' % result[4]

   def getChallenge(self):
      """Returns a challenge value for querying the server"""
      result = self.raw_send_udp(self.A2S_SERVERQUERY_GETCHALLENGE)
      if result.startswith('\xFF\xFF\xFF\xFF') and result[4] == self.S2C_CHALLENGE:
         return result[5:]

      raise SourceServerError, 'Unexpected server response \'%s\'' % result[4]

   def getRules(self):
      """Returns a dictionary of server rules"""
      result = self.raw_send_udp(self.A2S_RULES + self.getChallenge())

      if result.startswith('\xFF\xFF\xFF\xFF') and result[4] == self.S2A_RULES:
         rules = {}
         lines = result[7:].split('\x00')
         for x in range(0, len(lines) - 1, 2):
            rules[lines[x]] = lines[x + 1]

         return rules

      raise SourceServerError, 'Unexpected server response \'%s\'' % result[4]

   def getDetails(self):
      """Returns a dictionary of server details"""
      result = self.raw_send_udp(self.A2S_INFO)

      if result.startswith('\xFF\xFF\xFF\xFF') and result[4] == self.S2A_INFO:
         details = {}
         details['version'] = struct.unpack('<B', result[6])[0]
         lines = result[6:].split('\x00', 4)

         for name in ('server name', 'map', 'game directory', 'game description'):
            details[name] = lines.pop(0)

         line = lines.pop(0)
         (details['appid'], details['number of players'], details['maximum players'], details['number of bots'], details['dedicated'],
            details['os'], details['password'], details['secure']) = struct.unpack('<H3BccBB', line[:9])
         details['game version'] = line[9:].split('\x00')[0]

         return details

      raise SourceServerError, 'Unexpected server response \'%s\'' % result[4]

   def getPlayers(self):
      """Returns a dictionary of player information"""
      result = self.raw_send_udp(self.A2S_PLAYER + self.getChallenge())

      if result.startswith('\xFF\xFF\xFF\xFF') and result[4] == self.S2A_PLAYER:
         playercount = struct.unpack('<B', result[5])[0]

         index, x = 0, 6
         players = {}
         resultlen = len(result) # So we don't have to re-evaluate len()
         while x < resultlen:
            index = struct.unpack('<B', result[x])[0]
            if index in players:
               x += 5
               continue

            currentplayer = players[index] = {}
            y = result.find('\x00', x + 1)
            if y == -1: raise SourceServerError, 'Error parsing player information'

            currentplayer['player name'] = result[x + 1:y]
            currentplayer['kills'], currentplayer['time connected'] = struct.unpack('<BB', result[y + 1:y + 3])
            x = y + 4

         return players

      raise SourceServerError, 'Unexpected server response \'%s\'' % result[4]

   """ Data format functions """

   @staticmethod
   def packet(command, strings, request):
      """Compiles a raw packet string to send to the server"""
      if isinstance(strings, str): strings = (strings,)
      result = struct.pack('<II', request, command) + ''.join([x + '\x00' for x in strings])
      return struct.pack('<I', len(result)) + result

   @staticmethod
   def parsePacket(data):
      # Lengeth, Request, Command, Strings
      if not data: return None
      return struct.unpack('<3I', data[:12]) + (data[12:].split('\x00'),)


class MasterServerQuery(object):
   # <!-- m --><a class="postlink" href="http://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol">http://developer.valvesoftware.com/wiki ... y_Protocol</a><!-- m -->
   M2A_SERVER_BATCH = '\x66'

   REGION_US_EAST_COAST = '\x00'
   REGION_US_WEST_COAST = '\x01'
   REGION_SOUTH_AMERICA = '\x02'
   REGION_EUROPE = '\x03'
   REGION_ASIA = '\x04'
   REGION_AUSTRALIA = '\x05'
   REGION_MIDDLE_EAST = '\x06'
   REGION_AFRICA = '\x07'
   REGION_WORLD = '\xFF'

   ZERO_IP = '0.0.0.0:0'

   def __init__(self, network=('hl2master.steampowered.com', 27011)):
      self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.server.connect(network)

   def disconnect(self):
      self.server.close()

   def getServerList(self, region=None, server_filter='\x00'):
      """Returns a list of active Source servers (ip, port)"""
      if region is None: region = self.REGION_WORLD
      queryformat = '\x31' + region + '%s' + '\x00' + server_filter + '\x00'
      self.server.send(queryformat % self.ZERO_IP)

      result = []
      ip = ''
      data = self.server.recv(8192)[6:]
      while True:
         for x in range(0, len(data) - 1, 6):
            ip = struct.unpack('>BBBBH', data[x:x + 6])
            if ip == (0, 0, 0, 0, 0): return result

            result.append(('%d.%d.%d.%d' % ip[:4], ip[4]))

         self.server.send(queryformat % ('%d.%d.%d.%d:%d' % ip))
         data = self.server.recv(8192)

   @staticmethod
   def getFilterString(dedicated=False, secure=False, gamedir='', mapname='', linux=False, not_empty=False, not_full=False, proxy=False):
      """Returns a filter string for filtering query results"""
      result = ''
      if dedicated:
         result += '\\type\\d'

      if secure:
         result += '\\secure\\1'

      if gamedir:
         result += '\\gamedir\\' + gamedir

      if mapname:
         result += '\\map\\' + mapname

      if linux:
         result += '\\linux\\1'

      if not_empty:
         result += '\\empty\\1'

      if proxy:
         result += '\\full\\1'

      if proxy:
         result += '\\proxy\\1'

      return result if result else '\x00'