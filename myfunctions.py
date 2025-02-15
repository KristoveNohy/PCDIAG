import winreg
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
        return f'nenajdený'

def torch_with_cuda():
    try:
        import torch.cuda.is_available
        if torch.cuda.is_available():
            cuda_version = torch.version.cuda
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "N/A"
            print(f"CUDA je dostupná. Verzia: {cuda_version}, Počet GPU: {device_count}, Prvá GPU: {device_name}")
        else:
            print("CUDA nie je dostupná.")
    except ImportError:
        print("PyTorch nie je nainštalovaný.")

torch_with_cuda()
