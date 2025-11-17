import json
import os
import csv
import requests
from .parser import get_headers

data = {}

def create_filesystem_inventory(data, out_name):
    """
    Create CSV and JSON exports of filesystem inventory data.

    Args:
        data (dict): Inventory data containing filesystem details.
        out_name (str): Base name for output files (without extension).
    Side Effects:
        Writes 'out_name.csv' and 'out_name.json' files.
    """
    filesystems_payload = data['snapshots']
    data_file = open(f'{out_name}.csv', 'w')
    csv_writer = csv.writer(data_file)


    header_written = 0
    for item in filesystems_payload:
        if header_written == 0:
            header_row = item.keys()
            csv_writer.writerow(header_row)
            header_written += 1
        csv_writer.writerow(item.values())
    data_file.close()

    # Creating json file
    with open(f'{out_name}.json', 'w') as outfile:
        json.dump(filesystems_payload, outfile, indent=2)
	
def get_projects(args, storage, filesys, snap_name):
	"""
	Retrieve filesystem inventory and dispatch the requested action.

	Looks up the target filesystem within the appliance and, depending on CLI
	flags, performs one of the supported operations (create/remove/list/find).

	Args:
		args (dict): Parsed CLI arguments.
		storage (str): Storage appliance hostname or IP.
		filesys (str): Filesystem name to operate on.
		snap_name (str): Snapshot name (for create/remove/xcp checks).

	Side Effects:
		- Prints booleans / messages according to operations.
		- Triggers downstream functions that may write CSV/JSON files.
	"""
	filesystems_seen = []
	headers = get_headers()
	base_url = 'https://{}:215'.format(storage)
	url = '{}/api/storage/v1/filesystems'.format(base_url)

	resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
	json_resp = resp.json()
	data.update(json_resp)
    
	for item in data['filesystems']:
		filesystems_seen.append(item['name'])

	if filesys in filesystems_seen:
		for item in data['filesystems']:
			if item['name'] == filesys:
				pool = item['pool']
				filesys = item['name']
				project = item['project']
				# returns TRue if snap is created in the filesystem
				if args['--create']:
					newsnap(storage, pool, project, filesys, snap_name)
				# returns list of snap present in the filesystem
				elif args['--list']:
					list(storage, pool, project, filesys)
				# returns TRue if specific snap deleted in the filesystem
				elif args['--remove']:
					remove(storage, pool, project, filesys, snap_name)
				# returns TRue if xcp snap present in the filesystem
				elif args['--xcpfind']:
					find(storage, pool, project, filesys)
				# returns TRue if specific xcp snap present in the filesystem
				elif args['--xcp']:
					find_xcp(storage, pool, project, filesys, snap_name)
	else:
		print("Filesystem not Found!")

def newsnap(storage, pool, project, filesys, snap_name):
	"""
	Create a new snapshot and export current snapshot inventory.

	Attempts to create the snapshot. If the snapshot already exists (HTTP 409),
	it still exports the latest snapshot inventory. Prints True (as bool(1)) on
	success/duplicate, False (bool(0)) otherwise.

	Args:
		storage (str): Storage appliance hostname or IP.
		pool (str): Storage pool identifier.
		project (str): Project identifier.
		filesys (str): Filesystem name.
		snap_name (str): Snapshot name to create.

	Side Effects:
		- Prints bool(1) on 201/409, otherwise bool(0).
		- Creates/overwrites 'datafile.csv' and 'datafile.json'.
	"""
	response_data = {}
	headers = get_headers()
	base_url = f'https://{storage}:215'

	payload = {
		"name": snap_name,
		"retention": "unlocked"
	}
	json_dump = json.dumps(payload)
	url = f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots'

	resp = requests.post(url=url, data=json_dump, verify=False, headers=headers, timeout=30)
	newresp = requests.get(url=url, verify=False, headers=headers, timeout=30)
	json_resp = newresp.json()
	response_data.update(json_resp)

	if resp.status_code == 201 or resp.status_code == 409:
		print(bool(1)); create_filesystem_inventory(response_data, 'datafile')

	else:
		print(bool(0))
		
def list(storage, pool, project, filesys):
	"""
	List snapshots for a given filesystem and export results.

	Fetches snapshots, prints a formatted JSON list, and writes both CSV and JSON
	exports (datafile.csv, datafile.json) to the current working directory.

	Args:
		storage (str): Storage appliance hostname or IP.
		pool (str): Storage pool identifier.
		project (str): Project identifier.
		filesys (str): Filesystem name.

	Side Effects:
		- Prints snapshot listing or "No SNAPSHOT found!".
		- Creates/overwrites 'datafile.csv' and 'datafile.json'.
	"""
	response_data = {}
	headers = get_headers()
	base_url = 'https://{}:215'.format(storage)

	url = f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots'

	resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
	json_resp = resp.json()
	response_data.update(json_resp)

	if len(response_data['snapshots']) != 0:
		printed_json = json.dumps(response_data, indent=2)
		print('\n')
		print("~"*10+"List of Snapshots"+"~"*10+ "\n\t")
		print(printed_json)

		# Creating csv file 
		create_filesystem_inventory(response_data, 'datafile')

	else:
		print("No SNAPSHOT found!")
		
def remove(storage, pool, project, filesys, snap_name):
	"""
	Delete a specific snapshot and export the remaining inventory.

	Args:
		storage (str): Storage appliance hostname or IP.
		pool (str): Storage pool identifier.
		project (str): Project identifier.
		filesys (str): Filesystem name.
		snap_name (str): Snapshot name to delete.

	Side Effects:
		- Prints bool(1) on HTTP 204 success, otherwise bool(0).
		- Creates/overwrites 'datafile.csv' and 'datafile.json' with current inventory.
	"""
	response_data = {}
	headers = get_headers()
	base_url = 'https://{}:215'.format(storage)
	
	delete_url =  f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots/{snap_name}?confirm=true'
	
	list_url = f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots'


	resp = requests.delete(url=delete_url, verify=False, headers=headers, timeout=30)
	newresp = requests.get(url=list_url, verify=False, headers=headers, timeout=30)
	json_resp = newresp.json()
	response_data.update(json_resp)

	if resp.status_code == 204:
		print(f"Snapshot deleted!")
		print(bool(1)); create_filesystem_inventory(response_data, 'datafile')

	else:
		print(bool(0))


def find(storage, pool, project, filesys):
	"""
	Check if any snapshot starting with 'xcp' exists for the filesystem.

	Prints True (bool(1)) if at least one snapshot begins with 'xcp',
	otherwise prints False (bool(0)). If no snapshots exist at all, prints a message.

	Args:
		storage (str): Storage appliance hostname or IP.
		pool (str): Storage pool identifier.
		project (str): Project identifier.
		filesys (str): Filesystem name.

	Side Effects:
		- Prints a boolean or 'No SNAPSHOT found!' message.
	"""
	response_data = {}
	headers = get_headers()
	base_url = 'https://{}:215'.format(storage)
	
	url = f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots'

	resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
	json_resp = resp.json()
	response_data.update(json_resp)

	snapshots = resp.json().get("snapshots", [])
	if not snapshots:
		print("No SNAPSHOT found!")
		exit(0)
	for s in resp.json().get("snapshots", []):
		name = s.get("name", "")
		if name.startswith("xcp"):
			print(bool(1)); break
	else:
		print(bool(0))


def find_xcp(storage, pool, project, filesys, snap_name):
	"""
	Check for an exact 'xcp' snapshot name; create it if absent.

	Behavior:
	- If 'snap_name' exists in the snapshot list, prints True (bool(1)).
	- Otherwise, prints a creation message and attempts to create it.

	Args:
		storage (str): Storage appliance hostname or IP.
		pool (str): Storage pool identifier.
		project (str): Project identifier.
		filesys (str): Filesystem name.
		snap_name (str): Exact snapshot name to search for (and possibly create).

	Side Effects:
		- Prints boolean or progress messages.
		- May create a new snapshot and export CSV/JSON via `newsnap`.
	"""
	
	headers = get_headers()
	base_url = f'https://{storage}:215'
	url = f'{base_url}/api/storage/v1/pools/{pool}/projects/{project}/filesystems/{filesys}/snapshots'
	resp = requests.get(url=url, verify=False, headers=headers, timeout=30)
	snapshots = resp.json().get("snapshots", [])
	if not snapshots:
		print("No SNAPSHOT found!")
		exit(0)
    # Early exit: check if snap_name exists without building full list
	for snapshot in snapshots:
		if snapshot.get('name') == snap_name:
			print(bool(1))
			break
		else:
			print("Creating Snapshot ....\n")
			newsnap(storage, pool, project, filesys, snap_name)
            