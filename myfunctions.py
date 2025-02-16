import winreg, subprocess, re
from importlib.metadata import version, PackageNotFoundError
def getCPUname():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        cpu_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        winreg.CloseKey(key)
        return cpu_name
    except Exception as e:
        return f"Chyba pri čítaní registra: {e}"
    

def scale_bytes(bytes, suffix="B"):
    factor = 1024

    for unit in [" ", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


def is_module_installed(module_name):
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
    
def get_gpu_info():
    import pyopencl as cl
    gpus = []
    for platform in cl.get_platforms():
        for device in platform.get_devices(device_type=cl.device_type.GPU):
            gpus.append({
                "name": device.name,
                "vram": device.global_mem_size  # VRAM v bajtoch
            })
    return gpus

