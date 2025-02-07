# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 09:47:38 2023

@author: jorgil
"""
import pyautogui 
import time

time.sleep(5)

pyautogui.write('SCANS_TO_RUN')
pyautogui.press('tab')
pyautogui.write('all')
pyautogui.press('tab', presses=3)

pyautogui.write('SYNC_REGIONS')
pyautogui.press('tab')
pyautogui.write('ashburn frankfurt sydney melbourne singapore hyderabad mumbai')
pyautogui.press('tab', presses=3)

pyautogui.write('SYNC_ENV')
pyautogui.press('tab')
pyautogui.write('prod')
pyautogui.press('tab', presses=3)
