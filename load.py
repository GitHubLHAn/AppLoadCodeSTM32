import subprocess
import os

def get_stm32_cli_path():
    config_file = os.path.join(os.path.dirname(__file__), "path_STM32_CLI.txt")
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            path = f.readline().strip()
            if path:
                return path
    except Exception as e:
        print(f"Lỗi đọc file cấu hình STM32 CLI: {e}")
    # Fallback default if file not found or empty
    return r"D:"

STM32_CLI_PATH = get_stm32_cli_path()

# STM32_CLI_PATH = r"D:\Program Storage\CUBE_PROG__\setup\bin\STM32_Programmer_CLI.exe"


def detect_MCU_stlink_connected():
    try:
        command = [
            STM32_CLI_PATH, 
            "-l"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        
        output = result.stdout
        
        if "No ST-Link detected!" in output:
            return False, "-> Không phát hiện St-Link !"
        
        command = [
            STM32_CLI_PATH, 
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
                STM32_CLI_PATH,
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
                STM32_CLI_PATH,
                "-c", "port=SWD",
                "-w", firmware_path,
                "-v",
                "-rst",
            ]

        # Gọi lệnh
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Kiểm tra trạng thái
        if result.returncode == 0:
            # Load code thành công
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
        
    
    