import telnetlib

#TODO: Add comments

CMD = 'c'
FLD = 'f'
DSC = 'd'
EOF = 't'
END = EOF + '\n'

class Ossi():
	def __init__(self, settings):
		#TODO: Add assertions
		self.host = settings['host']
		self.port = settings['port']
		self.username = settings['username']
		self.password = settings['password']
		self.pin = settings['pin']

	def write_string(self, string):
		self.tn.write(string.encode())
		self.tn.write('\n'.encode())

	def write_command(self, command):
		string = CMD + command
		self.write_string(string)

	def write_field(self, field):
		string = FLD + field
		self.write_string(string)

	def write_descript(self, desc):
		string = DSC + desc
		self.write_string(string)

	def write_eof(self):
		self.write_string(EOF)

	def inline(self, output):
		lines = output.split('\n')
		return lines

	def parse(self, output):
		"""
		returns: dict
		{
			'fields': {
				1: str,
				2: str,
				3: str
			},
			'descriptors':{
				1: str,
				2: str,
				3: str
			}
		}
		"""
		fields = {}
		descriptors = {}
		lines = self.inline(output)
		for line in lines:
			if line.startswith(CMD):
				pass
			elif line.startswith(DSC):
				descriptors.update({
					len(descriptors): line[1:]
				})
			elif line.startswith(FLD):
				fields.update({
					len(fields): line[1:]
				})
			elif line.startswith(EOF):
				break
			else:
				pass
		result = {
			'fields': fields,
			'descriptors': descriptors,
		}
		return result

	def single_to_dict(self, output):
		result = {}
		parse = self.parse(output)
		for i in range(len(parse['fields'])):
			flds = parse['fields'][i].split('\t')
			dscs = parse['descriptors'][i].split('\t')
			if len(flds) != len(dscs):
				print('ERROR')
				break
			for i in range(len(flds)):
				result.update({
					flds[i]: dscs[i]
				})
		return result

	def multiple_to_dict(self, output):
		result = {}
		parse = self.parse(output)
		fields = parse['fields']
		descriptors = parse['descriptors']
		instances = {}
		result = {}
		count = 0
		while len(descriptors):
			inc = len(result) * len(fields)
			instance = {}
			for key in fields:
				instance.update({fields[key]: descriptors.pop(key + inc, None)})
			instances.update({count: instance})
			count += 1
		for inst in instances:
			new_instance = {}
			for i in inst:
				abc = {}
				flds = i.split('\t')
				dscs = inst[i].split('\t')
				if len(flds) != len(dscs):
					print('ERROR')
					break
				for k in range(len(flds)):
					abc.update({
						flds[i]: dscs[i]
					})
			result.update({inst: new_instance})
		return result

	def command(self, command, params=None):
		self.write_command(command)
		if params:
			fields = ''
			descriptors = ''
			for key in params:
				fields += '\t%s' % key
				descriptors += '\t%s' % params[key]
			self.write_field(fields)
			self.write_descript(descriptors)
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