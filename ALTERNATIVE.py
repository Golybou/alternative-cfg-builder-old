import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import math
import re
import winreg
import time
import sys
import webbrowser

CONFIG_FILE = 'script.cfg'

window = tk.Tk()
window.resizable(0, 0)
folder_path = tk.StringVar(window)
scrollbar = tk.Scale(window, from_=5, to=100, orient=tk.HORIZONTAL)
ini_file_label = tk.Label(window)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def choose_ini_file():
    scrollbar_value = scrollbar.get()
    ini_file_value = math.ceil(scrollbar_value / 5) * 5

    if ini_file_value > 100:
        ini_file_value = 100
    ini_file = f'{ini_file_value}.ini'
    ini_file_label.configure(text=f"Selected ini file: {ini_file}")
    return ini_file

def adjust_weapon(attribute, value):
    with open('complited cfg.ini', 'r') as f:
        lines = f.readlines()

    with open('complited cfg.ini', 'w') as f:
        for line in lines:
            if line.startswith(attribute + '='):
                f.write(f'{attribute}={value}\n')
            else:
                f.write(line)

def apply_smart_awp_scout():
    with open('complited cfg.ini', 'r') as f:
        lines = f.readlines()

    with open('complited cfg.ini', 'w') as f:
        is_in_section = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line == "[WEAPON_3]" or stripped_line == "[WEAPON_18]":
                is_in_section = True
            if stripped_line == "" or (stripped_line[0] == "[" and stripped_line[-1] == "]") and stripped_line not in [
            "[WEAPON_3]", "[WEAPON_18]"]:
                is_in_section = False
            if is_in_section:
                if line.startswith('aim_fov='):
                    f.write(f'aim_fov=3\n')
                elif line.startswith('aim_speed_enable='):
                    f.write(f'aim_speed_enable=1\n')
                elif line.startswith('aim_speed_in_attack='):
                    f.write(f'aim_speed_in_attack=92\n')
                elif line.startswith('aim_autodelay='):
                    f.write(f'aim_autodelay=1\n')
                elif line.startswith('trigger='):
                    f.write(f'trigger=1\n')
                elif line.startswith('trigger_accuracy='):
                    f.write(f'trigger_accuracy=2\n')
                elif line.startswith('trigger_type='):
                    f.write(f'trigger_type=1\n')
                elif line.startswith('trigger_hitbox_scale='):
                    f.write(f'trigger_hitbox_scale=0.8\n')
                else:
                    f.write(line)
            else:
                f.write(line)

def adjust_general_parameters():
    with open('complited cfg.ini', 'r') as f:
        lines = f.readlines()

    with open('complited cfg.ini', 'w') as f:
        for line in lines:
            if line.startswith('trigger_only_zoomed='):
                f.write(f'trigger_only_zoomed=1\n')
            elif line.startswith('trigger_key_mode='):
                f.write(f'trigger_key_mode=1\n')
            elif line.startswith('trigger_hitbox_scale='):
                f.write(f'trigger_hitbox_scale=0.8\n')
            elif line.startswith('trigger_key='):
                f.write(f'trigger_key=1\n')
            else:
                f.write(line)

def trigger_window():
    def trigger_enable():
        adjust_weapon("trigger_enable", "1")
        trigger_window.destroy()
        choose_speed_scale()

    def trigger_disable():
        adjust_weapon("trigger_disable", "0")
        trigger_window.destroy()
        choose_speed_scale()

    trigger_window = tk.Toplevel(window)
    trigger_window.resizable(0, 0)
    trigger_window.title("Smart AWP and SCOUT")
    tk.Label(trigger_window,
             text="Enable smart AWP and SCOUT? [will have to abandon the trigger]").pack()

    trigger_window_width = 400 
    trigger_window_height = 80 

    screen_width = trigger_window.winfo_screenwidth()
    screen_height = trigger_window.winfo_screenheight()

    position_top = int(screen_height / 2 - trigger_window_height / 2)
    position_right = int(screen_width / 2 - trigger_window_width / 2)

    trigger_window.geometry(f'{trigger_window_width}x{trigger_window_height}+{position_right}+{position_top}')

    tk.Button(trigger_window, text="Confirm", command=trigger_enable).pack()
    tk.Button(trigger_window, text="Reject", command=trigger_disable).pack()

    center_window(trigger_window)

def choose_psilent():
    def set_value():
        psilent_value = psilent_scale.get()
        with open('complited cfg.ini', 'r') as f:
            lines = f.readlines()
        with open('complited cfg.ini', 'w') as f:
            for line in lines:
                new_line = re.sub(r'(aim_psilent\s*=).*', r'\g<1>' + f'{psilent_value}', line)
                f.write(new_line)
        psilent_window.destroy()
        trigger_window() 


    def skip_value():
        psilent_window.destroy()
        trigger_window() 

    psilent_window = tk.Toplevel(window)
    psilent_window.resizable(0, 0)
    psilent_window.title("Selecting a value for Psilent aim for all weapons")

    psilent_window_width =  300
    psilent_window_height = 140

    screen_width = psilent_window.winfo_screenwidth()
    screen_height = psilent_window.winfo_screenheight()

    position_top = int(screen_height / 2 - psilent_window_height / 2)
    position_right = int(screen_width / 2 - psilent_window_width / 2)

    psilent_window.geometry(f'{psilent_window_width}x{psilent_window_height}+{position_right}+{position_top}')

    label = tk.Label(psilent_window, text="Selecting a value for Psilent aim for all weapons")
    label.pack()

    psilent_scale = tk.Scale(psilent_window, from_=0.1, to=1, resolution=0.1, orient=tk.HORIZONTAL)
    psilent_scale.pack(pady=10)

    save_btn = tk.Button(psilent_window, text="Save for all weapons", command=set_value)
    save_btn.pack()

    skip_btn = tk.Button(psilent_window, text="Skip and leave the preset in advance", command=skip_value)
    skip_btn.pack()

    center_window(psilent_window)


def choose_esp():
    def set_values():
        adjust_weapon("esp_player_type", "1")
        adjust_weapon("esp_box", "1")
        adjust_weapon("esp_thru_wall", "1")
        adjust_weapon("esp_history", "1")
        adjust_weapon("esp_sound", "1")
        adjust_weapon("esp_sound_only_enemy", "1")
        adjust_weapon("esp_bomb", "1")
        esp_window.destroy()
        successfully_created_config()  # Call the function here after all actions are done

    def skip_values():
        esp_window.destroy()
        successfully_created_config()

    esp_window = tk.Toplevel(window)
    esp_window.resizable(0, 0)
    esp_window.title("Choosing an ESP")

    esp_window_width = 300
    esp_window_height = 150

    screen_width = esp_window.winfo_screenwidth()
    screen_height = esp_window.winfo_screenheight()

    position_top = int(screen_height / 2 - esp_window_height / 2)
    position_right = int(screen_width / 2 - esp_window_width / 2)

    esp_window.geometry(f'{esp_window_width}x{esp_window_height}+{position_right}+{position_top}')

    label = tk.Label(esp_window, text="Enable Esp, Sound Esp, Bomb Esp?")
    label.pack(pady=20)

    confirm_btn = tk.Button(esp_window, text="Confirm", command=set_values)
    skip_btn = tk.Button(esp_window, text="Reject and terminate", command=skip_values)

    confirm_btn.pack(side=tk.TOP, padx=1)
    skip_btn.pack(side=tk.TOP, padx=2)

    center_window(esp_window)

def choose_speed_scale():
    def set_value():
        speed_scale_value = speed_scale.get()
        with open('complited cfg.ini', 'r') as f:
            lines = f.readlines()
        with open('complited cfg.ini', 'w') as f:
            for line in lines:
                new_line = re.sub(r'(aim_speed_scale\s*=).*', r'\g<1>' + f'{speed_scale_value}', line)
                f.write(new_line)
        speed_window.destroy()
        choose_esp() 

    def skip_value():
        speed_window.destroy()

    speed_window = tk.Toplevel(window)
    speed_window.resizable(0, 0)
    speed_window.title("Selecting the guidance acceleration")

    speed_window_width = 300
    speed_window_height = 140

    screen_width = speed_window.winfo_screenwidth()
    screen_height = speed_window.winfo_screenheight()

    position_top = int(screen_height / 2 - speed_window_height / 2)
    position_right = int(screen_width / 2 - speed_window_width / 2)

    # Set window geometry
    speed_window.geometry(f'{speed_window_width}x{speed_window_height}+{position_right}+{position_top}')

    label = tk.Label(speed_window, text="Select Hover acceleration")
    label.pack()

    speed_scale = tk.Scale(speed_window, from_=1, to=50, orient=tk.HORIZONTAL)
    speed_scale.pack(pady=10)

    save_btn = tk.Button(speed_window, text="Save hover acceleration", command=set_value)
    save_btn.pack()

    skip_btn = tk.Button(speed_window, text="Skip and leave without acceleration", command=skip_value)
    skip_btn.pack()

    center_window(speed_window)


def copy_ini_file():
    global scrollbar
    ini_file = choose_ini_file()
    script_dir = folder_path.get()
    source_folder = os.path.join(script_dir, 'config')

    if not os.path.exists(source_folder):
        for dirpath, dirnames, filenames in os.walk(script_dir):
            for filename in filenames:
                if filename.endswith('.ini'):
                    source_folder = dirpath
                    break

    ini_file_path = os.path.join(source_folder, ini_file)

    if not os.path.exists(ini_file_path):
        print('File does not exist')
        return

    copied_file_name = os.path.join(script_dir, 'complited cfg.ini')

    shutil.copy2(ini_file_path, copied_file_name)
    print('File copied successfully')
    choose_psilent()
    adjust_general_parameters()
    apply_smart_awp_scout()


def get_folder_path():
    window.withdraw()
    dir_path = filedialog.askdirectory(title="Choosing the path to the script")
    window.deiconify()

    folder_path.set(dir_path)
    with open(CONFIG_FILE, 'w') as f:
        f.write(dir_path)
    return dir_path


def check_config_file():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            dir_path = f.readline().strip()
            if os.path.isdir(dir_path):
                folder_path.set(dir_path)
                return dir_path

    window.withdraw()
    dir_path = filedialog.askdirectory(title="Choosing the path to the script")
    window.deiconify()

    if dir_path != "":
        folder_path.set(dir_path)
        with open(CONFIG_FILE, 'w') as f:
            f.write(dir_path)
        return dir_path

    return None

def successfully_created_config():
    def close_everything():
        success_window.destroy()
        window.destroy()

    success_window = tk.Toplevel(window)
    success_window.resizable(0, 0)
    success_window.title("Confirm!")
    success_window.geometry("250x120")

    label = tk.Label(success_window, text="The configuration has been created successfully!")
    label.pack(pady=20)

    ok_button = tk.Button(success_window, text="Okey!", command=close_everything, width=10)
    ok_button.pack()

    center_window(success_window)

def window_main():
    global scrollbar, ini_file_label

    config_dir = check_config_file() or get_folder_path()

    if config_dir:
        window.title("ALTERNATIVE config Builder by Golyb0u")

        window_width = 500
        window_height = 330

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        label = tk.Label(window, text="Choosing the percentage of legitness")
        label.pack()

        label2 = tk.Label(window, text="(The higher the percentage, the more legit the setup will be)")
        label2.pack()

        scrollbar = tk.Scale(window, from_=5, to=100,length=250, orient=tk.HORIZONTAL)
        scrollbar.pack(pady=100)  

        choose_btn = tk.Button(window, text="Confirm", command=copy_ini_file)
        choose_btn.pack()

        window.mainloop()

    else:
        print("The path to the script is not selected.")

window_main()
