import asyncio
from datetime import datetime
import pytz
import os
from telethon import TelegramClient, events, functions

# معلوماتك الأساسية من GitHub
api_id = 38595661
api_hash = '129990bd1d2cf9064516e6ebf503528d'

client = TelegramClient('al_amal_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def all_in_one_handler(event):
    # السكربت سيعمل فقط مع المحادثات الخاصة (ليس المجموعات)
    if not event.is_private:
        return

    sender = await event.get_sender()
    sender_name = sender.first_name if sender else "مجهول"
    
    # 1. صيد الميديا المؤقتة (تدمير ذاتي) - الأولوية القصوى
    if event.media and hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
        try:
            path = "captured_media.jpg"
            await event.download_media(file=path)
            caption = f"⚠️ تم صيد ميديا مؤقتة!\nمن: {sender_name}\nالوقت: {datetime.now().strftime('%I:%M')}"
            await client.send_file('me', path, caption=caption)
            if os.path.exists(path): os.remove(path)
            return # نتوقف هنا لكي لا يتم تكرار الإرسال
        except Exception as e:
            print(f"Error TTL: {e}")

    # 2. تحويل البصمات (الرسائل الصوتية)
    if event.voice:
        try:
            caption = f"🎤 بصمة صوتية جديدة\nمن: {sender_name}"
            await client.send_file('me', event.media, caption=caption)
        except Exception as e:
            print(f"Error Voice: {e}")

    # 3. تحويل الصور العادية والفيديوهات والرسائل المرئية
    elif event.photo or event.video or event.video_note:
        try:
            file_type = "صورة" if event.photo else "فيديو"
            caption = f"📸 {file_type} جديد\nمن: {sender_name}"
            await client.send_file('me', event.media, caption=caption)
        except Exception as e:
            print(f"Error Media: {e}")

    # 4. تحويل الرسائل النصية
    elif event.text:
        try:
            log_text = f"📩 رسالة نصية\nمن: {sender_name}\nالنص: {event.text}"
            await client.send_message('me', log_text)
        except Exception as e:
            print(f"Error Text: {e}")

# 5. تحديث الوقت (الساعة فقط بنظام 12 ساعة)
async def time_updater():
    while True:
        try:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            current_time = datetime.now(baghdad_tz).strftime("%I:%M")
            # تحديث الاسم ليصبح الساعة فقط
            await client(functions.account.UpdateProfileRequest(first_name=current_time))
            await asyncio.sleep(60)
        except Exception as e:
            await asyncio.sleep(10)

async def main():
    await client.start()
    print("✅ السكربت العملاق شغال: ساعة + بصمات + صور + فيديوهات + نصوص")
    await asyncio.gather(time_updater(), client.run_until_disconnected())

with client:
    client.loop.run_until_complete(main())
