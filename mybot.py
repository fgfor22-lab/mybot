import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events, functions

# معلوماتك الأساسية
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

# نظام إعادة اتصال تلقائي قوي
client = TelegramClient('al_amal_session', api_id, api_hash, connection_retries=None)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private: return
    try:
        # توجيه الميديا (صور، بصمات، فيديو) مباشرة لتوفير الرام
        if event.media:
            await event.forward_to('me')
        
        # تحويل النصوص
        elif event.text:
            sender = await event.get_sender()
            name = sender.first_name if sender else "مجهول"
            await client.send_message('me', f"📩 {name}:\n{event.text}")
    except: pass # تجاهل الأخطاء البسيطة لضمان عدم التوقف

async def time_updater():
    while True:
        try:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            current_time = datetime.now(baghdad_tz).strftime("%I:%M")
            # تحديث الساعة فقط (أرقام بنظام 12 ساعة)
            await client(functions.account.UpdateProfileRequest(first_name=current_time))
            await asyncio.sleep(60)
        except: await asyncio.sleep(20)

async def main():
    await client.start()
    print("✅ السكربت الاقتصادي شغال 24 ساعة")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
