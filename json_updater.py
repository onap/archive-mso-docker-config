#!/usr/bin/env python3
import json
import os
import sys

#chef_update_string = '{"default_attributes": {"asdc-connections": {"asdc-controller1": {"environmentName": "test"}}}}'
#json_file_to_update="./volumes/mso/chef-config/mso-docker.json"

def usage():
    print('Usage:')
    print("    echo <json> | %s <file> " % ( sys.argv[0], ))
    print()
    print("file\tpath of the valid json file to update")
    print("json\ta json string containing the values to update in <file>")
    print("")
    print("Example : ")
    print(""" 
    echo '{"default_attributes": {"asdc-connections": {"asdc-controller1": {"environmentName": "test"}}}}' | %s ./volumes/mso/chef-config/mso-docker.json
    """ % (sys.argv[0]))

    
if len(sys.argv) < 2:
    usage()
    exit(1)
    
if sys.argv[1] in ('--help','-h'):
    usage()
    exit(0)
    
# get updates
updates_json = sys.stdin.read()
print(updates_json[81:])
updates = json.loads(updates_json)

# get file to update
json_file_to_update = sys.argv[1]
with open(json_file_to_update) as f:
    to_update = json.load(f)
    
# update config with updates
def update(config, updates):
    #assert isinstance(config, dict)
    #assert isinstance(updates, dict)

    # if key is a simple type, update it. Otherwise, update sub values


    for update_key,update_value in updates.items():
        if update_key not in config:
            raise Exception('Incorrect parameter : %s' % (update_key,))        
        if isinstance(update_value, (int, str)):
            config[update_key] = update_value
        elif isinstance (update_value,list) and isinstance (config[update_key],list):
            config[update_key] = update_value
        else:
            update(config[update_key], update_value)

update(to_update, updates)

# replace the file
tmp_file = '%s.tmp' % (json_file_to_update,)
with open(tmp_file, 'w') as f:
    json.dump(to_update, f,  sort_keys=True, indent=2)
os.rename(tmp_file, json_file_to_update)

