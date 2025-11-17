from docopt import docopt


def get_headers():
	"""
	Build and return request headers for the appliance REST API.

	Returns:
		dict: A dictionary containing HTTP headers including content
		      type, accept headers, and X-Auth credentials.
	"""
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Auth-User": 'root',
		"X-Auth-Key": 'password'
	}
	return headers


def get_args():
	"""
	Parse command-line arguments using docopt, based on the embedded usage text.

	Returns:
		dict: Parsed arguments from the CLI.
	"""
	usage = """
	Usage:
		tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --create
		tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --remove
		tool.py -s <STORAGE> -fs <FILESYSTEM> -sp <SNAPSHOT> --xcp
		tool.py -s <STORAGE> -fs <FILESYSTEM> --xcpfind		
		tool.py -s <STORAGE> -fs <FILESYSTEM> --list		
		tool.py --version
		tool.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name
	"""
	args = docopt(usage)
	return args	
