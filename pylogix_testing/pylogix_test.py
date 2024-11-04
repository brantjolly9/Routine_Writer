import pylogix
from pylogix import PLC
from pprint import pprint

ip = "192.168.11.35"
emuIP = r"192.168.56.1"

with PLC(ip_address=emuIP, port=44818) as comm:
    c = comm.conn
    g = comm.GetModuleProperties(0)
    print(g)
    
    progList = comm.GetProgramsList()
    progNames = comm.ProgramNames
    print(progList)

