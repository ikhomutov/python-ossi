import colorama
import os
import ossi
import sys
import time


settings = {
	'host': '10.200.177.71',
	'port': '5023',
	'username': 'dadmin',
	'password': 'dadmin1',
	'pin': 'dadmin1',
}

MAPPING = {
	'6c02ff00': 'Major',
	'6c08ff00': 'Trunks',
	'6c0aff00': 'Links Down',
	'6c0cff00': '# Logins',
	'6c03ff00': 'Minor',
	'6c0bff00': 'Links Up',
	'6c04ff00': 'Warnings',
}

if __name__ == '__main__':
	test = ossi.Ossi(settings)
	test.connect()
	t = test.command('sta tru 1')
	import ipdb
	ipdb.set_trace()
	output = test.multiple_to_dict(t)
	print(output)
	test.disconnect()