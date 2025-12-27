import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession 

# معلوماتك الأساسية
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

# ⚠️ ضع هنا الكود الطويل الذي نسخته من الكونسول سابقاً
string_session = "ضَع_الكود_الطويل_هنا" 

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    try:
        sender = await event.get_sender()
        name = sender.first_name if sender else "مجهول"

        # 1. فحص هل الميديا "ذاتية تدمير" (TTL) - الأولوية القصوى
        is_ttl = False
        if event.media:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                is_ttl = True
            elif hasattr(event.media, 'photo') and hasattr(event.media.photo, 'ttl_seconds') and event.media.photo.ttl_seconds:
                is_ttl = True

        if is_ttl:
            # صيد الذاتية: تحميل ثم إرسال كصورة عادية لكي لا تضيع
            path = "captured.jpg"
            await event.download_media(file=path)
            await client.send_file('me', path, caption=f"🚀 تم صيد ذاتية من: {name}\nالوقت: {datetime.now().strftime('%I:%M')}")
            if os.path.exists(path): os.remove(path)
            return # إنهاء العملية هنا لكي لا يتم توجيهها مرة أخرى

        # 2. إذا كانت ميديا عادية (بصمة، صورة، فيديو) - توجيه لتوفير الرام
        if event.media:
            await event.forward_to('me')
            
        # 3. إذا كانت رسالة نصية
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
    print("✅ السكربت شغال: صيد الذاتية مفعل بالأولوية")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
