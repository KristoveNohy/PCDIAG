import winreg, subprocess, re

# def getCPUname():
#     try:
#         key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
#         cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
#         winreg.CloseKey(key)
#         return cpu_name
#     except Exception as e:
#         return f"Chyba pri čítaní registra: {e}"
    

def scale_bytes(bytes, suffix="B"):
    factor = 1024

    for unit in [" ", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


def is_module_installed(module_name):
    from importlib.metadata import version, PackageNotFoundError
    try:
        return version(module_name)
    except PackageNotFoundError:
        return f'nie je'


def is_cuda():
    try:
        output = subprocess.check_output("nvidia-smi", shell=True, stderr=subprocess.STDOUT)
        output = output.decode("utf-8")
        # Hlada riadok obsahujúci "CUDA Version:"
        match = re.search(r"CUDA Version:\s+([\d\.]+)", output)
        if match:
            return match.group(1)
        return "nie je"
    except Exception:
        return "nie je"

def is_cudnn():
    try:
        import ctypes

        cudnn = ctypes.cdll.LoadLibrary("cudnn.dll")
       
        cudnn_version = cudnn.cudnnGetVersion()
        # Rozloží číslo do častí (predpokladám formát: major*1000 + minor*100 + patch)
        major = cudnn_version // 1000
        minor = (cudnn_version % 1000) // 100
        patch = cudnn_version % 100
        return f"{major}.{minor}.{patch}"
    except Exception:
        return "nie je"
    


def get_system_info():
    import wmi
    w = wmi.WMI()
    info = {
        "cpu": {},
        "ram": [],
        "storage": [],
        "gpu": []
    }

    # CPU
    for cpu in w.Win32_Processor():
        info["cpu"] = {
            "name": cpu.Name,
            "cores": cpu.NumberOfCores,
            "logical_processors": cpu.NumberOfLogicalProcessors,
            "max_clock_speed_mhz": cpu.MaxClockSpeed
        }

    # RAM
    import psutil
    for mem in w.Win32_PhysicalMemory():
        info["ram"].append({
            "size_gb": int(mem.Capacity) / (1024**3),
            "type": mem.MemoryType,
            "speed_mhz": mem.Speed,
            "manufacturer": mem.Manufacturer,
        })


    # Storage
    for disk in w.Win32_DiskDrive():
        info["storage"].append({
            "model": disk.Model,
            "interface": disk.InterfaceType,
            "serial_number": disk.SerialNumber.strip(),
            "size_gb": int(disk.Size) / (1024**3),
            "media_type": disk.MediaType,
            "firmware_version": disk.FirmwareRevision,
            "rpm": disk.SpindleSpeed if hasattr(disk, "SpindleSpeed") else "N/A"
        })


    # GPU
    for gpu in w.Win32_VideoController():
        info["gpu"].append({
            "name": gpu.Name,
            "driver_version": gpu.DriverVersion,
            "sm_count": "Nemožno zistiť",
            "cuda_cores": "Nemožno zistiť",
            "cuda_cp": "Nemožno zistiť"
        })
    import pyopencl as cl
    for platform in cl.get_platforms():
        for i, device in enumerate(platform.get_devices(device_type=cl.device_type.GPU)):
            
            info["gpu"][i].update({
                "opencl": device.version,
                "CU": device.max_compute_units,
                "clock": device.max_clock_frequency,
                "vram": device.global_mem_size  # VRAM v bajtoch
            })

    if is_cuda()  != "nie je":
        CUDA_CORES_PER_SM = {
            3: 192,  # Kepler
            5: 128,  # Maxwell
            6: 64,   # Pascal
            7: 64,   # Volta
            75: 64,  # Turing
            8: 128,  # Ampere
            9: 128   # Lovelace
        }


        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,clocks.sm,multiprocessors", "--format=csv,noheader,nounits"],
            encoding="utf-8"
        )
        lines = output.strip().split("\n")
        

        for index, line in enumerate(lines):
            parts = line.split(", ")
            name = parts[0]
            sm_count = int(parts[2])  # Počet multiprocesorov

            # Odhadneme počet CUDA jadier podľa známej architektúry
            major_arch = int(sm_count / 10) if sm_count > 100 else sm_count  # Približný odhad architektúry
            cores_per_sm = CUDA_CORES_PER_SM.get(major_arch, 64)  # Ak nepoznáme, použijeme default 64
            total_cuda_cores = sm_count * cores_per_sm

            info["gpu"][index].update({
                "sm_count": sm_count,
                "cuda_cores": total_cuda_cores
                
            })
            try:
                import pycuda.driver
                info["gpu"][index].update({
                    "cuda_cp": pycuda.driver.Device(index).compute_capability(),
                })
            except Exception:
                pass

    return info

def memtotext(num):
    match num:
        case 24:
            return "DDR3"
        case 26:
            return "DDR4"
        case 34:
            return "DDR5"
        case default:
            return "Neznámy"
print(get_system_info())
