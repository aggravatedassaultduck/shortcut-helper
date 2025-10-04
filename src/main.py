#TODO: restructure, remapping, custom shortcuts
import time
import pyautogui
from loader import plugins, sound_options

import shortcuts as sh

last_move = time.time()
running = True

def anti_afk():
	global last_move
	if time.time() - last_move > 420:
		pyautogui.moveRel(1, 0, duration=0.1)
		pyautogui.moveRel(-1, 0, duration=0.1)
		last_move = time.time()


def main():
	while running:
		anti_afk()

		for plugin, keys in plugins.items():
			if plugin == sh.handle_mute and not sound_options:
				continue
			plugin(keys)

		time.sleep(0.1)

if __name__ == '__main__':
	main()
