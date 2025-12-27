import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events, functions

# معلوماتك
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

client = TelegramClient('al_amal_session', api_id, api_hash)

# صيد الصور المؤقتة
@client.on(events.NewMessage(incoming=True))
async def secret_media_hunter(event):
    if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
        try:
            file = await event.download_media(file=bytes)
            sender = await event.get_sender()
            caption = f"⚠️ تم صيد صورة مؤقتة!\nمن: {sender.first_name}\nالوقت: {datetime.now().strftime('%H:%M')}"
            await client.send_file('me', file, caption=caption)
        except Exception as e:
            print(f"خطأ: {e}")

# تحديث الوقت
async def time_updater():
    while True:
        try:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            current_time = datetime.now(baghdad_tz).strftime("%I:%M %p")
            await client(functions.account.UpdateProfileRequest(first_name=f"مجتبى | {current_time}"))
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(10)

async def main():
    await client.start()
    print("✅ السكربت شغال!")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
