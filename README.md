# Telegram Bot (Web Service + Webhook) — No assets folder

Sends **promo.jpg** + caption + one inline button when user sends `/start`.
Built with `python-telegram-bot` v20+. Deployed on Render as a **Web Service** (webhook).

## Files
- `main.py` — webhook server (binds to `$PORT`, registers webhook)
- `promo.jpg` — image sent on `/start`
- `requirements.txt`
- `render.yaml`
- `.gitignore`

## Deploy on Render (Web Service)
1. Push this folder to GitHub.
2. Render → **New → Web Service** → connect repo.
3. **Build Command:** `pip install -r requirements.txt`
   **Start Command:** `python main.py`
4. Add Environment Variables:
   - `BOT_TOKEN`   = your BotFather token
   - `WEBHOOK_URL` = your service URL (e.g. `https://your-app.onrender.com`)
   - *(Optional)* `CAPTION`, `BUTTON_TEXT`, `BUTTON_URL`, `PHOTO_PATH` (default: `promo.jpg`)
5. Deploy. If you added `WEBHOOK_URL` after first deploy, redeploy once more to set webhook.
6. Test your bot with `/start` in Telegram.

## Local quick test (polling alternative)
If you want to run locally without webhook, change in `main.py`:
```python
# Replace app.run_webhook(...) with:
app.run_polling(allowed_updates=Update.ALL_TYPES)
```
Then run:
```bash
pip install -r requirements.txt
export BOT_TOKEN="YOUR_TOKEN"
python main.py
```

## Security
Never commit your real token to Git. If it leaks, reset via `@BotFather /revoke` and update env vars.
