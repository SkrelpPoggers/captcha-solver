#Made by YaboiiDust#8251 (Discord)

import json
import numpy
import os
import subprocess
import sys
import tkinter as tk
import psutil
from ctypes import *
from ctypes.wintypes import *
from PIL import ImageGrab
import ctypes
import time
import win32gui
import win32ui
import pyautogui
import pydirectinput
from anticaptchaofficial.imagecaptcha import *


#globals for time and resets
global buff1_time
global buff2_time
global buff3_time
global buff4_time
global buff1_reset
global buff2_reset
global buff3_reset
global buff4_reset
global att1_time
global att2_time
global att3_time
global att4_time
global att1_reset
global att2_reset
global att3_reset
global att4_reset
global swim_status
global swim_left
global swim_right
global reset_swim

#set the resets to true
buff1_reset = True
buff2_reset = True
buff3_reset = True
buff4_reset = True
att1_reset = True
att2_reset = True
att3_reset = True
att4_reset = True
swim_status = True
swim_left = True
swim_right = False
reset_swim = False
#set times to initial time
buff1_time = time.time() * 1000
buff2_time = time.time() * 1000
buff3_time = time.time() * 1000
buff4_time = time.time() * 1000
att1_time = time.time() * 1000
att2_time = time.time() * 1000
att3_time = time.time() * 1000
att4_time = time.time() * 1000

#----------------------------------------------------------------------------------------
#SOLVER FUNCTIONS
#----------------------------------------------------------------------------------------
#from validator import activate_license
ALARM = 16777215
BLUE = 15641139

#auth method lol
def GetUUID():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid


process = psutil.Process(os.getpid())
def mem(): print(f'{process.memory_info().rss:,}')

# initial memory usage
mem()

def solve_captcha(file_path):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key('INSERT YOUR API KEY HERE!')
    captcha_text = solver.solve_and_return_solution(file_path)
    if captcha_text != 0:
        return captcha_text
    else:
        return 'FUCK'

def sample(dc, x, y):
    xfactor = 40
    yfactor = 1
    for i in range(5):
        for j in range(4):
            if dc.GetPixel(x + j * xfactor, y + i) != ALARM:
                return False

    return True


def hard_check(dc, x, y):
    for i in range(8):
        for j in range(100):
            if dc.GetPixel(x + j, y + i) != ALARM:
                return False

    return True


def find_text_box_ul(dc, x, y):
    while dc.GetPixel(x, y) == ALARM:
        x -= 1

    x += 1
    while dc.GetPixel(x, y) == ALARM:
        y -= 1

    return (
     x, y)


def final_verification(dc, x, y):
    i = 0
    arr = [ dc.GetPixel(x, y + 1) == ALARM for i in range(15) ]
    return numpy.all(arr)


def blue_check(dc, x, y):
    blue_list_3 = [ dc.GetPixel(x + 20 * i, y - 3) for i in range(5) ]
    blue_list_4 = [ dc.GetPixel(x + 20 * i, y - 4) for i in range(5) ]
    blue_list_5 = [ dc.GetPixel(x + 20 * i, y - 5) for i in range(5) ]
    arr = [ x == BLUE for x in blue_list_3 ]
    sol = numpy.all(arr)
    return sol

#----------------------------------------------------------------------------------------
#BACKGROUND FUNCTIONS FOR FINDING POINTER VALUES AND PRESSING KEYS
#----------------------------------------------------------------------------------------

PROCESS_ALL_ACCESS = 0x1F0FFF

def get_pid(process_name):
	pid = None
	for proc in psutil.process_iter():
		try:
			if (proc.name() == process_name):
				pid = proc.pid
		except (PermissionError, psutil.AccessDenied):
			pass
	return pid
	
def read_process_memory(pid, address, offsets, size_of_data):
    # Open the process and get the handle.
    process_handle = windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    size_of_data = 4 # Size of your data
    data = ""
    read_buff = create_string_buffer(size_of_data)
    count = c_ulong(0)
    current_address = address
    offsets.append(None) # We want a final loop where we actually get the data out, this lets us do that in one go.
    for offset in offsets:
        if not windll.kernel32.ReadProcessMemory(process_handle, current_address, cast(read_buff, LPVOID), size_of_data, byref(count)):
            return -1 # Error, so we're quitting.
        else:
            val = read_buff.value
            result = int.from_bytes(val, byteorder='little', signed=True)
            # Here that None comes into play.
            if(offset != None):
                current_address = result+offset
            else:
                windll.kernel32.CloseHandle(process_handle)
                return result



#----------------------------------------------------------------------------------------
#FUNCTIONS FOR UPDATING VALUES/PRESSING BUTTONS
#----------------------------------------------------------------------------------------
#get the game pid
game_id = get_pid("MapleStory.exe")
mapleftright = True
def update_button1():
	try:
		#get the game pid
		game_id = get_pid("MapleStory.exe")
		#base pointer
		char_bse_pointer = 0x029DB0D0
		#x coord pointers/offsets
		x_offsets = []
		x_offsets.append(0x00013A94)
		
		#get updated data from pointers/offsets
		x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
		
		b1var.set(str(x_count))
	except:
		pass

def update_button2():
	try:
		#get the game pid
		game_id = get_pid("MapleStory.exe")
		#base pointer
		char_bse_pointer = 0x029DB0D0
		#x coord pointers/offsets
		x_offsets = []
		x_offsets.append(0x00013A94)
		
		#get updated data from pointers/offsets
		x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
		
		b2var.set(str(x_count))
	except:
		pass
		
def set_map():
	if(mapcb.get() == 1):
		try:
			#get the game pid
			game_id = get_pid("MapleStory.exe")
			#base pointer
			map_base_pointer = 0x029EF390
			#map pointers/offsets
			map_offsets = []
			map_offsets.append(0x000015AC)
			
			#get updated data from pointers/offsets
			map_id_ct = read_process_memory(game_id,map_base_pointer,map_offsets,4)
			
			map_lock_id.config(text=str(map_id_ct))
		except:
			pass
	else:
		map_lock_id.config(text="0")
		
def set_pos():
	if(poscb.get() == 1):
		try:
			#get the game pid
			game_id = get_pid("MapleStory.exe")
			#base pointer
			char_bse_pointer = 0x029DB0D0
			#x coord pointers/offsets
			x_offsets = []
			x_offsets.append(0x00013A94)
			
			#get updated data from pointers/offsets
			x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
			
			pos_lock_id.config(text=str(x_count))
		except:
			pass
	else:
		pos_lock_id.config(text="0")
		
def update_labels():
	try:
		#get the game pid
		#game_id = get_pid("MapleStory.exe")
		
		#base pointers
		char_bse_pointer = 0x029DB0D0
		server_base_pointer = 0x029DB25C
		map_base_pointer = 0x029EF390
		
		mem()
		
		#attack count pointers/offsets
		atc_offsets = []
		atc_offsets.append(0x00012650)
		#x coord pointers/offsets
		x_offsets = []
		x_offsets.append(0x00013A94)
		#y coord pointers/offsets
		y_offsets = []
		y_offsets.append(0x00013A98)
		#nx pointers/offsets
		nx_offsets = []
		nx_offsets.append(0x00006CAC)
		#map pointers/offsets
		map_offsets = []
		map_offsets.append(0x000015AC)
		#get updated data from pointers/offsets
		attack_count = read_process_memory(game_id,char_bse_pointer,atc_offsets,4)
		x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
		y_count = read_process_memory(game_id,char_bse_pointer,y_offsets,4)
		nx_count = read_process_memory(game_id,server_base_pointer,nx_offsets,4)
		map_id_ct = read_process_memory(game_id,map_base_pointer,map_offsets,4)
		
		#update labels
		att_ct.config(text="AC: "+str(attack_count))
		if(x_count < 5000 and x_count > -5000):
			x_ct.config(text="X: "+str(x_count))
		if(y_count < 5000 and y_count > -5000):
			y_ct.config(text="Y: "+str(y_count))
		nx_ct.config(text="NX: "+str(nx_count))
		map_id.config(text="MID: "+str(map_id_ct))
	except:
		print("reee")
		#update labels with 0's
		att_ct.config(text="Attack Count: 0")
		x_ct.config(text="X: 0")
		y_ct.config(text="Y: 0")
		nx_ct.config(text="NX: 0")
		map_id.config(text="Map ID: 0")
		
		
		
			
	#call function again
	root.after(100,update_labels)
	
def buff_keys():
	#get window to make sure its Kastia
	window = win32gui.GetForegroundWindow()
	active_window_name = win32gui.GetWindowText(window)
	global buff1_time
	global buff2_time
	global buff3_time
	global buff4_time
	global buff1_reset
	global buff2_reset
	global buff3_reset
	global buff4_reset
	
	#BUFF KEYS------------------------------------------------------------------------------------

	#if buff1 ticked
	if(bufc1.get() == 1):
		if(buff1_reset == True):
			#set the reset to false
			buff1_reset = False
			#change the time to current time (in ms)
			buff1_time = time.time() * 1000
		
		if(buff1_reset == False):
			try:
				if(((time.time() * 1000) - buff1_time) > int(delay1_entry.get())):
					#delay has passed, time to buff again and reset timer
					if(active_window_name == "Kastia"):
						time.sleep(2)
						pydirectinput.press(buff1_entry.get())
					buff1_reset = True
			except:
				pass
	#if not ticked
	if(bufc1.get() == 0):
		#when off reset value so can be used next iteration
		if(buff1_reset != True):
			buff1_reset = True
			
	#if buff2 ticked
	if(bufc2.get() == 1):
		if(buff2_reset == True):
			#set the reset to false
			buff2_reset = False
			#change the time to current time (in ms)
			buff2_time = time.time() * 1000
		
		if(buff2_reset == False):
			try:
				if(((time.time() * 1000) - buff2_time) > int(delay2_entry.get())):
					#delay has passed, time to buff again and reset timer
					if(active_window_name == "Kastia"):
						time.sleep(2)
						pydirectinput.press(buff2_entry.get())
					buff2_reset = True
			except:
				pass
	#if not ticked
	if(bufc2.get() == 0):
		#when off reset value so can be used next iteration
		if(buff2_reset != True):
			buff2_reset = True
			
	#if buff3 ticked
	if(bufc3.get() == 1):
		if(buff3_reset == True):
			#set the reset to false
			buff3_reset = False
			#change the time to current time (in ms)
			buff3_time = time.time() * 1000
		
		if(buff3_reset == False):
			try:
				if(((time.time() * 1000) - buff3_time) > int(delay3_entry.get())):
					#delay has passed, time to buff again and reset timer
					if(active_window_name == "Kastia"):
						time.sleep(2)
						pydirectinput.press(buff3_entry.get())
					buff3_reset = True
			except:
				pass
	#if not ticked
	if(bufc3.get() == 0):
		#when off reset value so can be used next iteration
		if(buff3_reset != True):
			buff3_reset = True
			
	#if buff4 ticked
	if(bufc4.get() == 1):
		if(buff4_reset == True):
			#set the reset to false
			buff4_reset = False
			#change the time to current time (in ms)
			buff4_time = time.time() * 1000
		
		if(buff4_reset == False):
			try:
				if(((time.time() * 1000) - buff4_time) > int(delay4_entry.get())):
					#delay has passed, time to buff again and reset timer
					if(active_window_name == "Kastia"):
						time.sleep(2)
						pydirectinput.press(buff4_entry.get())
					buff4_reset = True
			except:
				pass
	#if not ticked
	if(bufc4.get() == 0):
		#when off reset value so can be used next iteration
		if(buff4_reset != True):
			buff4_reset = True
			
			
	
	
	root.after(500,buff_keys)

def att_keys():
	#get window to make sure its Kastia
	window = win32gui.GetForegroundWindow()
	active_window_name = win32gui.GetWindowText(window)
	#ATT KEYS------------------------------------------------------------------------------------
	if(active_window_name == "Kastia"):
		global att1_time
		global att2_time
		global att3_time
		global att4_time
		global att1_reset
		global att2_reset
		global att3_reset
		global att4_reset
		
		#if att1 ticked
		if(atkc1.get() == 1):
			if(att1_reset == True):
				#set the reset to false
				att1_reset = False
				#change the time to current time (in ms)
				att1_time = time.time() * 1000
			
			if(att1_reset == False):
				try:
					if(((time.time() * 1000) - att1_time) > int(atkdelay1_entry.get())):
						#delay has passed, time to buff again and reset timer
						if(active_window_name == "Kastia"):
							pydirectinput.press(atk1_entry.get())
						att1_reset = True
				except:
					pass
		#if not ticked
		if(atkc1.get() == 0):
			
			#when off reset value so can be used next iteration
			if(att1_reset != True):
				att1_reset = True
				
		#if att2 ticked
		if(atkc2.get() == 1):
			if(att2_reset == True):
				#set the reset to false
				att2_reset = False
				#change the time to current time (in ms)
				att2_time = time.time() * 1000
			
			if(att2_reset == False):
				try:
					if(((time.time() * 1000) - att2_time) > int(atkdelay2_entry.get())):
						#delay has passed, time to buff again and reset timer
						if(active_window_name == "Kastia"):
							time.sleep(0.1)
							pydirectinput.press(atk2_entry.get())
						att2_reset = True
				except:
					pass
		#if not ticked
		if(atkc2.get() == 0):
			
			#when off reset value so can be used next iteration
			if(att2_reset != True):
				att2_reset = True
				
		#if att3 ticked
		if(atkc3.get() == 1):
			if(att3_reset == True):
				#set the reset to false
				att3_reset = False
				#change the time to current time (in ms)
				att3_time = time.time() * 1000
			
			if(att3_reset == False):
				try:
					if(((time.time() * 1000) - att3_time) > int(atkdelay3_entry.get())):
						#delay has passed, time to buff again and reset timer
						if(active_window_name == "Kastia"):
							time.sleep(0.1)
							pydirectinput.press(atk3_entry.get())
						att3_reset = True
				except:
					pass
		#if not ticked
		if(atkc3.get() == 0):
			
			#when off reset value so can be used next iteration
			if(att3_reset != True):
				att3_reset = True
				
		#if att4 ticked
		if(atkc4.get() == 1):
			if(att4_reset == True):
				#set the reset to false
				att4_reset = False
				#change the time to current time (in ms)
				att4_time = time.time() * 1000
			
			if(att4_reset == False):
				try:
					if(((time.time() * 1000) - att4_time) > int(atkdelay4_entry.get())):
						#delay has passed, time to buff again and reset timer
						if(active_window_name == "Kastia"):
							time.sleep(0.1)
							pydirectinput.press(atk4_entry.get())
						att4_reset = True
				except:
					pass
		#if not ticked
		if(atkc4.get() == 0):
			
			#when off reset value so can be used next iteration
			if(att4_reset != True):
				att4_reset = True
	root.after(40,att_keys)

def extras():
	#get window to make sure its Kastia
	window = win32gui.GetForegroundWindow()
	active_window_name = win32gui.GetWindowText(window)
	if(active_window_name == "Kastia"):
		#offsets and pointers needed for these
		#base pointers
		char_bse_pointer = 0x029DB0D0
		map_base_pointer = 0x029EF390
		#attack count pointers/offsets
		atc_offsets = []
		atc_offsets.append(0x00012650)
		#x coord pointers/offsets
		x_offsets = []
		x_offsets.append(0x00013A94)
		#map pointers/offsets
		map_offsets = []
		map_offsets.append(0x000015AC)
		#--------------------------
		#MAP LOCK
		#---------------------------
		#if map ID is different from locked map and cb is checked
		if(mapcb.get() == 1):
			map_id_ct = read_process_memory(game_id,map_base_pointer,map_offsets,4)
			#if map id found and text label set are not the same then uncheck everything
			if(str(map_id_ct) != str(map_lock_id.cget("text"))):
				global mapleftright
				buff_c1.deselect()
				buff_c2.deselect()
				buff_c3.deselect()
				buff_c4.deselect()
				atk_c1.deselect()
				atk_c2.deselect()
				atk_c3.deselect()
				atk_c4.deselect()
				swim_c1.deselect()
				swim_c2.deselect()
				if(mapleftright == True):
					pydirectinput.press('left')
					time.sleep(0.05)
					pydirectinput.press('right')
					time.sleep(0.05)
					pydirectinput.press(swim_entry.get())
					
					mapleftright = False
		if(mapcb.get() == 0):
			mapleftright = True
					
		#--------------------------
		#POS LOCK
		#---------------------------
		if(poscb.get() == 1):
			x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
			#if the person is 300 away to the right from original position or greater move left until within 100ish
			if(x_count > int(pos_lock_id.cget("text")) + 200):
				while(x_count > int(pos_lock_id.cget("text")) + 100):
					#move left then reread value
					pydirectinput.keyDown('left')
					x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
				pydirectinput.press('left')
				time.sleep(0.05)
				pydirectinput.press('shift')
			#if the person is 300 away to the left from original position or greater move right until within 100ish
			if(x_count < int(pos_lock_id.cget("text")) - 200):
				while(x_count < int(pos_lock_id.cget("text")) - 100):
					#move right then reread value
					pydirectinput.keyDown('right')
					x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
				pydirectinput.press('right')
				time.sleep(0.05)
				pydirectinput.press('shift')
		#--------------------------
		#SWIMMER LOGIC
		#---------------------------
		#moving part
		if(swimc1.get() == 1):
			global reset_swim
			reset_swim = True
			x_count = read_process_memory(game_id,char_bse_pointer,x_offsets,4)
			#if they are actual integers
			if(str(b1var.get()) != "Left" and str(b2var.get()) != "Right"):
				global swim_status
				global swim_left
				global swim_right
				if(x_count <= int(b1var.get())):
					pydirectinput.keyUp('left')
					pydirectinput.keyDown('right')
					swim_right = True
					swim_left = False	
				elif(x_count > int(b1var.get()) and x_count < int(b2var.get())):
					if(swim_left == True):
						pydirectinput.keyDown('left')
						pydirectinput.keyUp('right')
					elif(swim_right == True):
						pydirectinput.keyUp('left')
						pydirectinput.keyDown('right')
				elif(x_count >= int(b2var.get())):
					pydirectinput.keyUp('right')
					pydirectinput.keyDown('left')
					swim_left = True
					swim_right = False
		if(swimc1.get() == 0):
			if(reset_swim == True):
				pydirectinput.press('shift')
				pydirectinput.press('left')
				pydirectinput.press('right')
				reset_swim = False
				
		#attacking part
		if(swimc2.get() == 1):
			pydirectinput.keyDown(swim_entry.get())
		if(swimc2.get() == 0):
			pydirectinput.keyUp(swim_entry.get())
		
		
		
		#--------------------------
		#ATTACK COUNT RESET
		#---------------------------
		attack_count = read_process_memory(game_id,char_bse_pointer,atc_offsets,4)
		#check attack count and do stuff
		if(attack_count > 90):
			time.sleep(1)
			pydirectinput.press('left')
			time.sleep(0.05)
			pydirectinput.press('left')
			time.sleep(0.05)
			pydirectinput.press('right')
			time.sleep(0.05)
			pydirectinput.press('right')
			time.sleep(0.5)
			if(bufc1.get() == 1):
				pydirectinput.press(buff1_entry.get())
			
	root.after(400,extras)

def solver():
	#get window to make sure its Kastia
	window = win32gui.GetForegroundWindow()
	active_window_name = win32gui.GetWindowText(window)
	captcha_label.config(text="Window not active, not scanning for captcha")
	if(active_window_name == "Kastia"):
		window_name = 'Kastia'
		wd = win32ui.FindWindow(None, window_name)
		try:
			captcha_label.config(text="Waiting for Captcha")
			dc = wd.GetWindowDC()
			x = 200
			y = 100
			while y <= 715:
				while x <= 800:
					px = dc.GetPixel(x, y)
					if px == ALARM:
						if sample(dc, x, y):
							ldfound = hard_check(dc, x, y)
							if ldfound:
								oldx = x
								oldy = y
								x, y = find_text_box_ul(dc, x, y)
								if final_verification(dc, x, y) and blue_check(dc, x, y):
									#stop all movement (only necessary for swimming I think since this is full blocking function when detected)
									#if swimming checked stop movement and attacking
									pydirectinput.press('f3')
									if(swimc1.get() == 1 or swimc2.get() == 1):
										pydirectinput.press('left')
										time.sleep(0.05)
										pydirectinput.press('right')
										time.sleep(0.05)
										pydirectinput.press(swim_entry.get())
									
									
									captcha_label.config(text="Lie detector found!!!! Now solving captcha..")
									print("LD Found")
									#print('Lie detector found!!!! Now solving captcha..')
									image_file_path = 'captcha.jpg'
									w_l, w_t, _, _ = wd.GetWindowRect()
									pic_x = x + w_l
									pic_y = y + w_t
									ld_captcha = ImageGrab.grab(bbox=(pic_x - 2, pic_y - 52, pic_x + 200, pic_y))
									ld_captcha.save(image_file_path, 'JPEG')
									#click on the text box to get ready for input
									pydirectinput.moveTo(pic_x + 75, pic_y+10)
									time.sleep(1)
									pydirectinput.doubleClick()
									#update label with processing then process
									captcha_label.config(text="Processing Captcha")
									solved_captcha = solve_captcha(image_file_path)
									#process logic
									#processed with no output
									if solved_captcha == 'FUCK':
										solved_captcha = ''
									#processed equation
									if '=' in solved_captcha:
										cut_string = solved_captcha.split('=')
										cut_string = cut_string[0]
										if 'x' in cut_string:
											number_set = cut_string.split('x')
											if len(number_set) >= 2:
												solved_captcha = str(int(number_set[0]) * int(number_set[1]))
										else:
											try:
												solved_captcha = str(eval(cut_string))
											except:
												print("Failed solving math equation.")
									#click again just to make sure the mouse hasn't moved or something
									pydirectinput.moveTo(pic_x + 75, pic_y+10)
									time.sleep(1)
									pydirectinput.doubleClick()
									#put detection here for if there is an error
									if(len(solved_captcha) < 7 and solved_captcha != ''):
										for i in solved_captcha:
											try:
												i = i.lower()
											except:
												pass
											pydirectinput.press(i)
											time.sleep(.5)
										pydirectinput.press('enter')
										time.sleep(2)
										pydirectinput.press('enter')
									#update label with solved captcha
									captcha_label.config(text=str(solvedcaptcha))
									print(solvedcaptcha)
									#sleep for 2 seconds just so everything is good
									pydirectinput.doubleClick()
									pydirectinput.press('f3')
									time.sleep(2)


								x = oldx
								y = oldy
					x += 60

				x = 350
				y += 5

		except:
			#put somehting here to detect
			pass
		
	root.after(1000,solver)

#GUI STUFF BELOW --------------------------

root = tk.Tk()
root.title('Discord')

#creating all frames
buffframe = tk.Frame(root,width=250,height=200,padx=2,pady=2)
attackframe = tk.Frame(root,width=250,height=200,padx=2,pady=2)
p2pframe = tk.Frame(root,width=250,height=200,padx=2,pady=2)
lock2mapframe = tk.Frame(root,width=250,height=50,padx=2,pady=2)
solverframe = tk.Frame(root,width=250,height=50,padx=2,pady=2)
statsframe = tk.Frame(root,width=250,height=20,padx=2,pady=2)

#layout frames and root
#root
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
#others
buffframe.grid(row=0)
attackframe.grid(row=1)
p2pframe.grid(row=2)
lock2mapframe.grid(row=3)
solverframe.grid(row=4)
statsframe.grid(row=5)

#all variables
#for buff frame checks
bufc1 = tk.IntVar()
bufc2 = tk.IntVar()
bufc3 = tk.IntVar()
bufc4 = tk.IntVar()
#attack frame checks
atkc1 = tk.IntVar()
atkc2 = tk.IntVar()
atkc3 = tk.IntVar()
atkc4 = tk.IntVar()
#p2p fram checks
swimc1 = tk.IntVar()
swimc2 = tk.IntVar()
#for tkinter buttons
b1var = tk.StringVar()
b2var = tk.StringVar()
#for map lock
mapcb = tk.IntVar()
poscb = tk.IntVar()
#default texts for attack and buffs delays
buff1_delay_text = tk.StringVar()
buff2_delay_text = tk.StringVar()
buff3_delay_text = tk.StringVar()
buff4_delay_text = tk.StringVar()
att1_delay_text = tk.StringVar()
att2_delay_text = tk.StringVar()
att3_delay_text = tk.StringVar()
att4_delay_text = tk.StringVar()
buff_delay_ms = "60000"
att_delay_ms = "100"
#default texts for att and buff and swim keys
buff1_key_text = tk.StringVar()
buff2_key_text = tk.StringVar()
buff3_key_text = tk.StringVar()
buff4_key_text = tk.StringVar()
att1_key_text = tk.StringVar()
att2_key_text = tk.StringVar()
att3_key_text = tk.StringVar()
att4_key_text = tk.StringVar()
swim1_key_text = tk.StringVar()
swim2_key_text = tk.StringVar()
b1_def = "a"
b2_def = "s"
b3_def = "d"
b4_def = "f"
a1_def = "a"
a2_def = "s"
a3_def = "d"
a4_def = "f"
swim_def1 = "ctrl"
swim_def2 = "100"

#----------------------------------------------------------------------------------------
#BUFF FRAME STUFF HERE
#----------------------------------------------------------------------------------------
#create widgets in buff frame
#title of section
buff_title = tk.Label(buffframe, text='Buffs',font='Helvetica 10 bold')
#key labels
buff1_lbl = tk.Label(buffframe, text='Key:')
buff1_lb2 = tk.Label(buffframe, text='Key:')
buff1_lb3 = tk.Label(buffframe, text='Key:')
buff1_lb4 = tk.Label(buffframe, text='Key:')
#entry boxes for att keys
buff1_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff1_key_text)
buff2_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff2_key_text)
buff3_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff3_key_text)
buff4_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff4_key_text)
#key labels
delay_lbl = tk.Label(buffframe, text='Delay(ms):')
delay_lb2 = tk.Label(buffframe, text='Delay(ms):')
delay_lb3 = tk.Label(buffframe, text='Delay(ms):')
delay_lb4 = tk.Label(buffframe, text='Delay(ms):')
#entry boxes for delays
delay1_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff1_delay_text)
delay2_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff2_delay_text)
delay3_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff3_delay_text)
delay4_entry = tk.Entry(buffframe,width = 10,borderwidth=1,relief="solid", textvariable = buff4_delay_text)
#enable checks
buff_c1 = tk.Checkbutton(buffframe, text='Enable', variable=bufc1,onvalue = 1, offvalue = 0, command=None)
buff_c2 = tk.Checkbutton(buffframe, text='Enable', variable=bufc2,onvalue = 1, offvalue = 0, command=None)
buff_c3 = tk.Checkbutton(buffframe, text='Enable', variable=bufc3,onvalue = 1, offvalue = 0, command=None)
buff_c4 = tk.Checkbutton(buffframe, text='Enable', variable=bufc4,onvalue = 1, offvalue = 0, command=None)

#layout buff section
buff_title.grid(row=0,column=0,padx=3,pady=3)
#key lables
buff1_lbl.grid(row=1,column=0,padx=3,pady=3)
buff1_lb2.grid(row=2,column=0,padx=3,pady=3)
buff1_lb3.grid(row=3,column=0,padx=3,pady=3)
buff1_lb4.grid(row=4,column=0,padx=3,pady=3)
#entry boxes for keys
buff1_entry.grid(row=1,column=1,padx=3,pady=3)
buff2_entry.grid(row=2,column=1,padx=3,pady=3)
buff3_entry.grid(row=3,column=1,padx=3,pady=3)
buff4_entry.grid(row=4,column=1,padx=3,pady=3)
#delay lables
delay_lbl.grid(row=1,column=2,padx=3,pady=3)
delay_lb2.grid(row=2,column=2,padx=3,pady=3)
delay_lb3.grid(row=3,column=2,padx=3,pady=3)
delay_lb4.grid(row=4,column=2,padx=3,pady=3)
#entry boxes for delays
delay1_entry.grid(row=1,column=3,padx=3,pady=3)
delay2_entry.grid(row=2,column=3,padx=3,pady=3)
delay3_entry.grid(row=3,column=3,padx=3,pady=3)
delay4_entry.grid(row=4,column=3,padx=3,pady=3)
#enable checks
buff_c1.grid(row=1,column=4,padx=3,pady=3)
buff_c2.grid(row=2,column=4,padx=3,pady=3)
buff_c3.grid(row=3,column=4,padx=3,pady=3)
buff_c4.grid(row=4,column=4,padx=3,pady=3)

#set delay texts
buff1_delay_text.set(buff_delay_ms)
buff2_delay_text.set(buff_delay_ms)
buff3_delay_text.set(buff_delay_ms)
buff4_delay_text.set(buff_delay_ms)
#set key texts
buff1_key_text.set(b1_def)
buff2_key_text.set(b2_def)
buff3_key_text.set(b3_def)
buff4_key_text.set(b4_def)
#----------------------------------------------------------------------------------------
#ATTACK FRAME STUFF HERE
#----------------------------------------------------------------------------------------
#create widgets in buff frame
#title of section
atk_title = tk.Label(attackframe, text='Attack Keys (Non-Moving)',font='Helvetica 10 bold')
#key labels
atk1_lbl = tk.Label(attackframe, text='Spam:')
atk1_lb2 = tk.Label(attackframe, text='Key:')
atk1_lb3 = tk.Label(attackframe, text='Key:')
atk1_lb4 = tk.Label(attackframe, text='Key:')
#entry boxes for att keys
atk1_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att1_key_text)
atk2_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att2_key_text)
atk3_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att3_key_text)
atk4_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att4_key_text)
#key labels
atkdelay_lbl = tk.Label(attackframe, text='Delay(ms):')
atkdelay_lb2 = tk.Label(attackframe, text='Delay(ms):')
atkdelay_lb3 = tk.Label(attackframe, text='Delay(ms):')
atkdelay_lb4 = tk.Label(attackframe, text='Delay(ms):')
#entry boxes for delays
atkdelay1_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att1_delay_text)
atkdelay2_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att2_delay_text)
atkdelay3_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att3_delay_text)
atkdelay4_entry = tk.Entry(attackframe,width = 10,borderwidth=1,relief="solid", textvariable = att4_delay_text)
#enable checks
atk_c1 = tk.Checkbutton(attackframe, text='Enable', variable=atkc1,onvalue = 1, offvalue = 0, command=None)
atk_c2 = tk.Checkbutton(attackframe, text='Enable', variable=atkc2,onvalue = 1, offvalue = 0, command=None)
atk_c3 = tk.Checkbutton(attackframe, text='Enable', variable=atkc3,onvalue = 1, offvalue = 0, command=None)
atk_c4 = tk.Checkbutton(attackframe, text='Enable', variable=atkc4,onvalue = 1, offvalue = 0, command=None)

#layout buff section
atk_title.grid(row=0,columnspan=3,padx=7,pady=3,sticky="w")
#key lables
atk1_lbl.grid(row=1,column=0,padx=3,pady=3)
atk1_lb2.grid(row=2,column=0,padx=3,pady=3)
atk1_lb3.grid(row=3,column=0,padx=3,pady=3)
atk1_lb4.grid(row=4,column=0,padx=3,pady=3)
#entry boxes for keys
atk1_entry.grid(row=1,column=1,padx=3,pady=3)
atk2_entry.grid(row=2,column=1,padx=3,pady=3)
atk3_entry.grid(row=3,column=1,padx=3,pady=3)
atk4_entry.grid(row=4,column=1,padx=3,pady=3)
#delay lables
atkdelay_lbl.grid(row=1,column=2,padx=3,pady=3)
atkdelay_lb2.grid(row=2,column=2,padx=3,pady=3)
atkdelay_lb3.grid(row=3,column=2,padx=3,pady=3)
atkdelay_lb4.grid(row=4,column=2,padx=3,pady=3)
#entry boxes for delays
atkdelay1_entry.grid(row=1,column=3,padx=3,pady=3)
atkdelay2_entry.grid(row=2,column=3,padx=3,pady=3)
atkdelay3_entry.grid(row=3,column=3,padx=3,pady=3)
atkdelay4_entry.grid(row=4,column=3,padx=3,pady=3)
#enable checks
atk_c1.grid(row=1,column=4,padx=3,pady=3)
atk_c2.grid(row=2,column=4,padx=3,pady=3)
atk_c3.grid(row=3,column=4,padx=3,pady=3)
atk_c4.grid(row=4,column=4,padx=3,pady=3)

#set delay texts
att1_delay_text.set(att_delay_ms)
att2_delay_text.set(att_delay_ms)
att3_delay_text.set(att_delay_ms)
att4_delay_text.set(att_delay_ms)
#set key texts
att1_key_text.set(a1_def)
att2_key_text.set(a2_def)
att3_key_text.set(a3_def)
att4_key_text.set(a4_def)
#----------------------------------------------------------------------------------------
#P2P STUFF HERE
#----------------------------------------------------------------------------------------
#create widgets in buff frame
#title of section
p2p_title = tk.Label(p2pframe, text='Swimmer Macro (NOTE: CANT HAVE ANYTHING ON SHIFT)',font='Helvetica 8 bold')
#buttons
b1 = tk.Button(p2pframe,textvariable=b1var,command=update_button1,relief="groove",width=10)
b2 = tk.Button(p2pframe,textvariable=b2var,command=update_button2,relief="groove",width=10)
#set button text
b1var.set("Left")
b2var.set("Right")
#enable checks
swim_c1 = tk.Checkbutton(p2pframe, text='Enable', variable=swimc1,onvalue = 1, offvalue = 0, command=None)

#key label
swim_lbl = tk.Label(p2pframe, text='Hold:')
#entry boxes for att keys
swim_entry = tk.Entry(p2pframe,width = 10,borderwidth=1,relief="solid", textvariable = swim1_key_text)
#delay label
swimdelay_lbl = tk.Label(p2pframe, text='Delay(ms):')
#entry boxes for swim att delay
swimdelay1_entry = tk.Entry(p2pframe,width = 10,borderwidth=1,relief="solid", textvariable = swim2_key_text)
#enable check for swim att
swim_c2 = tk.Checkbutton(p2pframe, text='Enable', variable=swimc2,onvalue = 1, offvalue = 0, command=None)


#layout top of swim section
p2p_title.grid(row=0,columnspan=5,padx=11,pady=3,sticky="w")
#buttons
b1.grid(row=1,column=0,columnspan=2,padx=(13,3),pady=3,sticky="ew")
b2.grid(row=1,column=2,columnspan=2,padx=(22,3),pady=3,sticky="ew")
#enable check
swim_c1.grid(row=1,column=4,padx=3,pady=3)

#bottom row of swim section
swim_lbl.grid(row=2,column=0,padx=(12,3),pady=3)
swim_entry.grid(row=2,column=1,padx=3,pady=3)
swimdelay_lbl.grid(row=2,column=2,padx=3,pady=3)
swimdelay1_entry.grid(row=2,column=3,padx=3,pady=3)
swim_c2.grid(row=2,column=4,padx=3,pady=3)

#set key texts
swim1_key_text.set(swim_def1)
swim2_key_text.set(swim_def2)

#----------------------------------------------------------------------------------------
#STATS STUFF HERE
#----------------------------------------------------------------------------------------
#stats labels
x_ct = tk.Label(statsframe, text='X: 0')
y_ct = tk.Label(statsframe, text='Y: 0')
att_ct = tk.Label(statsframe, text='AC: 0')
nx_ct = tk.Label(statsframe, text='NX: 0')
map_id = tk.Label(statsframe, text='MID: 0')

#stats grids
x_ct.grid(row=0,column=0,padx=3,pady=3,sticky="ew")
y_ct.grid(row=0,column=1,padx=3,pady=3,sticky="ew")
att_ct.grid(row=0,column=2,padx=3,pady=3,sticky="ew")
nx_ct.grid(row=0,column=3,padx=3,pady=3,sticky="ew")
map_id.grid(row=0,column=4,padx=3,pady=3,sticky="ew")

#----------------------------------------------------------------------------------------
#MAP/POSITION LOCK STUFF HERE
#----------------------------------------------------------------------------------------
#check box
map_lock_cb = tk.Checkbutton(lock2mapframe, text='Lock Map', variable=mapcb,onvalue = 1, offvalue = 0, command=set_map)
pos_lock_cb = tk.Checkbutton(lock2mapframe, text='Lock Pos', variable=poscb,onvalue = 1, offvalue = 0, command=set_pos)
#label
map_lock_id = tk.Label(lock2mapframe, text='0')
pos_lock_id = tk.Label(lock2mapframe, text='0')

#grid
map_lock_cb.grid(row=0,column=2,padx=3,pady=3,sticky="e")
pos_lock_cb.grid(row=0,column=0,padx=3,pady=3,sticky="e")
map_lock_id.grid(row=0,column=3,columnspan=2,padx=3,pady=3)
pos_lock_id.grid(row=0,column=1,padx=3,pady=3)
#----------------------------------------------------------------------------------------
#CAPTCHA STUFF HERE
#----------------------------------------------------------------------------------------
#label
captcha_label = tk.Label(solverframe, text='')
#grid
captcha_label.grid(row=0,column=0,columnspan=5,padx=3,pady=3,sticky="ew")

#start stat count and main loop
#stat function
root.after(100,update_labels)
root.after(400,buff_keys)
root.after(40,att_keys)
root.after(400,extras)
root.after(1000,solver)


#auth for program
root.mainloop()
