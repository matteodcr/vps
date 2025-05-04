#!/usr/bin/env python3

import json
import subprocess
import sys
import re
import os

def get_vagrant_vm_info():
    try:
        # Get VM ID
        status_output = subprocess.check_output(["vagrant", "global-status"], universal_newlines=True)
        vm_id = None
        for line in status_output.splitlines():
            if "ansible_vm" in line:
                match = re.search(r'^([a-z0-9]+)\s+', line)
                if match:
                    vm_id = match.group(1)
                    break
        
        if not vm_id:
            return {}
            
        # Get SSH config
        ssh_config = subprocess.check_output(["vagrant", "ssh-config", vm_id], universal_newlines=True)
        
        # Parse config
        host_info = {
            "ansible_connection": "ssh",
            "ansible_become": True,
            "ansible_become_user": "root"
        }
        
        for line in ssh_config.splitlines():
            line = line.strip()
            if line.startswith("HostName"):
                host_info["ansible_host"] = line.split()[1]
            elif line.startswith("User ") and not line.startswith("UserKnownHostsFile"):
                host_info["ansible_user"] = line.split()[1]
            elif line.startswith("IdentityFile"):
                host_info["ansible_ssh_private_key_file"] = line.split()[1]
                
        return {"vm_test": host_info}
    except Exception as e:
        sys.stderr.write(f"Error getting VM info: {str(e)}\n")
        return {}

def list_hosts():
    hosts = get_vagrant_vm_info()
    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "children": ["ungrouped"]
        },
        "ungrouped": {
            "hosts": list(hosts.keys())
        }
    }
    
    # Add host vars to _meta
    for hostname, vars in hosts.items():
        inventory["_meta"]["hostvars"][hostname] = vars
        
    return inventory

def get_host(hostname):
    hosts = get_vagrant_vm_info()
    return hosts.get(hostname, {})

if __name__ == "__main__":
    # Make this script executable in the shell
    if not os.access(__file__, os.X_OK):
        os.chmod(__file__, 0o755)
        
    if len(sys.argv) > 1 and sys.argv[1] == "--host":
        if len(sys.argv) != 3:
            sys.stderr.write("Usage: --host <hostname>\n")
            sys.exit(1)
        result = get_host(sys.argv[2])
    else:
        result = list_hosts()
        
    print(json.dumps(result, indent=2))