from load import flash_firmware
from load import detect_MCU_stlink_connected
import time
from colorama import Fore, Style

import keyboard 
import os
import sys

from datetime import datetime

import winsound

def In_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Giờ hiện tại (HH:MM:SS)
    print("(" + current_time +")")
    
print("\n======================================================================================")
print("                    Chương trình nạp code cho mạch Chute (Báo máng)")
print("======================================================================================\n")

path_App_Load_code_STM32 = os.path.dirname(os.path.abspath(__file__)) + "\\"

print(Fore.YELLOW+ "> Đường dẫn hiện tại: " + path_App_Load_code_STM32 + "Code_Chute" + Style.RESET_ALL)

files = os.listdir(path_App_Load_code_STM32 + "Code_Chute\\")

print(Fore.YELLOW+ "> Những file hex hiện có:"+ Style.RESET_ALL)

for ind in range (0, len(files)):
    print("     + " + files[ind])
    
if files == []:
    print(Fore.RED+ "-> Không phát hiện file Hex! Kết thúc chương trình!"+ Style.RESET_ALL)
    sys.exit()
    
#  Nhập vào tên file hex cần nạp
hexx = input("\n> Nhập tên file hex cần nạp (Ví dụ: lehuuan.hex): ")

if hexx in files:
    print(Fore.GREEN+ f"-> Đã tìm thấy file <{hexx}> !\n"+ Style.RESET_ALL)
else:
    print(Fore.RED+ f"-> Không tìm thấy file <{hexx}>, Kết thúc chương trình !!\n"+ Style.RESET_ALL)
    sys.exit()

firmware_path = path_App_Load_code_STM32 + "Code_Chute\\" + hexx

# ============================================================================================
print(Fore.YELLOW+"> Có xóa Flash cũ của vi điều khiển không?"+ Style.RESET_ALL)
print("      1. Có")
print("      2. Không")

while True:
    nhapxoaflash = input("> Nhập: ")
    if nhapxoaflash == "1":
        xoaflash = 1
        print("-> Có!")
        break
    elif nhapxoaflash == "2":
        xoaflash = 0
        print("-> Không")
        break
    else:
        print(Fore.RED+"-> Nhập sai, yêu cầu nhập lại!"+ Style.RESET_ALL)

# ============================================================================================
print(Fore.YELLOW+"\n> Chọn chế độ nạp?"+ Style.RESET_ALL)
print("      1. Nạp thủ công (Nhấn ENTER để nạp)")
print("      2. Nạp tự động")

while True:
    nhapCheDoNap = input("> Nhập: ")
    if nhapCheDoNap == "1":
        vManual = True
        vAutomation = False
        print("-> Nạp thủ công!")
        break
    elif nhapCheDoNap == "2":
        vManual = False
        vAutomation = True
        print("-> Nạp tự động!")
        break
    else:
        print(Fore.RED+"-> Nhập sai, yêu cầu nhập lại!"+ Style.RESET_ALL)

# ************************************************************************************************************************
# CHƯƠNG TRÌNH NẠP THỦ CÔNG, NHẤN ENTER ĐỂ NẠP
if vManual:
    print(Fore.YELLOW+"\n                *********************************************    "+ Style.RESET_ALL)
    print(Fore.YELLOW+"                *            CHẾ ĐỘ NẠP THỦ CÔNG            *    "+ Style.RESET_ALL)
    print(Fore.YELLOW+"                *********************************************    "+ Style.RESET_ALL)
    
while vManual:
    print("******************************************************************************\n")
    print(Fore.YELLOW+f"> Nhấn Enter để nạp code <{hexx}> , nhập 9 để kết thúc!"+ Style.RESET_ALL)
    i = "er"
    while i == "er":
        i = input("-> Nhập: ")  
        if i == "":
            print(Fore.YELLOW +"\n> Bắt đầu nạp code"+ Style.RESET_ALL)
        elif i == "9":
            print(Fore.YELLOW +"\n-> Kết thúc nạp Code!"+ Style.RESET_ALL)
        else:
            print(Fore.RED +"\n> Nhập sai, hãy nhập lại\n"+ Style.RESET_ALL)
            i = "er"
    
    if i == "9":
        break
    
    print(f"-> Đang trong quá trình nạp code <{hexx}>, vui lòng chờ...")
    
    kq = flash_firmware(firmware_path, xoaflash = xoaflash)
    
    if kq == 1:
        In_time()
                
        print(Fore.GREEN+f"-> Nạp firmware <{hexx}> thành công!\n"+ Style.RESET_ALL)
        winsound.Beep(3000, 500)
    else:
        In_time()
        
        print(Fore.RED+f"-> Nạp firmware <{hexx}> thất bại, yêu cầu rút St-link cắm lại!\n"+ Style.RESET_ALL)
        winsound.Beep(1000, 1000)

# # ************************************************************************************************************************
# CHƯƠNG TRÌNH NẠP TỰ ĐỘNG, RÚT RA + CẮM LẠI ĐỂ NẠP
if vAutomation:    
    start_time = time.time()
    start_time_print = time.time()    
    print(Fore.YELLOW+"\n                *********************************************    "+ Style.RESET_ALL)
    print(Fore.YELLOW+"                *   CHẾ ĐỘ NẠP TỰ ĐỘNG (Nhấn 'q' để dừng)   *    "+ Style.RESET_ALL)
    print(Fore.YELLOW+"                *********************************************    "+ Style.RESET_ALL)
    print("")
    vNextTime = True

while vAutomation: 
    time.sleep(0.01)   
    interval_time = time.time() - start_time
    interval_time_print = time.time() - start_time_print
    
    if interval_time > 0.5:   
        rs, out = detect_MCU_stlink_connected()         
        if rs:
            if vNextTime:
                print("*******************************************************************\n")
                print(f"-> Đang trong quá trình nạp code <{hexx}>, vui lòng chờ...")
    
                kq = flash_firmware(firmware_path, xoaflash = xoaflash)
                
                if kq == 1:
                    In_time()
                    print(Fore.GREEN+f"-> Nạp firmware <{hexx}> thành công, rút ra cắm lại cho lần nạp tiếp theo!\n"+ Style.RESET_ALL)
                    winsound.Beep(3000, 500)
                else:
                    In_time()   
                    print(Fore.RED+f"-> Nạp firmware <{hexx}> thất bại, yêu cầu rút St-link cắm lại!\n"+ Style.RESET_ALL)
                    winsound.Beep(1000, 1000)
                vNextTime = False
        else:
            if interval_time_print > 5:     #print every 5s
                print(Fore.RED+ out + Style.RESET_ALL )
                start_time_print = time.time()
            vNextTime = True
            
        start_time = time.time()
    
    if keyboard.is_pressed('q'):
            print("\n")
            print(Fore.YELLOW + "> Đã nhấn Exit. Kết thúc chương trình!\n" + Style.RESET_ALL)
            break  
    
    
    
    
    