import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession 

api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'
string_session = "" 

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    try:
        # صيد الذاتية وتوجيه الميديا
        if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
            path = "captured.jpg"
            await event.download_media(file=path)
            await client.send_file('me', path, caption=f"⚠️ صيد ذاتية")
            if os.path.exists(path): os.remove(path)
        elif event.media: await event.forward_to('me')
        elif event.text:
            sender = await event.get_sender()
            await client.send_message('me', f"📩 {sender.first_name}:\n{event.text}")
    except: pass

async def main():
    await client.start()
    # 💡 هذه الإضافة سترسل لك الكود إلى تليجرام فوراً
    if not string_session:
        session_code = client.session.save()
        await client.send_message('me', f"✅ هذا هو كود الهوية الخاص بك، انسخه وضعه في GitHub:\n\n`{session_code}`")
        print("✅ تم إرسال الكود إلى رسائلك المحفوظة في تليجرام!")
    
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
