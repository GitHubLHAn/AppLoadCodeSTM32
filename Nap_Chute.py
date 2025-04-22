from load import flash_firmware
from load import detect_MCU_stlink_connected
import time
from colorama import Fore, Style

import keyboard 
import os

from datetime import datetime

import winsound

def In_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Giờ hiện tại (HH:MM:SS)
    print("(" + current_time +")")
    
# path_App_Load_code_STM32 = "C:"

path_App_Load_code_STM32 = os.path.dirname(os.path.abspath(__file__)) + "\\"

print("\n======================================================================================")
print("                    Chương trình nạp code cho mạch Chute (Báo máng)")
print("======================================================================================\n")

#  Đường dẫn đến thư mục chứa code
dir_folder_code = path_App_Load_code_STM32 + "Code_Chute\\"

# Gán đường dẫn đến các file hex
fw_path_v2_0_yody = dir_folder_code + "\Chute_Board_v2.0.hex"

fw_slave_path_v3_1 = dir_folder_code + "\Chute_Slave_FW_v3.1.hex"

fw_master_test_slave = dir_folder_code + "\Chute_Master_Fw_testSlave.hex"

fw_slave_path_v3_2 = dir_folder_code + "\Chute_Slave_FW_v3.2.hex"

fw_master_path_v3_1 = dir_folder_code + "\Chute_Master_FW_v3.1.hex"

fw_slave_path_v3_3 = dir_folder_code + "\Chute_Slave_FW_v3.3.hex"

fw_slave_path_v3_4 = dir_folder_code + "\Chute_Slave_FW_v3.4.hex"

fw_slave_path_v4_0 = dir_folder_code + "\Chute_Slave_FW_v4.0.hex"

fw_master_path_v4_0 = dir_folder_code + "\Chute_Master_FW_v4.0.hex"

fw_master_path_v3_2 = dir_folder_code + "\Chute_Master_FW_v3.2.hex"

print("> HÃY CHỌN PHIÊN BẢN NẠP:")
print("")
print("         a. Version 2.0 (Version Yody)")
print("")
print("         b. Version SLAVE 3.1 ")
print("")
print("         c. Code MASTER test line SLAVE")
print("")
print("         d. Version SLAVE 3.2")
print("")
print("         e. Version MASTER 3.1")
print("")
print("         f. Version SLAVE 3.3")
print("")
print("         g. Version SLAVE 3.4 (KV1)")
print("")
print("         h. Version SLAVE 4.0 (Kv3)")
print("")
print("         i. Version MASTER 4.0 (Kv3)")
print("")
print("         j. Version MASTER 3.2 (Kv1)")
print("")

str_version = ""

i = "er"
while i == "er":  
    i = input("-> Nhập: ")
    # ----------------------------------------------------------------------------------------------
    if i == "a":
        firmware_path = fw_path_v2_0_yody
        str_version = "======> Nạp code version 2.0 Yody"
    # ----------------------------------------------------------------------------------------------
    elif i == "b":
        firmware_path = fw_slave_path_v3_1
        str_version = "======> Nạp code mạch chute SLAVE version 3.1"
    # ----------------------------------------------------------------------------------------------
    elif i == "c":
        firmware_path = fw_master_test_slave
        str_version = "======> Nạp code mạch chute MASTER test line SLAVE"
    # ----------------------------------------------------------------------------------------------
    elif i == "d":
        firmware_path = fw_slave_path_v3_2
        str_version = "=====> Nạp code mạch chute SLAVE version 3.2 (Sửa lại chân LCD_RESET_PIN)"
    # ----------------------------------------------------------------------------------------------
    elif i == "e":
        firmware_path = fw_master_path_v3_1
        str_version = "=====> Nạp code mạch chute MASTER version 3.1"
    # ----------------------------------------------------------------------------------------------
    elif i == "f":
        firmware_path = fw_slave_path_v3_3
        str_version = "=====> Nạp code mạch chute SLAVE version 3.3 (Bổ sung bitmap)"
    # ----------------------------------------------------------------------------------------------
    elif i == "g":
        firmware_path = fw_slave_path_v3_4
        str_version = "=====> Nạp code mạch chute SLAVE version 3.4 (Bỏ nhấn nút reset và bỏ calib mode), sử dụng tại KV1"
    # ----------------------------------------------------------------------------------------------
    elif i == "h":
        firmware_path = fw_slave_path_v4_0
        str_version = "=====> Nạp code mạch chute SLAVE version 4.0 (Update từ v3.4, sử dụng tại KV3)"
    # ----------------------------------------------------------------------------------------------
    elif i == "i":
        firmware_path = fw_master_path_v4_0
        str_version = "=====> Nạp code mạch chute MASTER version 4.0 (Update từ v3.2, sử dụng tại KV3)"
    # ----------------------------------------------------------------------------------------------
    elif i == "j":
        firmware_path = fw_master_path_v3_2
        str_version = "=====> Nạp code mạch chute MASTER version 3.2 (sử dụng tại KV1, set ưu tiên ngắt + tự reset)"
    # ----------------------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------------------
    else:
        i = "er"

print("")
print(Fore.MAGENTA+str_version+ Style.RESET_ALL+ Style.RESET_ALL)
print("")

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
while vManual:
    print("******************************************************************************\n")
    print(Fore.MAGENTA+str_version+ Style.RESET_ALL)
    print(Fore.YELLOW+"> Nhấn Enter để nạp code, nhập 9 để kết thúc!"+ Style.RESET_ALL)
    i = "er"
    while i == "er":
        i = input("-> Nhập: ")  
        if i == "":
            print(Fore.YELLOW +"\n> Bắt đầu nạp code"+ Style.RESET_ALL)
        elif i == "9":
            print(Fore.YELLOW +"\n->Ket Thuc Nap Code!"+ Style.RESET_ALL)
        else:
            print(Fore.RED +"\n> Nhập sai, hãy nhập lại\n"+ Style.RESET_ALL)
            i = "er"
    
    if i == "9":
        break
    
    print("-> Đang trong quá trình nạp code, vui lòng chờ...")
    
    print("xoaflash = " + str(xoaflash))
    kq = flash_firmware(firmware_path, xoaflash = xoaflash)
    
    if kq == 1:
        In_time()
                
        print(Fore.GREEN+"->Nạp firmware thành công!\n"+ Style.RESET_ALL)
        winsound.Beep(3000, 500)
    else:
        In_time()
        
        print(Fore.RED+"->Nạp firmware thất bại, yêu cầu rút St-link cắm lại!\n"+ Style.RESET_ALL)
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
                print(Fore.MAGENTA+str_version+ Style.RESET_ALL)
                print("-> Đang trong quá trình nạp code, vui lòng chờ...")
    
                kq = flash_firmware(firmware_path, xoaflash = xoaflash)
                
                if kq == 1:
                    In_time()
                    print(Fore.GREEN+"->Nạp firmware thành công, rút ra cắm lại cho lần nạp tiếp theo!\n"+ Style.RESET_ALL)
                    winsound.Beep(3000, 500)
                else:
                    In_time()   
                    print(Fore.RED+"->Nạp firmware thất bại, yêu cầu rút St-link cắm lại!\n"+ Style.RESET_ALL)
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
    
    
    
    
    