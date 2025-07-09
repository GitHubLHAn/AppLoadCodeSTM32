import subprocess
import os

def flash_efr32(hex_file_path, commander_path=None, device_type=None):
    # --- 1. Xác định đường dẫn của Simplicity Commander ---
    if commander_path is None:
        # Thử các đường dẫn mặc định phổ biến cho Simplicity Commander
        # Điều chỉnh các đường dẫn này theo cài đặt của bạn
        possible_commander_paths = [
            r"C:\SiliconLabs\SimplicityCommander\commander.exe",  # Windows mặc định
            r"C:\Program Files (x86)\SiliconLabs\SimplicityCommander\commander.exe", # Windows (x86)
            "/Applications/Simplicity Commander.app/Contents/MacOS/commander", # macOS
            # Thêm các đường dẫn khác nếu cần
        ]
        
        found_commander = False
        for path in possible_commander_paths:
            if os.path.exists(path):
                commander_path = path
                found_commander = True
                break
        
        if not found_commander:
            print("Lỗi: Không tìm thấy Simplicity Commander.")
            print("Vui lòng chỉ định đường dẫn commander_path hoặc đảm bảo nó nằm trong các đường dẫn mặc định.")
            return False

    if not os.path.exists(commander_path):
        print(f"Lỗi: Đường dẫn Simplicity Commander không hợp lệ: {commander_path}")
        return False

    # --- 2. Kiểm tra tệp hex ---
    if not os.path.exists(hex_file_path):
        print(f"Lỗi: Tệp hex không tồn tại: {hex_file_path}")
        return False

    # --- 3. Xây dựng lệnh Simplicity Commander ---
    command = [commander_path, "flash", hex_file_path]

    if device_type:
        command.extend(["--device", device_type])

    print(f"\nĐang thực thi lệnh: {' '.join(command)}")

    # --- 4. Thực thi lệnh ---
    try:
        # subprocess.run sẽ chạy lệnh và đợi nó hoàn thành
        # capture_output=True để lấy stdout và stderr
        # text=True để giải mã output thành chuỗi văn bản
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # Bật kiểm tra lỗi: Nếu lệnh trả về mã lỗi khác 0, sẽ ném CalledProcessError
        )
        print("\n--- Output từ Simplicity Commander ---")
        print(process.stdout)
        if process.stderr:
            print("--- Lỗi (stderr) từ Simplicity Commander ---")
            print(process.stderr)
        
        print("\nNạp code thành công!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\nLỗi khi nạp code: Simplicity Commander trả về lỗi.")
        print(f"Mã lỗi: {e.returncode}")
        print(f"Lệnh đã thực thi: {e.cmd}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy Simplicity Commander tại đường dẫn: {commander_path}")
        print("Đảm bảo Simplicity Commander đã được cài đặt và đường dẫn chính xác.")
        return False
    except Exception as e:
        print(f"Một lỗi không mong muốn đã xảy ra: {e}")
        return False

# --- Cách sử dụng ---
if __name__ == "__main__":
    
    print("\n======================================================================================")
    print("                    NẠP CODE FIRMWARE EFR32 SILAB DÙNG FILE HEX")
    print("======================================================================================\n")

    
    # Thay thế bằng đường dẫn thực tế của tệp hex của bạn
    my_hex_file = "D:\Project_silab\Dev_main__240625\GNU ARM v12.2.1 - Default\FG23_B020_FullFunction_24062025.hex"
    
    print(f">> Path hex file: {my_hex_file}\n")
    

    my_commander_path = 'D:\Simplicity_Studio_v5__\setup\developer\\adapter_packs\commander\commander.exe'
    print(f">> Path Simplicity Commander: {my_commander_path}\n")
    
    my_device_type = "EFR32FG23B020F512IM48" 
    print(f">> Device type: {my_device_type}\n")
    
    input("> Nhấn ENTER để tiếp tục...\n")

    print(">> Bắt đầu quá trình nạp firmware EFR32...\n")
    success = flash_efr32(my_hex_file, my_commander_path, my_device_type)

    if success:
        print("Chương trình nạp hoàn tất thành công.")
    else:
        print("Chương trình nạp thất bại.")