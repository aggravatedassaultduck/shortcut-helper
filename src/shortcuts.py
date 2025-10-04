import time
import ctypes
from win32api import GetKeyState as gks
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import pyautogui
import pyscreenshot as ImageGrab
import io
import win32clipboard
import helpers as hlp



previous_volume = [1.0]
muted = False

# Windows API
user32 = ctypes.WinDLL('user32')

# audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
original_volume = volume_interface.GetMasterVolumeLevel()




def handle_mute(keys):
	'''mute all sounds whilst given key is being held down'''
	
	if hlp.all_keys_down(keys):  # End key pressed
		if not bool(volume_interface.GetMute()):
			
			# Save current volume
			previous_volume[0] = volume_interface.GetMasterVolumeLevelScalar()
			hlp.fade_volume(0.0)
			volume_interface.SetMute(True, None)
			
	else:  # End key released
		if bool(volume_interface.GetMute()):
			
			volume_interface.SetMute(False, None)
			hlp.fade_volume(previous_volume[0])



def sc_copy(keys):
	'''take a screenshot and copy it to clipboard'''

	if hlp.all_keys_down(keys):  # Alt+S
		
		im = ImageGrab.grab()
		output = io.BytesIO()
		im.save(output, 'BMP')
		data = output.getvalue()[14:]
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
		win32clipboard.CloseClipboard()


def close_window(keys):
	'''minimize focused window'''

	hwnd = ctypes.windll.user32.GetForegroundWindow()
	title = hlp.get_window_title(hwnd)


	if hlp.all_keys_down(keys):
		ctypes.windll.user32.ShowWindow(hwnd, 6)
		pyautogui.click()