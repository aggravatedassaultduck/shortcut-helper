import time
import ctypes
from win32api import GetKeyState as gks
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER



previous_volume = [1.0]
sound_options = True
muted = False

# Windows API
user32 = ctypes.WinDLL('user32')

# audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
original_volume = volume_interface.GetMasterVolumeLevel()


def key_down(key):
	state = gks(key)
	return (state != 0 and state != 1)


def get_window_title(hwnd):
	'''get the title of a window handle'''
	
	length = user32.GetWindowTextLengthW(hwnd)
	if length == 0: # return an empty string if it doesn't exist
		return ""
	
	buffer = ctypes.create_unicode_buffer(length + 1)
	user32.GetWindowTextW(hwnd, buffer, length + 1)
	return buffer.value

 
def all_keys_down(keys):
	'''check if all given keys are pressed'''

	for key in keys:
		state = gks(key)
		if state == 0 or state == 1:
			return False 
		
	return True # All keys in the list are pressed.



def fade_volume(target, duration=0.2, steps=20):
	'''gradually fade the volume to whatever volume'''

	current = volume_interface.GetMasterVolumeLevelScalar()
	for i in range(steps + 1):

		interp = current + (target - current) * (i / steps)
		volume_interface.SetMasterVolumeLevelScalar(interp, None)
		time.sleep(duration / steps)




