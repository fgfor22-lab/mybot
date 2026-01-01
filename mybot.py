import asyncio
import os
from datetime import datetime
import pytz
from telethon import TelegramClient, events, functions, errors
from telethon.sessions import StringSession 

# --- واجهة المبرمج مجتبى الكعبي ---
print("---------------------------------------")
print("🚀 نظام 'مجتبى للبرمجيات' - العمل الدائم")
print("👨‍💻 المبرمج المسؤول: مجتبى الكعبي")
print("---------------------------------------")

# 1. إعدادات الحساب والمفاتيح التي أرسلتها
API_ID = 10006527
API_HASH = 'f531ddb8a981efacd5b5ed52c42094ed'
# كود الجلسة (String Session) الخاص بك
STRING_SESSION = "1ApWapzMBuzZ4J02CNhX0MTJyWyITZTcz5kXUi7C0S_NKyFPaeSmzaf1WkqwdJywFCkbp4-lTSm8-ApyGzv5mn1FeluL9Dy3louMrG9OVxPUaWM6AdgAxBo3z4F61beNguYJ09EVKHLDM4mIMAH2ObAYAjdntd83MQUX6C3xscV8nRNJmC66VQl7GmQ40V_jeWaoh9fpw7QO7UrJGDJMoKzORCxw2SE5gUIVQv223mvqNNO7fVyHU4Sw1E12yA_yK3PR0laCdHDk4rTJ62vEfYylMBK4irjMZ4LWi_BzzMtdgMf030-ILlExkWWOK7elCTos0T9iOCisi6aFxmoTwAfk6_1Z7mV8="

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# 2. نظام صيد الميديا الذاتية (TTL)
@client.on(events.NewMessage(incoming=True))
async def media_catcher(event):
    if not event.is_private: return
    try:
        is_ttl = False
        if event.media:
            # التحقق من مؤقت التدمير الذاتي
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds: is_ttl = True
            elif hasattr(event.media, 'photo') and hasattr(event.media.photo, 'ttl_seconds') and event.media.photo.ttl_seconds: is_ttl = True
            elif hasattr(event.media, 'document') and hasattr(event.media.document, 'ttl_seconds') and event.media.document.ttl_seconds: is_ttl = True

        if is_ttl:
            file_path = await event.download_media()
            caption = "⚠️ تم صيد ميديا ذاتية بنجاح!\n👨‍💻 تطوير: المبرمج مجتبى الكعبي"
            await client.send_file('me', file_path, caption=caption)
            if os.path.exists(file_path): os.remove(file_path) # تنظيف السيرفر
    except: pass

# 3. نظام الساعة (تحديث الاسم كل دقيقة)
async def profile_clock():
    while True:
        try:
            # توقيت بغداد
            tz = pytz.timezone('Asia/Baghdad')
            current_time = datetime.now(tz).strftime("%I:%M")
            
            # تحديث البروفايل
            await client(functions.account.UpdateProfileRequest(first_name=current_time))
            
            # الانتظار لمدة 60 ثانية (دقيقة واحدة)
            await asyncio.sleep(60) 
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds) # الانتظار التلقائي في حال الحظر المؤقت
        except:
            await asyncio.sleep(30)

# التشغيل الرئيسي مع نظام الحماية من التوقف
async def main():
    try:
        await client.start()
        print("✅ تم تفعيل 'مجتبى للبرمجيات' بنجاح!")
        # تشغيل الساعة وصيد الميديا معاً
        await asyncio.gather(profile_clock(), client.run_until_disconnected())
    except Exception as e:
        print(f"🔴 خطأ في التشغيل: {e}")

if __name__ == "__main__":
    asyncio.run(main())
