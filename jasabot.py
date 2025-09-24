# jasabot.py
import os
import json
import time
import importlib
from pyrogram import Client
from threading import Thread

# --- config ---
CFG_PATH = "config.json"
if os.path.exists(CFG_PATH):
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
else:
    raise FileNotFoundError("config.json tidak ditemukan!")

bot = Client(
    "mybot_session",
    api_id=cfg["api_id"],
    api_hash=cfg["api_hash"],
    bot_token=cfg["bot_token"]
)

# --- folder fitur ---
FEATURES_FOLDER = "."
feature_files = {}  # simpan file yg sudah di-load dan timestamp

def load_or_reload_features():
    global feature_files
    for file in os.listdir(FEATURES_FOLDER):
        if file.endswith(".py") and file not in ["jasabot.py"]:
            path = os.path.join(FEATURES_FOLDER, file)
            mtime = os.path.getmtime(path)
            modul_name = file[:-3]  # tanpa .py
            if file not in feature_files or feature_files[file] != mtime:
                try:
                    if file in feature_files:
                        # reload modul
                        mod = importlib.import_module(modul_name)
                        importlib.reload(mod)
                        print(f"[RELOAD] {modul_name}")
                    else:
                        # import baru
                        mod = importlib.import_module(modul_name)
                        print(f"[LOAD] {modul_name}")
                    if hasattr(mod, "register"):
                        mod.register(bot)
                        print(f"[OK] handler register({modul_name}) dijalankan")
                    feature_files[file] = mtime
                except Exception as e:
                    print(f"[ERROR] gagal load {modul_name}: {e}")

# --- thread background untuk scan fitur ---
def feature_watcher():
    while True:
        load_or_reload_features()
        time.sleep(5)  # cek setiap 5 detik

# --- mulai thread watcher ---
Thread(target=feature_watcher, daemon=True).start()

if __name__ == "__main__":
    print("Bot sedang berjalan... (hot-reload fitur aktif)")
    bot.run()
