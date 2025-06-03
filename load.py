import subprocess
import time

def detect_MCU_stlink_connected():
    try:
        command = [
            r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe",
            "STM32_Programmer_CLI.exe", 
            "-l"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        
        output = result.stdout
        
        if "No ST-Link detected!" in output:
            # print("-> Không phát hiện St-Link !")
            return False, "-> Không phát hiện St-Link !"
        
        command = [
            r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe",
            "STM32_Programmer_CLI.exe", 
            "-c", 
            "port=SWD", 
            "reset=HWrst"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)

        output = result.stdout
        # print(output)
        
        if "No STM32 target found!" in output:
            # print("-> Không phát hiện vi điều khiển STM32 (No STM32 target found!)")
            return False, "-> Không phát hiện vi điều khiển STM32 (No STM32 target found!)"

        return True, "Phát hiện STM32 MCU!"
    
    except FileNotFoundError:
        print("Không tìm thấy STM32_Programmer_CLI.exe. Hãy kiểm tra biến môi trường PATH.")
        return False, "Không tìm thấy STM32_Programmer_CLI.exe. Hãy kiểm tra biến môi trường PATH."
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return False, "Lỗi không xác định."


def flash_firmware(firmware_path, port="SWD", xoaflash:int = 0):
    try:      
        
        if xoaflash == 1:        
            print("-> XÓA FLASH CŨ!\n")
            # Cấu hình lệnh CLI
            command = [
                r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe",
                "-c", "port=SWD",
                "-e", "all",
                "-w", firmware_path,
                "-v",
                "-rst",
            ]
        
        else:        
            print("-> KHÔNG XÓA FLASH CŨ!")
            # Cấu hình lệnh CLI
            command = [
                r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe",
                "-c", "port=SWD",
                # "-e", "all",
                "-w", firmware_path,
                "-v",
                "-rst",
            ]
        
        # cmd_dis = [
        #     r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe",
        #     "-c", f"port={port}",
        #     "-rst",
        #     "-disconnect"
        # ]

        # Gọi lệnh
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Kiểm tra trạng thái
        if result.returncode == 0:
            
            # result = subprocess.run(cmd_dis, capture_output=True, text=True)
            return 1
        else:
            print("Lỗi khi nạp firmware.")
            # print("Lỗi:", result.stderr)
            print("Kết quả:\n", result.stdout)
            # result = subprocess.run(cmd_dis, capture_output=True, text=True)
            return -1

    except FileNotFoundError:
        print("Không tìm thấy STM32_Programmer_CLI. Hãy kiểm tra lại đường dẫn.")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
        
        
# print("> Chế độ nạp chương trình tự động!")

# start_time = time.time()

# while True:
    
#     interval_time = time.time() - start_time
    
#     if interval_time > 3:
#         rl = detect_MCU_stlink_connected()
        
#         if rl:
#             print("-> Nạp chương trình thành công!")
#         else:
#             print("-> Nạp chương trình thất bại !")
         
#         start_time = time.time()
    
    