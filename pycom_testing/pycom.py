import pycomm3
from pycomm3 import LogixDriver
import time
import json

startTime = time.process_time()
ipAddress = "192.168.11.35"

with LogixDriver(ipAddress) as drive:
    jsonTags = drive.tags_json
    for key, val in jsonTags:
        with open(f"JSON_TAGS\\{key}.json", "x") as jf:
            json.dump(val, jf, indent=3)
    plcinfo = drive.get_plc_info()
    modInfo = drive.get_module_info(1)
    g = drive.list_identity(ipAddress)
    print(g)

stopTime = time.process_time()

print(f"Elapsed: {(stopTime - startTime) * 10**3}ms")


#drive.close()