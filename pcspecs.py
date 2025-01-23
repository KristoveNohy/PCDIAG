import psutil
import platform, sys, GPUtil
from myfunctions import *


class cpu:

    name = getCPUname()
    physCore = psutil.cpu_count()
    logicCore = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()

	
class ram:
    __data = psutil.virtual_memory()
    total = scale_bytes(__data.total)

    def get_available(): return scale_bytes(psutil.virtual_memory().available)

class gpu:
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"Name: {gpu.name}")
        print(f"Total Memory: {gpu.memoryTotal} MB")
        print(f"Free Memory: {gpu.memoryFree} MB")
        print(f"Used Memory: {gpu.memoryUsed} MB")
        print(f"Load: {gpu.load * 100:.2f}%")
        print(f"Temperature: {gpu.temperature} °C")
        print("-" * 30)

class software:
    system = platform.system()
    release = platform.release()
    version = platform.version()


print()


print(software.release)