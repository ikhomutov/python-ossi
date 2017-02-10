import os
import ossi
import re
import sys
import time

from colorama import Fore, Back

DATE = '0001ff00'
# #          S             A                   Q             W
# #: Group;  S: Grp Size;  A: Active Members;  Q: Q Length;  W: Calls Waiting


if __name__ == '__main__':
	status = ossi.Ossi()
	status.connect()
	trunks = status.list_trunks()
	last_group = int(trunks[len(trunks)-1]['800bff00'])
	pre_last_group = 0
	start_group = 1
	command = 'mon tra tru {}'
	monitor = {}

	while pre_last_group != last_group:
		t = status.command(command.format(
			pre_last_group if pre_last_group else start_group
		))
		parse = status.parse(t)
		result = status.single_to_dict(parse)
		result.pop(DATE)
		for r in result:
			if not result[r]:
				continue
			group, size, active, length, waiting = result[r].split()
			group = int(group)
			monitor.update({
				group: '%s-%s-%s-%s' % (size, active, length, waiting),
			})
			if group > pre_last_group:
				pre_last_group = group
	print(monitor)
	status.disconnect()