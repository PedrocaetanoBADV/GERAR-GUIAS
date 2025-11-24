import pyautogui
import time

time.sleep(6)  # espera 6 segundos antes de capturar
x, y = pyautogui.position()
print(x, y)
