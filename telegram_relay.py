# telegram_relay.py • Telegram Staging Bot Relay
import requests
import streamlit as st

def send_to_telegram(caption, image_paths=None, bot_token=None, chat_id=None):
    """
    Sends generated text, captions, and media files to a private Telegram chat/channel
    as a staging queue for agentic publishing.
    """
    # Fallback to Streamlit secrets if not explicitly passed
    token = bot_token or st.secrets.get("TELEGRAM_BOT_TOKEN", "")
    chat = chat_id or st.secrets.get("TELEGRAM_CHAT_ID", "")
    
    if not token or not chat:
        return False, "Missing Telegram Bot Token or Chat ID in configuration/secrets."
    
    # 1. Send the Caption / Text Payload first
    text_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat,
        "text": f"🚀 **Staged Content Ready for Posting**\n\n{caption}",
        "parse_mode": "Markdown"
    }
    
    response = requests.post(text_url, data=payload)
    if not response.ok:
        return False, f"Failed to send text payload: {response.text}"
        
    # 2. If there are media files (images/video), send them as an album or individual files
    if image_paths:
        for path in image_paths:
            photo_url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(path, "rb") as photo_file:
                files = {"photo": photo_file}
                data = {"chat_id": chat}
                requests.post(photo_url, data=data, files=files)
                
    return True, "Successfully delivered content package to your Telegram staging queue!"