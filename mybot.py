from telethon import TelegramClient, events
import os

# --- بيانات المبرمج مجتبى الكعبي الجديدة ---
API_ID = 10006527 
API_HASH = 'f531ddb8a981efacd5b5ed52c42094ed'

# استخدام الجلسة القديمة المستقرة
client = TelegramClient('mojtaba_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    try:
        # الحصول على بيانات المرسل
        sender = await event.get_sender()
        name = sender.first_name if sender.first_name else 'بدون اسم'
        username = f'@{sender.username}' if sender.username else 'لا يوجد يوزر'
                
        # التوقيع الخاص بك (بصمة مجتبى الكعبي)
        footer_text = f'\n\n👤 المرسل: {name}\n🆔 اليوزر: {username}\n━━━━━━━━━━━━\n💎 المبرمج مجتبى'

        # 1. إذا كانت الرسالة وسائط (صورة، فيديو، رسالة صوتية)
        if event.media:
            # إرسال الوسائط إلى الرسائل المحفوظة مع الكابشن الجديد
            await client.send_file('me', event.media, caption=footer_text)
            print(f'✅ تم صيد وسائط من {name} بنجاح!')
                
        # 2. إذا كانت رسالة نصية فقط
        elif event.text:
            full_message = f'{event.text}{footer_text}'
            await client.send_message('me', full_message)
            print(f'✅ تم صيد نص من {name} بنجاح!')

    except Exception as e:
        print(f'❌ حدث خطأ بسيط: {e}')

print('🚀 السكربت القديم يعمل الآن تحت إشراف المبرمج مجتبى...')
client.start()
client.run_until_disconnected()
