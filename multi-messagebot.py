import psutil
import time
import keyboard
import win32gui
import win32process

def chat(message):
    keyboard.press_and_release('slash')
    time.sleep(0.05)
    keyboard.write(message, 0.005)
    time.sleep(0.05)
    keyboard.press_and_release('enter')

def get_roblox_pids():
    roblox_pids = []
    for process in psutil.process_iter(['name']):
        if 'Roblox' in process.info['name']:
            roblox_pids.append(process.pid)
    return roblox_pids

def get_window_by_pid(pid):
    pid_to_hwnd = None
    def callback(hwnd, extra_pid):
        nonlocal pid_to_hwnd
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if current_pid == extra_pid and win32gui.IsWindowVisible(hwnd):
            pid_to_hwnd = hwnd

    win32gui.EnumWindows(callback, pid)
    return pid_to_hwnd

def maximize_and_focus_window_by_pid(pid):
    try:
        hwnd = get_window_by_pid(pid)
        if hwnd:
            window_title = win32gui.GetWindowText(hwnd)
            if window_title == "Roblox":
                # Maximize the window
                win32gui.ShowWindow(hwnd, 3)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    print(f"Maximized and focused window for PID: {pid}")
                    return True
                except Exception as inner_error:
                    print(f"Error bringing window to foreground for PID {pid}: {inner_error}")
    except Exception as e:
        print(f"Error maximizing and focusing window for PID {pid}: {e}")
    return False


while True:
    message = input('Type Message: ')
    for pid in get_roblox_pids():
        if maximize_and_focus_window_by_pid(pid):
            chat(message)
            time.sleep(0.1)