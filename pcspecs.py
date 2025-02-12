import psutil
import platform, sys
import pyopencl as cl
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


class software:
    system = platform.system()
    release = platform.release()
    version = platform.version()


print()


platforms = cl.get_platforms()
for plat in platforms:
    print(f"Platforma: {plat.name}")
    for device in plat.get_devices():
        print(f"  Zariadenie: {device.name}")
        print(f"  Typ: {device.type}")
        print(f"  VRAM: {scale_bytes(device.global_mem_size)}")
        print(f"  Výpočtové jednotky: {device.max_compute_units}")