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
feature_files = {}  # simpan file yang sudah di-load
feature_handlers = {}  # simpan semua handler per modul

def load_or_reload_features():
    global feature_files, feature_handlers
    for file in os.listdir(FEATURES_FOLDER):
        if file.endswith(".py") and file != "jasabot.py":
            path = os.path.join(FEATURES_FOLDER, file)
            mtime = os.path.getmtime(path)
            modul_name = file[:-3]

            # reload jika ada perubahan
            if file not in feature_files or feature_files[file] != mtime:
                try:
                    if file in feature_files:
                        mod = importlib.import_module(modul_name)
                        importlib.reload(mod)
                        print(f"[RELOAD] {modul_name}")
                    else:
                        mod = importlib.import_module(modul_name)
                        print(f"[LOAD] {modul_name}")

                    # hapus handler lama kalau ada
                    if modul_name in feature_handlers:
                        for h in feature_handlers[modul_name]:
                            bot.remove_handler(h)
                        feature_handlers[modul_name] = []

                    # register handler baru
                    handlers_before = bot.handlers.copy()
                    if hasattr(mod, "register"):
                        mod.register(bot)
                    # ambil handler baru yang ditambahkan
                    new_handlers = [h for h in bot.handlers if h not in handlers_before]
                    feature_handlers[modul_name] = new_handlers

                    feature_files[file] = mtime
                    print(f"[OK] Fitur {modul_name} siap dengan handler baru")
                except Exception as e:
                    print(f"[ERROR] gagal load {modul_name}: {e}")

def feature_watcher():
    while True:
        load_or_reload_features()
        time.sleep(5)

Thread(target=feature_watcher, daemon=True).start()

if __name__ == "__main__":
    print("Bot sedang berjalan... (hot-reload penuh aktif)")
    bot.run()
