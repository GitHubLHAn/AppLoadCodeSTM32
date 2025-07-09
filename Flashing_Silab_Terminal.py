from loadcode_silab import flash_efr32

import time
from colorama import Fore, Style
# import keyboard 
import os
import sys
from datetime import datetime
import winsound

def In_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("(" + current_time +")")

def perform_flash(firmware_path, xoaflash, hexx):
    print(f"-> Đang trong quá trình nạp code <{hexx}>, vui lòng chờ...")
    kq = flash_firmware(firmware_path, xoaflash=xoaflash)
    In_time()
    if kq == 1:
        print(Fore.GREEN+f"-> Nạp firmware <{hexx}> thành công!\n"+ Style.RESET_ALL)
        winsound.Beep(3000, 500)
    else:
        print(Fore.RED+f"-> Nạp firmware <{hexx}> thất bại, yêu cầu rút St-link cắm lại!\n"+ Style.RESET_ALL)
        winsound.Beep(1000, 1000)

def select_file(files):
    for idx, fname in enumerate(files):
        print(f"     {idx+1}. {fname}")
    while True:
        try:
            file_idx = int(input("\n> Nhập số thứ tự file hex cần nạp: ")) - 1
            if 0 <= file_idx < len(files):
                hexx = files[file_idx]
                print(Fore.GREEN+ f"-> Đã chọn file <{hexx}> !\n"+ Style.RESET_ALL)
                return hexx
            else:
                print(Fore.RED+"-> Số thứ tự không hợp lệ!"+ Style.RESET_ALL)
        except ValueError:
            print(Fore.RED+"-> Vui lòng nhập số hợp lệ!"+ Style.RESET_ALL)

def ask_erase_flash():
    print(Fore.YELLOW+"> Có xóa Flash cũ của vi điều khiển không?"+ Style.RESET_ALL)
    print("      1. Có")
    print("      2. Không")
    while True:
        nhapxoaflash = input("> Nhập: ")
        if nhapxoaflash == "1":
            print("-> Có!")
            return 1
        elif nhapxoaflash == "2":
            print("-> Không")
            return 0
        else:
            print(Fore.RED+"-> Nhập sai, yêu cầu nhập lại!"+ Style.RESET_ALL)

def ask_mode():
    print(Fore.YELLOW+"\n> Chọn chế độ nạp?"+ Style.RESET_ALL)
    print("      1. Nạp thủ công (Nhấn ENTER để nạp)")
    print("      2. Nạp tự động")
    while True:
        nhapCheDoNap = input("> Nhập: ")
        if nhapCheDoNap == "1":
            print("-> Nạp thủ công!")
            return True, False
        elif nhapCheDoNap == "2":
            print("-> Nạp tự động!")
            return False, True
        else:
            print(Fore.RED+"-> Nhập sai, yêu cầu nhập lại!"+ Style.RESET_ALL)

def main():
    try:
        print("\n======================================================================================")
        print("                    CHƯƠNG TRÌNH NẠP CODE EFR32 SILAB DÙNG FILE HEX")
        print("======================================================================================\n")

        path_App_Load_code_STM32 = os.path.dirname(os.path.abspath(__file__))
        code_hex_dir = os.path.join(path_App_Load_code_STM32, "Code_Silab_Hex")
        print(Fore.YELLOW+ "> Đường dẫn hiện tại: " + code_hex_dir + Style.RESET_ALL)

        if not os.path.exists(code_hex_dir):
            print(Fore.RED+ "-> Thư mục Code_Silab_Hex không tồn tại!"+ Style.RESET_ALL)
            sys.exit()

        files = [f for f in os.listdir(code_hex_dir) if f.lower().endswith('.hex')]
        print(Fore.YELLOW+ "> Những file hex silab hiện có:"+ Style.RESET_ALL)
        if not files:
            print(Fore.RED+ "-> Không phát hiện file Hex! Kết thúc chương trình!"+ Style.RESET_ALL)
            sys.exit()

        hexx = select_file(files)
        firmware_path = os.path.join(code_hex_dir, hexx)
        xoaflash = ask_erase_flash()
        vManual, vAutomation = ask_mode()

        # Manual mode
        if vManual:
            print(Fore.YELLOW+"\n                *********************************************    "+ Style.RESET_ALL)
            print(Fore.YELLOW+"                *            CHẾ ĐỘ NẠP THỦ CÔNG            *    "+ Style.RESET_ALL)
            print(Fore.YELLOW+"                *********************************************    "+ Style.RESET_ALL)
            while True:
                print("\n*****************************************************************************")
                print(Fore.YELLOW+f"> Nhấn Enter để nạp code <{hexx}> , nhập 9 để kết thúc!"+ Style.RESET_ALL)
                i = input("-> Nhập: ")
                if i == "":
                    print(Fore.YELLOW +"\n> Bắt đầu nạp code"+ Style.RESET_ALL)
                    perform_flash(firmware_path, xoaflash, hexx)
                elif i == "9":
                    print(Fore.YELLOW +"\n->Kết thúc nạp Code!"+ Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED +"\n> Nhập sai, hãy nhập lại\n"+ Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n> Đã dừng chương trình bằng Ctrl+C\n" + Style.RESET_ALL)
        sys.exit()

if __name__ == "__main__":
    main()