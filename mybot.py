import asyncio
from telethon import TelegramClient, events, functions, errors
from telethon.sessions import StringSession
import pytz
from datetime import datetime

# بياناتك المحدثة
API_ID = 10006527
API_HASH = 'f531ddb8a981efacd5b5ed52c42094ed'
# كود الهوية الذي استخرجته من Termux
SESSION = '1ApWapzMBuzZ4J02CNhX0MTJyWyITZTcz5kXUi7C0S_NKyFPaeSmzaf1WkqwdJywFCkbp4-lTSm8-ApyGzv5mn1FeluL9Dy3louMrG9OVxPUaWM6AdgAxBo3z4F61beNguYJ09EVKHLDM4mIMAH2ObAYAjdntd83MQUX6C3xscV8nRNJmC66VQl7GmQ40V_jeWaoh9fpw7QO7UrJGDJMoKzORCxw2SE5gUIVQv223mvqNNO7fVyHU4Sw1E12yA_yK3PR0laCdHDk4rTJ62vEfYylMBK4irjMZ4LWi_BzzMtdgMf030-ILlExkWWOK7elCTos0T9iOCisi6aFxmoTwAfk6_1Z7mV8='

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def clock():
    while True:
        try:
            tz = pytz.timezone('Asia/Baghdad')
            now = datetime.now(tz).strftime("%I:%M")
            await client(functions.account.UpdateProfileRequest(first_name=now))
            print(f"⏰ الساعة الآن في كربلاء: {now}")
            await asyncio.sleep(60)
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ خطأ الساعة: {e}")
            await asyncio.sleep(30)

async def main():
    await client.start()
    print("🚀 تم تفعيل سكربت مجتبى بنجاح!")
    await asyncio.gather(clock(), client.run_until_disconnected())

if __name__ == "__main__":
    asyncio.run(main())
