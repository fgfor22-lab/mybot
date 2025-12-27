import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions

# معلوماتك الأساسية
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

client = TelegramClient('al_amal_session', api_id, api_hash)

# 1. صيد الصور المؤقتة (إصلاح مشكلة الملف unnamed)
@client.on(events.NewMessage(incoming=True))
async def secret_media_hunter(event):
    if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
        try:
            # حفظ الملف بصيغة jpg ليتعرف عليه تليجرام كصورة
            path = "photo.jpg"
            await event.download_media(file=path)
            
            caption = f"⚠️ تم صيد صورة مؤقتة!\nالوقت: {datetime.now().strftime('%I:%M')}"
            
            # إرسال الملف كصورة وليس ملف خام
            await client.send_file('me', path, caption=caption)
            
            # حذف الصورة من السيرفر بعد الإرسال
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error: {e}")

# 2. تحديث الوقت (الساعة فقط بدون الاسم وبدون AM/PM)
async def time_updater():
    while True:
        try:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            # %I:%M تعطي الساعة والدقيقة فقط (نظام 12 ساعة)
            current_time = datetime.now(baghdad_tz).strftime("%I:%M")
            
            # تحديث الاسم ليصبح الساعة فقط
            await client(functions.account.UpdateProfileRequest(first_name=current_time))
            
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(10)

async def main():
    await client.start()
    print("✅ السكربت المحدث شغال!")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
