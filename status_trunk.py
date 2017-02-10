import os
import ossi
import re
import sys
import time

from colorama import Fore, Back

MEMBER = '0001ff00'
PORT = '0002ff00'
STATE = '0003ff00'
MTCE = '0004ff00'
CONNECTED = '0005ff00'


MAPPING = {
	MEMBER: 'Member',
	PORT: 'Port',
	STATE: 'State',
	MTCE: 'Mtce',
	CONNECTED: 'Connected ports',
	'3e81ff00': 'Unknown',
	'3e82ff00': 'Unknown',
	'3e83ff00': 'Unknown',
}


if __name__ == '__main__':
	status = ossi.Ossi()
	status.connect()
	t = status.command('sta tru 2')
	parse = status.parse(t)

	result = status.multiple_to_dict(parse)
	for i in range(len(result)):
		member = result[i]
		print('%s(%s) => %s' % (member[MEMBER], member[PORT], member[STATE]))

	status.disconnect()