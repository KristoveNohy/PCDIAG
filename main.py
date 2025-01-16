import psutil
import platform, os, sys
from myfunctions import *



def cpuinfo():
    cpu_name = getCPUname()
    physCore = psutil.cpu_count()
    logicCore = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()
    print()
	



cpuinfo()