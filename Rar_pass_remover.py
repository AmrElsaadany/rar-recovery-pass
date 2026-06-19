import os
import string
import itertools
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- AUTO DEPENDENCY CHECK ---
try:
    from rarfile import RarFile, BadRarFile
except ImportError:
    # If missing, we show a native Tkinter error box before exiting
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Missing Dependency", 
        "The 'rarfile' library is required.\n\nPlease open CMD and run:\npip install rarfile"
    )
    sys.exit(1)


class RarRecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAR Password Recovery Tool")
        self.root.geometry("520x400")
        self.root.resizable(False, False)
        
        # Variables
        self.rar_path = tk.StringVar()
        self.wordlist_path = tk.StringVar()
        self.attack_mode = tk.StringVar(value="numeric")
        self.status_msg = tk.StringVar(value="Ready.")
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        # --- File Selection Frame ---
        file_frame = ttk.LabelFrame(self.root, text=" Target & Wordlist ", padding=10)
        file_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(file_frame, text="RAR File:").grid(row=0, column=0, sticky="w")
        ttk.Entry(file_frame, textvariable=self.rar_path, width=45).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_rar).grid(row=0, column=2, pady=5)

        ttk.Label(file_frame, text="Wordlist:").grid(row=1, column=0, sticky="w")
        self.wl_entry = ttk.Entry(file_frame, textvariable=self.wordlist_path, width=45, state="disabled")
        self.wl_entry.grid(row=1, column=1, padx=5, pady=5)
        self.wl_btn = ttk.Button(file_frame, text="Browse", command=self.browse_wordlist, state="disabled")
        self.wl_btn.grid(row=1, column=2, pady=5)

        # --- Attack Mode Frame ---
        mode_frame = ttk.LabelFrame(self.root, text=" Attack Method ", padding=10)
        mode_frame.pack(fill="x", padx=15, pady=5)

        ttk.Radiobutton(mode_frame, text="Numeric Brute Force (1, 2, 3...)", variable=self.attack_mode, 
                        value="numeric", command=self.toggle_wordlist).pack(anchor="w", pady=2)
        ttk.Radiobutton(mode_frame, text="Dictionary Attack (Uses Wordlist)", variable=self.attack_mode, 
                        value="dict", command=self.toggle_wordlist).pack(anchor="w", pady=2)
        ttk.Radiobutton(mode_frame, text="Alphanumeric Brute Force (a-z, A-Z, 0-9, !@#)", variable=self.attack_mode, 
                        value="alpha", command=self.toggle_wordlist).pack(anchor="w", pady=2)

        # --- Progress & Controls ---
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill="x", padx=15, pady=5)

        self.start_btn = ttk.Button(control_frame, text="Start Attack", command=self.start_process)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_process, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # --- Status Bar ---
        status_frame = ttk.LabelFrame(self.root, text=" Live Progress ", padding=10)
        status_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_msg, font=("Consolas", 10), wraplength=480)
        self.status_label.pack(anchor="w")

    def toggle_wordlist(self):
        """Enables wordlist inputs only if Dictionary mode is selected."""
        if self.attack_mode.get() == "dict":
            self.wl_entry.config(state="normal")
            self.wl_btn.config(state="normal")
        else:
            self.wl_entry.config(state="disabled")
            self.wl_btn.config(state="disabled")

    def browse_rar(self):
        path = filedialog.askopenfilename(filetypes=[("RAR Archives", "*.rar")])
        if path:
            self.rar_path.set(path)

    def browse_wordlist(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.wordlist_path.set(path)

    def test_password(self, password):
        try:
            with RarFile(self.rar_path.get()) as rf:
                rf.testrar(pwd=password)
                return True
        except (BadRarFile, RuntimeError, Exception):
            return False

    def open_target_file(self):
        try:
            absolute_path = os.path.abspath(self.rar_path.get())
            if os.name == 'nt':
                os.startfile(absolute_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.run([opener, absolute_path])
        except Exception as e:
            print(f"Error opening file: {e}")

    def stop_process(self):
        self.is_running = False
        self.status_msg.set("Stopping process...")

    def start_process(self):
        if not self.rar_path.get() or not os.path.exists(self.rar_path.get()):
            messagebox.showwarning("Warning", "Please select a valid target RAR file.")
            return
        if self.attack_mode.get() == "dict" and (not self.wordlist_path.get() or not os.path.exists(self.wordlist_path.get())):
            messagebox.showwarning("Warning", "Please select a valid Wordlist text file.")
            return

        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Run execution loop in a secondary Thread so the Tkinter window does not freeze
        threading.Thread(target=self.recovery_loop, daemon=True).start()

    def recovery_loop(self):
        mode = self.attack_mode.get()
        found = False
        final_pwd = ""

        if mode == "numeric":
            pwd_num = 1
            while self.is_running:
                pwd = str(pwd_num)
                self.status_msg.set(f"Testing: {pwd}")
                if self.test_password(pwd):
                    found, final_pwd = True, pwd
                    break
                pwd_num += 1

        elif mode == "dict":
            try:
                with open(self.wordlist_path.get(), 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if not self.is_running:
                            break
                        pwd = line.strip()
                        self.status_msg.set(f"Testing: {pwd}")
                        if self.test_password(pwd):
                            found, final_pwd = True, pwd
                            break
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Could not read wordlist: {e}"))

        elif mode == "alpha":
            charset = string.ascii_letters + string.digits + string.punctuation
            # Automatically scans lengths from 1 up to 8 characters
            for length in range(1, 9):
                if not self.is_running or found:
                    break
                for item in itertools.product(charset, repeat=length):
                    if not self.is_running:
                        break
                    pwd = "".join(item)
                    self.status_msg.set(f"Testing: {pwd}")
                    if self.test_password(pwd):
                        found, final_pwd = True, pwd
                        break

        # UI updates after finishing loop
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        if found:
            self.status_msg.set(f"[SUCCESS] Found Password: {final_pwd}")
            # Use 'after' method to interact with GUI from a separate thread safely
            self.root.after(0, lambda: messagebox.showinfo("Success!", f"Password Found: {final_pwd}"))
            self.open_target_file()
        else:
            self.status_msg.set("Process finished. Password not discovered.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RarRecoveryApp(root)
    root.mainloop()