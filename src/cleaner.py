import os
import shutil
import time

def get_fivem_data_path():
    user = os.environ.get("USERNAME")
    base = os.path.expandvars(rf"C:\Users\{user}\AppData\Local\FiveM\FiveM.app\data")
    return base

def get_keybind_path():
    user = os.environ.get("USERNAME")
    return os.path.expandvars(rf"C:\Users\{user}\AppData\Roaming\CitizenFX\fivem.cfg")

class Cleaner:
    def __init__(self, progress_callback, status_callback):
        self.progress_callback = progress_callback
        self.status_callback = status_callback

    def delete_files_and_folders(self, paths):
        total_items = len(paths)
        for index, path in enumerate(paths):
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.progress_callback(int((index + 1) / total_items * 100))
                self.status_callback(f'Deleted: {path}')
            else:
                self.status_callback(f'Not found: {path}')
            time.sleep(0.1)  # Simulate time taken for deletion

    def restore_keybind(self):
        # Logic to restore keybinds can be implemented here
        self.status_callback('Keybinds restored.')

def clean_fivem(log_callback, progress_callback, delete_keybind=False, locale=None):
    data_path = get_fivem_data_path()
    targets = ["cache", "game-storage", "server-cache", "server-cache-priv"]
    total = len(targets) + (1 if delete_keybind else 0)
    done = 0

    for folder in targets:
        folder_path = os.path.join(data_path, folder)
        if os.path.exists(folder_path):
            try:
                log_callback(locale["log_deleting"].format(item=folder_path))
                shutil.rmtree(folder_path)
            except Exception as e:
                log_callback(f"Errore: {e}")
        else:
            log_callback(f"{folder_path} non trovato.")
        done += 1
        progress_callback(int(done / total * 100))

    if delete_keybind:
        keybind_path = get_keybind_path()
        if os.path.exists(keybind_path):
            try:
                log_callback(locale["log_deleting"].format(item=keybind_path))
                os.remove(keybind_path)
            except Exception as e:
                log_callback(f"Errore: {e}")
        else:
            log_callback(f"{keybind_path} non trovato.")
        done += 1
        progress_callback(int(done / total * 100))