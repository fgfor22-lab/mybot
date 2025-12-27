import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession 

# معلوماتك الأساسية
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

# اتركها فارغة الآن لكي نستخرج الكود الجديد
string_session = "" 

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    try:
        sender = await event.get_sender()
        name = sender.first_name if sender else "مجهول"
        # صيد الذاتية وتوجيه البصمات
        if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
            path = "captured.jpg"
            await event.download_media(file=path)
            await client.send_file('me', path, caption=f"⚠️ صيد ذاتية من: {name}")
            if os.path.exists(path): os.remove(path)
        elif event.media:
            await event.forward_to('me')
        elif event.text:
            await client.send_message('me', f"📩 {name}:\n{event.text}")
    except: pass

async def time_updater():
    while True:
        try:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            current_time = datetime.now(baghdad_tz).strftime("%I:%M")
            await client(functions.account.UpdateProfileRequest(first_name=current_time))
            await asyncio.sleep(60)
        except: await asyncio.sleep(20)

async def main():
    await client.start()
    if not string_session:
        print("انسخ هذا الكود الطويل وضعه في GitHub:")
        print(client.session.save())
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
