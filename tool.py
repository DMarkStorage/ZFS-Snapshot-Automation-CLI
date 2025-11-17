"""
Snapshot management helper for ZFS appliances via REST API.

This utility provides CLI actions to create, remove, list, and find snapshots
for a given filesystem on a specified storage appliance. It also supports
XCP-related snapshot checks.

CLI Usage (parsed by docopt):
    tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --create
    tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --remove
    tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --xcp
    tool.py -s <STORAGE> -fs <FILESYSTEM> --xcpfind
    tool.py -s <STORAGE> -fs <FILESYSTEM> --list
    tool.py --version
    tool.py -h | --help

"""

import traceback



__version__ = '1.0'
__revision__ = '20190626'
__deprecated__ = False

from utils.parser import get_args
from utils.utils import get_projects





def main(args):
	"""
	Main entry point: routes CLI arguments to the project/filesystem workflow.

	Args:
		args (dict): Parsed CLI arguments from docopt.

	Side Effects:
		- Invokes get_projects which triggers the requested operations.
	"""
	storage = args['<STORAGE>']
	filesys = args['<FILESYSTEM>']
	snap_name = args['<SNAPSHOT>']

	get_projects(args, storage, filesys, snap_name)


if __name__ == '__main__':
	try:
		ARGS = get_args()
		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
		TRACEBACK_STR = traceback.format_exc()
		print(TRACEBACK_STR)
