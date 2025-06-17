import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from load import flash_firmware, detect_MCU_stlink_connected

import winsound
import time
import datetime

class FlashApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STM32 Hex Flasher")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.hex_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Code_Hex")
        self.hex_files = [f for f in os.listdir(self.hex_dir) if f.lower().endswith('.hex')] if os.path.exists(self.hex_dir) else []

        # File selection
        ttk.Label(self, text="Choose hex file:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(self, textvariable=self.file_var, values=self.hex_files, state="readonly", width=50)
        self.file_combo.pack()

        # Erase option
        ttk.Label(self, text="Erase Flash?", font=("Arial", 12, "bold")).pack(pady=(15, 0))
        self.erase_var = tk.IntVar(value=1)
        ttk.Radiobutton(self, text="Yes", variable=self.erase_var, value=1).pack()
        ttk.Radiobutton(self, text="No", variable=self.erase_var, value=0).pack()

        # Mode option
        ttk.Label(self, text="Programming mode:", font=("Arial", 12, "bold")).pack(pady=(15, 0))
        self.mode_var = tk.StringVar(value="manual")
        ttk.Radiobutton(self, text="Manual", variable=self.mode_var, value="manual", command=self.on_mode_change).pack()
        ttk.Radiobutton(self, text="Automatic", variable=self.mode_var, value="auto", command=self.on_mode_change).pack()

        # Start and Stop buttons
        self.start_btn = ttk.Button(self, text="Start programming", command=self.start_flash)
        self.start_btn.pack(pady=10)
        self.stop_btn = ttk.Button(self, text="Stop automatic", command=self.stop_auto_mode, state="disabled")
        self.stop_btn.pack(pady=0)

        # Status
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status, foreground="blue").pack(pady=5)

        # Text box for log output
        ttk.Label(self, text="Programming log:", font=("Arial", 14, "bold")).pack(pady=(10, 0))
        self.log_text = tk.Text(self, height=15, width=120, state="disabled", wrap="word")
        self.log_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        # Control flag for auto mode
        self.auto_mode_running = False
        self.auto_thread = None

    def on_mode_change(self):
        # If switching to manual, stop auto mode if running
        if self.mode_var.get() == "manual":
            self.stop_auto_mode()

    def start_flash(self):
        hex_file = self.file_var.get()
        if not hex_file:
            messagebox.showerror("Error", "Please select a hex file!")
            return
        firmware_path = os.path.join(self.hex_dir, hex_file)
        erase = self.erase_var.get()
        mode = self.mode_var.get()
        self.start_btn.config(state="disabled")
        self.status.set("Programming...")
        if mode == "auto":
            self.stop_btn.config(state="normal")
            self.auto_mode_running = True
            self.auto_thread = threading.Thread(target=self.flash_thread, args=(firmware_path, erase, hex_file, mode), daemon=True)
            self.auto_thread.start()
        else:
            self.stop_btn.config(state="disabled")
            threading.Thread(target=self.flash_thread, args=(firmware_path, erase, hex_file, mode), daemon=True).start()

    def stop_auto_mode(self):
        self.auto_mode_running = False
        self.stop_btn.config(state="disabled")
        self.status.set("Automatic mode stopped.")

    def log(self, message, color=None):
        now = datetime.datetime.now()
        timestamp = now.strftime("(%H:%M:%S)")
        full_message = f"{timestamp} {message}"
        self.log_text.config(state="normal")
        if color:
            tag_name = f"color_{color}"
            if not tag_name in self.log_text.tag_names():
                self.log_text.tag_configure(tag_name, foreground=color)
            self.log_text.insert(tk.END, full_message + "\n", tag_name)
        else:
            self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def flash_thread(self, firmware_path, erase, hex_file, mode):
        try:
            if mode == "manual":
                rs, msgrl = detect_MCU_stlink_connected()
                if rs:
                    kq = flash_firmware(firmware_path, xoaflash=erase)
                    if kq == 1:
                        msg = f"Programming {hex_file} successful!"
                        self.status.set(msg)
                        self.log(msg, color="green")
                        winsound.Beep(3000, 500)
                    else:
                        msg = f"Programming {hex_file} failed!"
                        self.status.set(msg)
                        self.log(msg, color="red")
                        winsound.Beep(1000, 1000)
                else:
                    self.status.set(msgrl)
                    self.log(msgrl, color="red")
                    winsound.Beep(1000, 1000)
            else:  # auto
                self.status.set("Plug in St-link to program... (Press 'Stop automatic' to stop)")
                self.log("Plug in St-link to program... (Press 'Stop automatic' to stop)")
                last_log_time = 0
                while self.auto_mode_running:
                    # Wait for device to connect
                    while self.auto_mode_running:
                        rs, msg = detect_MCU_stlink_connected()
                        if rs:
                            break
                        self.status.set("Plug in St-link to program... (Press 'Stop automatic' to stop)")
                        if time.time() - last_log_time > 5:
                            self.log(msg, color="red")
                            last_log_time = time.time()
                        self.update()
                    if not self.auto_mode_running:
                        break

                    # Flash firmware
                    result = flash_firmware(firmware_path, xoaflash=erase)
                    if result == 1:
                        msg = f"Programming {hex_file} successful! Unplug and replug to program again..."
                        self.status.set(msg)
                        self.log(msg, color="green")
                        winsound.Beep(3000, 500)
                    else:
                        msg = f"Programming {hex_file} failed! Please replug St-link..."
                        self.status.set(msg)
                        self.log(msg, color="red")
                        winsound.Beep(1000, 1000)

                    # Wait for device to disconnect before next round
                    while self.auto_mode_running:
                        rs, msg = detect_MCU_stlink_connected()
                        if not rs:
                            self.status.set("Device unplugged. Plug in again to continue programming...")
                            self.log("Device unplugged. Plug in again to continue programming...")
                            self.update()
                            time.sleep(1)
                            break
                        self.status.set("Waiting for device to be unplugged... (Press 'Stop automatic' to stop)")
                        self.update()
        finally:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.auto_mode_running = False

if __name__ == "__main__":
    app = FlashApp()
    app.mainloop()