import os
import ossi
import re
import sys
import time

from colorama import Fore, Back

MAJOR = '6c02ff00'
MINOR = '6c03ff00'
WARNINGS = '6c04ff00'
TRUNKS = '6c08ff00'
STATIONS = '6c09ff00'
LINKS_UP = '6c0bff00'
LINKS_DOWN = '6c0aff00'
LOGINS = '6c0cff00'

GENERAL_INFORMATION = (
	MAJOR,
	MINOR,
	WARNINGS,
	TRUNKS,
	STATIONS,
	LINKS_UP,
	LINKS_DOWN,
	LOGINS,
)

MAPPING = {
	MAJOR: 'Major',
	MINOR: 'Minor',
	WARNINGS: 'Warnings',
	TRUNKS: 'Trunks',
	STATIONS: 'Stations',
	LINKS_UP: 'Links Up',
	LINKS_DOWN: 'Links Down',
	LOGINS: '# Logins',
	'6c0fff01': 'MediaGate 1',
	'6c0fff02': 'MediaGate 2',
	'6c0fff03': 'MediaGate 3',
	'6c0fff04': 'MediaGate 4',
	'6c0fff05': 'MediaGate 5',
	'6c0fff06': 'MediaGate 6',
	'6c0fff07': 'MediaGate 7',
	'6c0fff08': 'MediaGate 8',
	'6c10ff09': 'MediaGate 9',
	'6c10ff0a': 'MediaGate 10',
	'6c10ff0b': 'MediaGate 11',
	'6c10ff0c': 'MediaGate 12',
	'6c10ff0d': 'MediaGate 13',
	'6c10ff0e': 'MediaGate 14',
	'6c10ff0f': 'MediaGate 15',
	'6c10ff10': 'MediaGate 16',
	'6c11ff11': 'MediaGate 17',
	'6c11ff12': 'MediaGate 18',
	'6c11ff13': 'MediaGate 19',
	'6c11ff14': 'MediaGate 20',
	'6c11ff15': 'MediaGate 21',
	'6c11ff16': 'MediaGate 22',
	'6c11ff17': 'MediaGate 23',
	'6c11ff18': 'MediaGate 24',
	'6c12ff19': 'MediaGate 25',
	'6c12ff1a': 'MediaGate 26',
	'6c12ff1b': 'MediaGate 27',
	'6c12ff1c': 'MediaGate 28',
	'6c12ff1d': 'MediaGate 29',
	'6c12ff1e': 'MediaGate 30',
	'6c12ff1f': 'MediaGate 31',
	'6c12ff20': 'MediaGate 32',
	'6c13ff21': 'MediaGate 33',
	'6c13ff22': 'MediaGate 34',
	'6c13ff23': 'MediaGate 35',
	'6c13ff24': 'MediaGate 36',
	'6c13ff25': 'MediaGate 37',
	'6c13ff26': 'MediaGate 38',
	'6c13ff27': 'MediaGate 39',
	'6c13ff28': 'MediaGate 40',
}

# Gateway status constants
MG_MG = 'MG'
MG_Mj = 'Mj'
MG_Mn = 'Mn'
MG_Wn = 'Wn'
MG_Lk = 'Lk'

def parse_gate_info(gate_info):
	"""
	Args:
		gate_info (str): output information about gateway.
			Example: '29 0| 0| 1|up'

	Returns:
		dict: Separate information about gateway
			Example: {
				'MG': 29, # Gateway number (int)
				'Mj': 0, # Counts of major alarms (int)
				'Mn': 0, # Counts of minor alarms (int)
				'Wn': 1, # Counts of warnings (int)
				'Lk': True # Gateway status: up==True, other==False (bool)
			}
	"""
	list_info = list(filter(None, re.split('[ |]', gate_info)))
	link_status = True if list_info[4]=='up' else False
	result = {
		MG_MG: int(list_info[0]),
		MG_Mj: int(list_info[1]),
		MG_Mn: int(list_info[2]),
		MG_Wn: int(list_info[3]),
		MG_Lk: link_status
	}
	return result

def print_major_alarms(mj):
	"""
	Args:
		mj (int): Counts of major alarms

	Returns:
		str: Colorized information by using colorama
	"""
	if mj > 0:
		return Back.RED + Fore.WHITE + str(mj) + Fore.RESET + Back.RESET
	else:
		return Fore.GREEN + str(mj) + Fore.RESET

def print_minor_alarms(mn):
	"""
	Args:
		mn (int): Counts of minor alarms

	Returns:
		str: Colorized information by using colorama
	"""
	if mn > 0:
		return Fore.RED + str(mn) + Fore.RESET
	else:
		return Fore.GREEN + str(mn) + Fore.RESET

def print_warnings(wn):
	"""
	Args:
		wn (int): Counts of warnings

	Returns:
		str: Colorized information by using colorama
	"""
	if wn > 0:
		return Fore.YELLOW + str(wn) + Fore.RESET
	else:
		return Fore.GREEN + str(wn) + Fore.RESET



if __name__ == '__main__':
	status = ossi.Ossi()
	status.connect()
	os.system('setterm -cursor off')
	while True:
		t = status.command('sta media-g')
		output = status.single_to_dict(t)
		general = {}
		gates = []
		for key in output:
			if key in MAPPING:
				if key in GENERAL_INFORMATION:
					general.update({MAPPING[key]: output[key]})
				elif output[key]:
					gates.append(parse_gate_info(output[key]))
		os.system('clear')
		print('ALARMS SUMMARY')
		print('%s => %s' % (MAPPING[MAJOR], general[MAPPING[MAJOR]]))
		print('%s => %s' % (MAPPING[MINOR], general[MAPPING[MINOR]]))
		print('%s => %s' % (MAPPING[WARNINGS], general[MAPPING[WARNINGS]]))
		print('\nGATEWAY STATUS')
		for gate in gates:
			if gate[MG_Lk]:
				print('MG {MG}: {Mj} {Mn} {Wn}'.format(
					MG=gate[MG_MG], 
					Mj=print_major_alarms(gate[MG_Mj]), 
					Mn=print_minor_alarms(gate[MG_Mn]), 
					Wn=print_warnings(gate[MG_Wn])
				))
			else:
				print(
					Back.RED + 
					Fore.WHITE + 
					'MG ' + 
					str(gate[MG_MG]) + 
					' is DOWN' + 
					Back.RESET + 
					Fore.RESET
				)
		time.sleep(5)
	status.disconnect()