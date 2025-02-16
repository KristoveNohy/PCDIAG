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
    
def get_gpu_names():
    gpu_names = []
    try:
        import wmi
        c = wmi.WMI()
        for gpu in c.Win32_VideoController():
            gpu_names.append(gpu.Name)
    except ImportError:
        gpu_names.append("WMI modul nie je nainštalovaný")
    return gpu_names

