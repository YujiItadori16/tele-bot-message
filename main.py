# main.py
# Telegram bot as a Web Service on Render using webhook.
# Sends a local photo (promo.jpg), a caption, and an inline button on /start.

import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Content (override via env vars if desired) ----------------------------
CAPTION     = os.getenv("CAPTION", "free youtube premium giveaway")
BUTTON_TEXT = os.getenv("BUTTON_TEXT", "Click here")
BUTTON_URL  = os.getenv("BUTTON_URL", "https://t.me/Playerstatsandnews")
# Use promo.jpg in repo root (no assets folder)
BASE_DIR = Path(__file__).resolve().parent
PHOTO_PATH = os.getenv("PHOTO_PATH", str(BASE_DIR / "promo.jpg"))
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_TEXT, url=BUTTON_URL)]])
    with open(PHOTO_PATH, "rb") as f:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=f,
            caption=CAPTION,
            reply_markup=keyboard,
        )

def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing BOT_TOKEN env var.")
    webhook_base = os.getenv("WEBHOOK_URL") or os.getenv("RENDER_EXTERNAL_URL")
    if not webhook_base:
        raise RuntimeError(
            "Missing WEBHOOK_URL/RENDER_EXTERNAL_URL. Set WEBHOOK_URL to your Render service URL."
        )

    port = int(os.getenv("PORT", "10000"))  # Render sets PORT automatically

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Use token as secret path
    url_path = token
    webhook_url = f"{webhook_base.rstrip('/')}/{url_path}"

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=url_path,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
