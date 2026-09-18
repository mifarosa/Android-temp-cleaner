#!/usr/bin/env python3
"""
Android Temp File Cleaner
A GUI application to clean temporary files from Android devices via ADB
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
from datetime import datetime


# Language translations
LANGUAGES = {
    "TR": {
        "title": "Android Temp Dosya Temizleyici",
        "device_selection": "Cihaz Seçimi",
        "refresh_devices": "🔄 Cihazları Yenile",
        "clean_temp": "🗑️ Temp Dosyaları Temizle",
        "check_size": "📊 Dosya Boyutunu Kontrol Et",
        "log": "İşlem Günlüğü",
        "ready": "Hazır",
        "checking_adb": "ADB varlığı kontrol ediliyor...",
        "adb_found": "ADB bulundu",
        "adb_not_found": "HATA: ADB bulunamadı! ADB'nin kurulu ve PATH'de olduğundan emin olun.",
        "adb_error_title": "ADB Bulunamadı",
        "adb_error_msg": "ADB (Android Debug Bridge) sisteminizde bulunamadı.\n\nLütfen Android SDK Platform Tools'u indirip PATH'e ekleyin.",
        "scanning_devices": "Bağlı cihazlar taranıyor...",
        "scanning": "Cihazlar aranıyor...",
        "device_list_error": "Cihaz listesi alınamadı",
        "device_error": "Hata: Cihazlar listelenemedi",
        "devices_found": "cihaz bulundu",
        "devices_ready": "cihaz hazır",
        "no_devices": "Hiç cihaz bulunamadı. USB debugging aktif mi?",
        "no_device_found": "Cihaz bulunamadı",
        "select_device": "Uyarı",
        "select_device_msg": "Lütfen bir cihaz seçin",
        "checking_size": "Temp klasör boyutu kontrol ediliyor",
        "calculating": "Dosya boyutu hesaplanıyor...",
        "size_title": "Klasör Boyutu",
        "size_msg": "Temp klasör boyutu",
        "location": "Konum",
        "size_error": "Hata",
        "size_error_msg": "Dosya boyutu kontrol edilemedi",
        "error_occurred": "Hata oluştu",
        "confirm_clean": "Onay",
        "confirm_clean_msg": "Seçili cihazın temp dosyalarını temizlemek istediğinizden emin misiniz?",
        "confirm_device": "Cihaz",
        "confirm_location": "Konum",
        "confirm_warning": "Bu işlem geri alınamaz!",
        "cleaning_started": "Temizlik başlatılıyor",
        "cleaning": "Temp dosyaları temizleniyor...",
        "cleaning_success": "✓ Temp dosyaları başarıyla temizlendi!",
        "success_title": "Başarılı",
        "success_msg": "Temp dosyaları başarıyla temizlendi!\n\nKonum",
        "cleaning_error": "Temizlik hatası",
        "cleaning_failed": "Temizlik sırasında hata oluştu",
        "process_error": "İşlem hatası",
        "unexpected_error": "Beklenmeyen hata",
        "cleaning_complete": "Temizlik tamamlandı",
    },
    "EN": {
        "title": "Android Temp File Cleaner",
        "device_selection": "Device Selection",
        "refresh_devices": "🔄 Refresh Devices",
        "clean_temp": "🗑️ Clean Temp Files",
        "check_size": "📊 Check Folder Size",
        "log": "Operation Log",
        "ready": "Ready",
        "checking_adb": "Checking ADB availability...",
        "adb_found": "ADB found",
        "adb_not_found": "ERROR: ADB not found! Make sure ADB is installed and in PATH.",
        "adb_error_title": "ADB Not Found",
        "adb_error_msg": "ADB (Android Debug Bridge) is not installed on your system.\n\nPlease download Android SDK Platform Tools and add it to PATH.",
        "scanning_devices": "Scanning connected devices...",
        "scanning": "Searching devices...",
        "device_list_error": "Device list could not be retrieved",
        "device_error": "Error: Could not list devices",
        "devices_found": "devices found",
        "devices_ready": "devices ready",
        "no_devices": "No devices found. Is USB debugging enabled?",
        "no_device_found": "No devices found",
        "select_device": "Warning",
        "select_device_msg": "Please select a device",
        "checking_size": "Checking temp folder size",
        "calculating": "Calculating file size...",
        "size_title": "Folder Size",
        "size_msg": "Temp folder size",
        "location": "Location",
        "size_error": "Error",
        "size_error_msg": "Could not check file size",
        "error_occurred": "Error occurred",
        "confirm_clean": "Confirm",
        "confirm_clean_msg": "Are you sure you want to clean temp files from selected device?",
        "confirm_device": "Device",
        "confirm_location": "Location",
        "confirm_warning": "This operation cannot be undone!",
        "cleaning_started": "Starting cleanup",
        "cleaning": "Cleaning temp files...",
        "cleaning_success": "✓ Temp files cleaned successfully!",
        "success_title": "Success",
        "success_msg": "Temp files cleaned successfully!\n\nLocation",
        "cleaning_error": "Cleaning error",
        "cleaning_failed": "Error occurred during cleaning",
        "process_error": "Process error",
        "unexpected_error": "Unexpected error",
        "cleaning_complete": "Cleanup completed",
    }
}


class AndroidTempCleaner:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        
        # Language selection
        self.language = tk.StringVar(value="TR")
        self.show_language_selection()
        
    def show_language_selection(self):
        """Show language selection window"""
        lang_window = tk.Toplevel(self.root)
        lang_window.title("Dil Seçimi / Language Selection")
        lang_window.geometry("400x200")
        lang_window.resizable(False, False)
        
        # Center the window
        lang_window.transient(self.root)
        lang_window.grab_set()
        
        # Label
        label = tk.Label(
            lang_window,
            text="Lütfen dili seçin\nPlease select a language",
            font=("Segoe UI", 12, "bold"),
            pady=20
        )
        label.pack()
        
        # Buttons frame
        button_frame = tk.Frame(lang_window)
        button_frame.pack(pady=20)
        
        def select_tr():
            self.language.set("TR")
            lang_window.destroy()
            self.continue_init()
            
        def select_en():
            self.language.set("EN")
            lang_window.destroy()
            self.continue_init()
        
        tr_btn = tk.Button(
            button_frame,
            text="🇹🇷 Türkçe",
            font=("Segoe UI", 11, "bold"),
            width=15,
            height=2,
            command=select_tr,
            bg="#FF6B35",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )
        tr_btn.pack(side=tk.LEFT, padx=10)
        
        en_btn = tk.Button(
            button_frame,
            text="🇬🇧 English",
            font=("Segoe UI", 11, "bold"),
            width=15,
            height=2,
            command=select_en,
            bg="#FF6B35",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )
        en_btn.pack(side=tk.LEFT, padx=10)
        
        # Center on parent window
        lang_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - lang_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - lang_window.winfo_height()) // 2
        lang_window.geometry(f"+{x}+{y}")
    
    def continue_init(self):
        """Continue initialization after language selection"""
        self.root.title(self.t("title"))
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#FF6B35"
        self.success_color = "#4CAF50"
        self.warning_color = "#FFC107"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.devices = []
        self.selected_device = tk.StringVar()
        self.is_cleaning = False
        
        self.setup_ui()
        self.check_adb_available()
    
    def t(self, key):
        """Get translated text"""
        lang = self.language.get()
        return LANGUAGES[lang].get(key, key)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=50)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text=f"🔧 {self.t('title')}",
            font=("Segoe UI", 16, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Device selection section
        device_frame = tk.LabelFrame(
            main_frame,
            text=self.t("device_selection"),
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=8
        )
        device_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Device dropdown and refresh button in same row
        device_control_frame = tk.Frame(device_frame, bg=self.bg_color)
        device_control_frame.pack(fill=tk.X)
        
        self.device_combo = ttk.Combobox(
            device_control_frame,
            textvariable=self.selected_device,
            state="readonly",
            font=("Segoe UI", 10),
            width=45
        )
        self.device_combo.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.refresh_btn = tk.Button(
            device_control_frame,
            text=self.t("refresh_devices"),
            command=self.refresh_devices,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.refresh_btn.pack(side=tk.LEFT)
        
        # Action buttons section
        action_frame = tk.Frame(main_frame, bg=self.bg_color)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.clean_btn = tk.Button(
            action_frame,
            text=self.t("clean_temp"),
            command=self.clean_temp_files,
            bg=self.success_color,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.clean_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.check_btn = tk.Button(
            action_frame,
            text=self.t("check_size"),
            command=self.check_temp_size,
            bg=self.warning_color,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.check_btn.pack(side=tk.LEFT)
        
        # Log section
        log_frame = tk.LabelFrame(
            main_frame,
            text=self.t("log"),
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=8
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#2b2b2b",
            fg="#00ff00",
            insertbackground="white",
            height=14
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text=self.t("ready"),
            font=("Segoe UI", 9),
            bg="#e0e0e0",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def log(self, message, level="INFO"):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.log_text.update()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.status_bar.update()
        
    def run_adb_command(self, command):
        """Execute ADB command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
            
    def check_adb_available(self):
        """Check if ADB is installed and accessible"""
        self.log(self.t("checking_adb"))
        returncode, stdout, stderr = self.run_adb_command("adb version")
        
        if returncode == 0:
            version = stdout.split('\n')[0] if stdout else "Unknown version"
            self.log(f"{self.t('adb_found')}: {version}", "SUCCESS")
            self.refresh_devices()
        else:
            self.log(self.t("adb_not_found"), "ERROR")
            messagebox.showerror(
                self.t("adb_error_title"),
                self.t("adb_error_msg")
            )
            
    def refresh_devices(self):
        """Refresh list of connected devices"""
        self.log(self.t("scanning_devices"))
        self.update_status(self.t("scanning"))
        
        returncode, stdout, stderr = self.run_adb_command("adb devices -l")
        
        if returncode != 0:
            self.log(f"{self.t('device_list_error')}: {stderr}", "ERROR")
            self.update_status(f"Hata: {self.t('device_error')}")
            return
            
        # Parse device list
        self.devices = []
        lines = stdout.strip().split('\n')[1:]  # Skip header line
        
        for line in lines:
            if line.strip() and 'device' in line:
                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    device_id = parts[0]
                    # Try to get device model
                    model = "Unknown"
                    for part in parts[2:]:
                        if 'model:' in part:
                            model = part.split(':')[1]
                            break
                    
                    device_info = f"{device_id} ({model})"
                    self.devices.append((device_id, device_info))
        
        # Update combo box
        if self.devices:
            device_names = [info for _, info in self.devices]
            self.device_combo['values'] = device_names
            self.device_combo.current(0)
            
            self.log(f"{len(self.devices)} {self.t('devices_found')}", "SUCCESS")
            self.update_status(f"{len(self.devices)} {self.t('devices_ready')}")
            
            self.clean_btn.config(state=tk.NORMAL)
            self.check_btn.config(state=tk.NORMAL)
        else:
            self.device_combo['values'] = []
            self.selected_device.set('')
            self.log(self.t("no_devices"), "WARNING")
            self.update_status(self.t("no_device_found"))
            
            self.clean_btn.config(state=tk.DISABLED)
            self.check_btn.config(state=tk.DISABLED)
            
    def get_selected_device_id(self):
        """Get the device ID of selected device"""
        if not self.devices:
            return None
            
        selected_index = self.device_combo.current()
        if selected_index >= 0:
            return self.devices[selected_index][0]
        return None
        
    def check_temp_size(self):
        """Check size of temp directory"""
        device_id = self.get_selected_device_id()
        if not device_id:
            messagebox.showwarning(self.t("select_device"), self.t("select_device_msg"))
            return
            
        self.log(f"{self.t('checking_size')}: {device_id}")
        self.update_status(self.t("calculating"))
        
        # Run du command to check size
        command = f'adb -s {device_id} shell "du -sh /data/local/tmp 2>/dev/null || echo \'0K\'"'
        returncode, stdout, stderr = self.run_adb_command(command)
        
        if returncode == 0:
            size = stdout.strip().split()[0] if stdout.strip() else "Unknown"
            self.log(f"{self.t('size_msg')}: {size}", "INFO")
            messagebox.showinfo(
                self.t("size_title"),
                f"{self.t('size_msg')}: {size}\n\n{self.t('location')}: /data/local/tmp"
            )
            self.update_status(f"Temp {self.t('size_msg').lower()}: {size}")
        else:
            self.log(f"{self.t('size_error')}: {stderr}", "ERROR")
            messagebox.showerror(self.t("size_error"), self.t("size_error_msg"))
            self.update_status(self.t("error_occurred"))
            
    def clean_temp_files(self):
        """Clean temp files from selected device"""
        device_id = self.get_selected_device_id()
        if not device_id:
            messagebox.showwarning(self.t("select_device"), self.t("select_device_msg"))
            return
            
        # Confirm action
        response = messagebox.askyesno(
            self.t("confirm_clean"),
            f"{self.t('confirm_clean_msg')}\n\n"
            f"{self.t('confirm_device')}: {self.selected_device.get()}\n"
            f"{self.t('confirm_location')}: /data/local/tmp/*\n\n"
            f"{self.t('confirm_warning')}"
        )
        
        if not response:
            return
            
        # Run cleaning in separate thread
        thread = threading.Thread(target=self._clean_thread, args=(device_id,))
        thread.daemon = True
        thread.start()
        
    def _clean_thread(self, device_id):
        """Thread function for cleaning operation"""
        self.is_cleaning = True
        self.clean_btn.config(state=tk.DISABLED)
        self.check_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.DISABLED)
        
        try:
            self.log(f"{self.t('cleaning_started')}: {device_id}", "INFO")
            self.update_status(self.t("cleaning"))
            
            # Execute cleaning command
            command = f'adb -s {device_id} shell rm -rf /data/local/tmp/*'
            returncode, stdout, stderr = self.run_adb_command(command)
            
            if returncode == 0:
                self.log(self.t("cleaning_success"), "SUCCESS")
                messagebox.showinfo(
                    self.t("success_title"),
                    f"{self.t('success_msg')}: /data/local/tmp/*"
                )
                self.update_status(self.t("cleaning_complete"))
            else:
                error_msg = stderr if stderr else self.t("unexpected_error")
                self.log(f"{self.t('cleaning_error')}: {error_msg}", "ERROR")
                messagebox.showerror(self.t("size_error"), f"{self.t('cleaning_failed')}:\n{error_msg}")
                self.update_status(self.t("error_occurred"))
                
        except Exception as e:
            self.log(f"{self.t('process_error')}: {str(e)}", "ERROR")
            messagebox.showerror(self.t("size_error"), f"{self.t('unexpected_error')}:\n{str(e)}")
            self.update_status(self.t("error_occurred"))
        finally:
            self.is_cleaning = False
            self.clean_btn.config(state=tk.NORMAL)
            self.check_btn.config(state=tk.NORMAL)
            self.refresh_btn.config(state=tk.NORMAL)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AndroidTempCleaner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
