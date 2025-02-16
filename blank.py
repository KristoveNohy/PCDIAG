import wmi
from myfunctions import scale_bytes
gpus = []

c = wmi.WMI()
video_controller = c.Win32_VideoController()[0]


video_controller_dict = {prop: getattr(video_controller, prop) for prop in video_controller.properties.keys()}
    
print(video_controller_dict["AdapterRAM"])