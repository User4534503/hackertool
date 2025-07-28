# HackerTool

import os
import sys
import time
import hashlib
import tempfile
import subprocess
import urllib.request
import json
from colorama import init, Fore, Style
import msvcrt
import zipfile
import winreg
import ctypes
init()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_password(prompt="Please enter the password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char in [b'\r', b'\n']:  # Enter key
            print('')
            break
        elif char == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        elif char == b'\x03':  # Ctrl+C
            raise KeyboardInterrupt
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)
    return password

def print_main():
    clear_terminal()
    print(Fore.GREEN + r"""
 _   _            _            _____           _ 
| | | | __ _  ___| | _____ _ _|_   _|__   ___ | |
| |_| |/ _` |/ __| |/ / _ \ '__|| |/ _ \ / _ \| |
|  _  | (_| | (__|   <  __/ |   | | (_) | (_) | |
|_| |_|\__,_|\___|_|\_\___|_|   |_|\___/ \___/|_|
    """ + Style.RESET_ALL)

def auto_update():
    """
    Downloads the latest hackertool.exe from the GitHub Releases API,
    compares SHA256 hashes, and if different,
    swaps in the new version and restarts.
    """
    # 1️⃣ Query the GitHub API for the latest release
    api_url = "https://api.github.com/repos/User4534503/hackertool/releases/latest"
    req = urllib.request.Request(api_url, headers={
        "User-Agent": "HackerTool-Updater",
        "Accept": "application/vnd.github.v3+json"
    })
    with urllib.request.urlopen(req) as resp:
        release_info = json.load(resp)

    # 2️⃣ Find the hackertool.exe asset
    assets = release_info.get("assets", [])
    exe_asset = next((a for a in assets if a.get("name") == "hackertool.exe"), None)
    if not exe_asset:
        print("⚠️ Couldn't find hackertool.exe in the latest release!")
        return

    download_url = exe_asset["browser_download_url"]

    # 3️⃣ Download remote EXE to a temp file
    local_exe = sys.executable  # current running .exe
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".exe", dir=os.path.dirname(local_exe))
    os.close(tmp_fd)
    print("⬇️  Downloading latest version...")
    urllib.request.urlretrieve(download_url, tmp_path)

    # 4️⃣ Hash helper
    def file_hash(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    # 5️⃣ Compare hashes
    if file_hash(tmp_path) != file_hash(local_exe):
        print("✨ New version detected! Applying update... ✨")
        base_dir = os.path.dirname(local_exe)
        new_name = os.path.basename(tmp_path)
        old_name = os.path.basename(local_exe)
        bat_path = os.path.join(base_dir, "update.bat")

        # 6️⃣ Write batch script to swap and restart
        bat_content = f"""
@echo off
timeout /t 2 /nobreak >nul
del "{old_name}"
ren "{new_name}" "{old_name}"
start "" "{old_name}"
del "%~f0"
"""
        with open(bat_path, "w") as bat:
            bat.write(bat_content.strip())

        # 7️⃣ Launch the updater and exit
        subprocess.Popen(["cmd", "/c", bat_path], cwd=base_dir)
        sys.exit()
    else:
        # 🚀 Already up to date
        os.remove(tmp_path)
        print("✅ HackerTool is up to date!")
        time.sleep(1)



# ========= Hacking Terminal =========
def loadHackingTerminal():

    # initialise colour mapping
    colour_map = {
        'red': Fore.RED,
        'orange': Fore.LIGHTRED_EX,
        'yellow': Fore.YELLOW,
        'green': Fore.GREEN,
        'blue': Fore.BLUE,
        'purple': Fore.MAGENTA,
        'pink': Fore.LIGHTMAGENTA_EX,
        'white': Fore.WHITE,
        'black': Fore.BLACK,
        'grey': Fore.LIGHTBLACK_EX,
        'default': Style.RESET_ALL
    }
    # use mutable dict to allow wrapper access to current colour
    colour_state = {'code': Style.RESET_ALL}

    class ColourWriter:
        def __init__(self, orig):
            self.orig = orig
        def write(self, text):
            # prefix and reset to ensure all text is coloured
            self.orig.write(colour_state['code'] + text + Style.RESET_ALL)
        def flush(self):
            self.orig.flush()
        def isatty(self):
            return getattr(self.orig, 'isatty', lambda: False)()

    # wrap stdout and stderr
    sys.stdout = ColourWriter(sys.stdout)
    sys.stderr = ColourWriter(sys.stderr)

    def coloured_input(prompt):
        # write prompt & flush so it actually appears
        sys.stdout.write(colour_state['code'] + prompt)
        sys.stdout.flush()

        buffer = ''
        while True:
            ch = msvcrt.getwch()  # gets a str
            if ch == '\r':  # Enter
                sys.stdout.write('\n')
                sys.stdout.flush()
                break

            elif ch == '\x08':  # Backspace
                if buffer:
                    buffer = buffer[:-1]
                    # move cursor back, overwrite with space, move back
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()

            else:
                buffer += ch
                # echo the character in the current colour, then flush
                sys.stdout.write(colour_state['code'] + ch)
                sys.stdout.flush()

        return buffer.strip()

    def ensure_home():
        home = os.path.join(
            os.environ.get('USERPROFILE', os.path.expanduser('~')),
            'hacking-terminal'
        )
        os.makedirs(home, exist_ok=True)
        return home

    clear_terminal()
    home = ensure_home()
    cwd = home

    while True:
        # build Windows-style prompt with backslashes only
        rel = os.path.relpath(cwd, home)
        if rel == '.':
            display = "~\\"
        else:
            display = "~\\" + rel.replace("/", "\\") + "\\"
        # get coloured input including echo
        try:
            line = coloured_input(f"{display}> ")
        except (EOFError, KeyboardInterrupt):
            sys.stdout.write('\n')
            break

        if not line:
            continue

        parts = line.split(None, 1)
        cmd = parts[0].lower()

        # colour command
        if cmd in ('colour', 'color'):
            if len(parts) < 2:
                sys.stdout.write("Usage: colour <colorname>\n")
            else:
                choice = parts[1].strip().lower()
                if choice in colour_map:
                    colour_state['code'] = colour_map[choice]
                else:
                    sys.stdout.write(f"Unknown colour '{choice}'. Available: {', '.join(colour_map.keys())}\n")
            continue

        # exit or quit
        if cmd in ('exit', 'quit'):
            # === RESET terminal state after exit ===
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            colour_state['code'] = Style.RESET_ALL
            print(Style.RESET_ALL, end='')  # ensure it visually resets the terminal
            break

        # cd command
        if cmd == 'cd':
            target = parts[1] if len(parts) > 1 else ''
            if target in ('', '~', '~/'):
                cwd = home
            else:
                if target.startswith('~/') or target.startswith('~\\'):
                    path = os.path.join(home, target[2:].lstrip("\\/"))
                else:
                    path = os.path.join(cwd, target)
                real = os.path.abspath(path)
                if os.path.isdir(real) and real.startswith(home):
                    cwd = real
                else:
                    sys.stdout.write(f"cd: no such file or directory: {target}\n")
            continue

        # mkdir command
        if cmd == 'mkdir':
            if len(parts) < 2 or not parts[1].strip():
                sys.stdout.write("mkdir: missing operand\n")
                continue
            target = parts[1].strip()
            if target.startswith('~/') or target.startswith('~\\'):
                path = os.path.join(home, target[2:].lstrip("\\/"))
            else:
                path = os.path.join(cwd, target)
            try:
                os.makedirs(path)
            except FileExistsError:
                sys.stdout.write(f"mkdir: cannot create directory '{target}': File exists\n")
            except Exception as e:
                sys.stdout.write(f"mkdir: cannot create directory '{target}': {e}\n")
            continue

        # unknown command
        sys.stdout.write(f"{cmd}: command not found\n")



# === Program start ===
clear_terminal()
passw = input_password()

if passw == "hack1ng":
    auto_update()
    print("")
else:
    sys.exit()

# === Main menu ===
while True:
    print_main()
    print("1) Install apps\n2) UEN v1\n3) Hacking Terminal\n4) Quit\n")

    choice = input("What would you like to do: ")
    while choice not in ["1", "2", "3", "4"]:
        choice = input("What would you like to do: ")

    print_main()

    if choice == "1":
        print("1) Install Java 21\n2) Back\n")
        sub = input("What would you like to do: ")
        while sub not in ["1", "2"]:
            sub = input("What would you like to do: ")

        if sub == "1":
            # Java installer logic
            user_profile = os.environ['USERPROFILE']
            install_dir = os.path.join(user_profile, 'Java21')
            zip_path     = os.path.join(install_dir, 'java21.zip')
            url          = "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.zip"

            os.makedirs(install_dir, exist_ok=True)
            print("\n📥 Downloading...")
            urllib.request.urlretrieve(url, zip_path)

            print("📦 Installing...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
            os.remove(zip_path)

            extracted_dir = next(os.scandir(install_dir)).path
            bin_path      = os.path.join(extracted_dir, "bin")

            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0,
                                     winreg.KEY_READ | winreg.KEY_WRITE) as key:
                    current_path, reg_type = winreg.QueryValueEx(key, "Path")
                    if bin_path.lower() not in current_path.lower():
                        new_path = current_path + ";" + bin_path
                        winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
                ctypes.windll.user32.SendMessageTimeoutW(
                    0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, None
                )
                print("✅ Java Successfully Installed!")
            except Exception as e:
                print(f"⚠️ Failed to update PATH: {e}")
            time.sleep(3)

    elif choice == "2":
        print_main()
        print("UEN is coming soon...")
        time.sleep(3)

    elif choice == "3":
        print_main()
        print("Loading Hacking Terminal...")
        time.sleep(2)
        loadHackingTerminal()
        time.sleep(3)

    elif choice == "4":
        print_main()
        print("Closing HackerTool...")
        time.sleep(2)
        clear_terminal()
        sys.exit()
