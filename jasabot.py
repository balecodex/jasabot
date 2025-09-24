# jasabot.py
import os
import json
import importlib
import time
from threading import Thread
from pyrogram import Client

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

FEATURES_FOLDER = "."
feature_files = {}
feature_handlers = {}  # modul_name -> list handler

def load_or_reload_features():
    for file in os.listdir(FEATURES_FOLDER):
        if file.endswith(".py") and file != "jasabot.py":
            path = os.path.join(FEATURES_FOLDER, file)
            mtime = os.path.getmtime(path)
            modul_name = file[:-3]

            if file not in feature_files or feature_files[file] != mtime:
                try:
                    # reload modul
                    if file in feature_files:
                        mod = importlib.reload(importlib.import_module(modul_name))
                        print(f"[RELOAD] {modul_name}")
                    else:
                        mod = importlib.import_module(modul_name)
                        print(f"[LOAD] {modul_name}")

                    # hapus handler lama
                    if modul_name in feature_handlers:
                        for h in feature_handlers[modul_name]:
                            bot.remove_handler(h)
                        feature_handlers[modul_name] = []

                    # ambil handler sebelum dan sesudah register
                    handlers_before = list(bot.handlers)
                    if hasattr(mod, "register"):
                        mod.register(bot)
                    handlers_after = list(bot.handlers)

                    # simpan handler baru untuk modul ini
                    new_handlers = [h for h in handlers_after if h not in handlers_before]
                    feature_handlers[modul_name] = new_handlers

                    feature_files[file] = mtime
                    print(f"[OK] {modul_name} terupdate, handler baru aktif")

                except Exception as e:
                    print(f"[ERROR] {modul_name}: {e}")

def feature_watcher():
    while True:
        load_or_reload_features()
        time.sleep(5)

Thread(target=feature_watcher, daemon=True).start()

if __name__ == "__main__":
    print("Bot aktif... (hot-reload penuh)")
    bot.run()
