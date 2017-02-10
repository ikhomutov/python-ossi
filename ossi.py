import telnetlib
#TODO: Add try-except
import settings

#TODO: Add comments and docstrings

CMD = 'c'
FID = 'f'
DATA = 'd'
ERR = 'e'
EOF = 't'
END = EOF + '\n'

class Ossi():
	def __init__(self):
		#TODO: Add assertions
		self.host = settings.HOST
		self.port = settings.PORT
		self.username = settings.USERNAME
		self.password = settings.PASSWORD
		self.pin = settings.PIN

	def write_string(self, string):
		self.tn.write(string.encode())
		self.tn.write('\n'.encode())

	def write_command(self, command):
		string = CMD + command
		self.write_string(string)

	def write_field(self, field):
		string = FID + field
		self.write_string(string)

	def write_data(self, desc):
		string = DATA + desc
		self.write_string(string)

	def write_eof(self):
		self.write_string(EOF)

	def inline(self, output):
		lines = output.split('\n')
		return lines

	def parse(self, output):
		"""
		Returns: 
			dict
		{
			'fields': {
				1: str,
				2: str,
				3: str
			},
			'data':{
				1: str,
				2: str,
				3: str
			}
		}
		"""
		fields = {}
		data = {}
		lines = self.inline(output)
		for line in lines:
			if line.startswith(CMD):
				pass
			elif line.startswith(DATA):
				data.update({
					len(data): line[1:]
				})
			elif line.startswith(FID):
				fields.update({
					len(fields): line[1:]
				})
			elif line.startswith(ERR):
				# TODO: Add error handler
				pass
			elif line.startswith(EOF):
				break
			else:
				pass
		result = {
			'fields': fields,
			'data': data,
		}
		return result

	def single_to_dict(self, parse):
		result = {}
		for i in range(len(parse['fields'])):
			fids = parse['fields'][i].split('\t')
			data = parse['data'][i].split('\t')
			if len(fids) != len(data):
				# print('ERROR')
				break
			for i in range(len(fids)):
				result.update({
					fids[i]: data[i]
				})
		return result

	def multiple_to_dict(self, parse):
		fields = parse['fields']
		data = parse['data']
		instances = {}
		result = {}
		count = 0

		while len(data):
			inc = count * len(fields)
			instance_data = {}
			for key in fields:
				instance_data.update({
					key: data.pop(key + inc, None)
					})
			instance = {
				'fields': fields,
				'data': instance_data
			}
			instances.update({count: instance})
			count += 1
		for inst in instances:
			result.update({
				inst: self.single_to_dict(instances[inst])
				})

		return result

	def command(self, command, params=None):
		self.write_command(command)
		# TODO: Add connection lost handler
		if params:
			fields = ''
			data = ''
			for key in params:
				fields += '\t%s' % key
				data += '\t%s' % params[key]
			self.write_field(fields)
			self.write_descript(data)
		self.write_eof()
		output_bytes = self.tn.read_until(END.encode())
		return output_bytes.decode('utf-8')

	def connect(self):
		self.tn = telnetlib.Telnet(self.host, self.port)
		self.tn.read_until('login'.encode())
		self.write_string(self.username)
		self.tn.read_until('Password'.encode())
		self.write_string(self.password)	
		self.tn.read_until('Pin'.encode())
		self.write_string(self.pin)
		self.tn.read_until('Terminal'.encode())
		self.write_string('ossi')

		self.tn.read_until(EOF.encode())
		print('Connected')

	def disconnect(self):
		self.tn.close()
		print('Disconnected')