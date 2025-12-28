import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession 

# معلوماتك الأساسية
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

# كود الهوية الخاص بك (المستخرج من صورتك الأخيرة)
string_session = "1ApWapzMBu4TYb7nkLcRODtj9yVAOkl-vXCqnSMfYcoQ-hWqadtb5i8noDB1jc42L16Blf7HH1_Anivbj2CeOp2sZD8MJLnGZGsqQW-Pgn5GPo2hnGeozFx9IAvh6_N7mjH8ahoVzwbWfPshgGZrEOlHz2e-GFZF6htk471s1aEjLy9XjfIP8J1F451SKvq35JwvEpMOZ-KoZt5nfuMgYt8dvDSXuXoNAfvmpfiLEB-Y45z0Yz2KDKswpNZH34kvUTKdr3rWCesO74IXjJSQGcZmrmiIMPgRJm4EfO4--8I3uruEAZvkEUT6LqVaU4hcq6zYEyobMtuuqU7STukUO7M8XJ6aSesM=" 

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    try:
        sender = await event.get_sender()
        name = sender.first_name if sender else "مجهول"

        # فحص الميديا المؤقتة (صور أو فيديوهات ذاتية التدمير)
        is_ttl = False
        if event.media:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                is_ttl = True
            elif hasattr(event.media, 'photo') and hasattr(event.media.photo, 'ttl_seconds') and event.media.photo.ttl_seconds:
                is_ttl = True
            elif hasattr(event.media, 'document') and hasattr(event.media.document, 'ttl_seconds') and event.media.document.ttl_seconds:
                is_ttl = True

        if is_ttl:
            # تحميل الميديا بالصيغة الصحيحة تلقائياً (صورة أو فيديو)
            file_path = await event.download_media()
            caption = f"⚠️ تم صيد ميديا ذاتية (صورة/فيديو) من: {name}"
            await client.send_file('me', file_path, caption=caption)
            if os.path.exists(file_path): os.remove(file_path)
            return

        # توجيه الميديا العادية (لتوفير الرام ومنع توقف Koyeb)
        if event.media:
            await event.forward_to('me')
            
        # تحويل النصوص
        elif event.text:
            await client.send_message('me', f"📩 {name}:\n{event.text}")

    except Exception as e:
        print(f"Error: {e}")

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
    print("✅ السكربت الشامل يعمل: صيد (صور + فيديوهات) ذاتية بنجاح!")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
