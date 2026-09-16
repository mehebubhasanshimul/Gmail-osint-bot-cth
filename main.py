# -*- coding: utf-8 -*-
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# কনফিগারেশন ও ক্রেডেন্সিয়াল
TOKEN = '8801113765:AAGjrmqclSXw1zDeihGCQSQnERas7tKTozQ'
RAPIDAPI_KEY = 'b3ad11e41cmahhb18121f061df58ep1b5c61jand7a83cdda6d56'
RAPIDAPI_HOST = 'gmail-osint.p.rapidapi.com'
GROUP_LINK = 'https://t.me/+inTW2I925HcyMjU1'
CREDIT = '@SHADOW_JOKER_CTH'

bot = telebot.TeleBot(TOKEN)

# ভেরিফাইড ইউজারদের স্টোর করার জন্য সেট
verified_users = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
    markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
    
    welcome_text = (
        f"স্বাগতম! 🕵️‍♂️ *Gmail OSINT Intelligence* বটে আপনাকে স্বাগতম।\n\n"
        f"বটটি ব্যবহার করতে প্রথমে আমাদের অফিসিয়াল টেলিগ্রাম গ্রুপে জয়েন করুন, তারপর নিচে *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন।\n\n"
        f"👑 *Developer/Credit:* {CREDIT}"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.from_user.id
    verified_users.add(user_id)
    bot.answer_callback_query(call.id, "ধন্যবাদ! আপনার ভেরিফিকেশন সফল হয়েছে।")
    
    # ইউজারকে লেখার সুবিধা দেওয়ার জন্য নিচে স্থায়ী রিপ্লাই কিবোর্ড যুক্ত করা
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton("🔍 কীভাবে সার্চ করব?"), KeyboardButton("ℹ️ বটের তথ্য"))
    
    edit_text = (
        f"✅ *ভেরিফিকেশন সফল!*\n\n"
        f"এখন নিচের চ্যাট বক্সে যেকোনো জিমেইল (Email) অ্যাড্রেস লিখে পাঠান (যেমন: `example@gmail.com`), আমি RapidAPI থেকে সেটির সম্পূর্ণ ইন্টেলিজেন্স রিপোর্ট বের করে দেব।\n\n"
        f"👑 *Credit:* {CREDIT}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_text,
        parse_mode="Markdown"
    )
    bot.send_message(call.message.chat.id, "👇 নিচ থেকে সাহায্য নিতে পারেন অথবা সরাসরি জিমেইল লিখে পাঠান:", reply_markup=reply_markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if text == "🔍 কীভাবে সার্চ করব?":
        bot.reply_to(message, f"💡 **ব্যবহারবিধি:**\nচ্যাট বক্সে সরাসরি যেকোনো জিমেইল অ্যাড্রেস লিখে পাঠিয়ে দিন। যেমন:\n`target@gmail.com`\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    elif text == "ℹ️ বটের তথ্য":
        bot.reply_to(message, f"🤖 **Gmail OSINT Bot v2.0**\nপাওয়ার্ড বাই RapidAPI.\nনিরাপদ ও দ্রুত ইমেল ইন্টেলিজেন্স রিপোর্ট প্রদান করে।\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return

    # ইউজার গ্রুপে জয়েন করেছে কি না চেক
    if user_id not in verified_users:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
        markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
        
        bot.reply_to(
            message, 
            f"⚠️ দয়া করে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন!\n\n👑 *Credit:* {CREDIT}", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
        return

    email = text
    
    # সাধারণ ইমেইল ভ্যালিডেশন
    if '@' not in email or '.' not in email:
        bot.reply_to(message, f"❌ দয়া করে একটি সঠিক জিমেইল বা ইমেইল অ্যাড্রেস পাঠান। (যেমন: `target@gmail.com`)\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    
    processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য RapidAPI থেকে ডেটা স্ক্যান করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
    
    try:
        url = f"https://{RAPIDAPI_HOST}/gmail"
        headers = {
            "content-type": "application/json",
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        payload = {
            "email": email
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code != 200:
            bot.edit_message_text(
                f"❌ লুকআপ ব্যর্থ হয়েছে বা এপিআই লিমিট শেষ হয়েছে। (Status: {response.status_code})\n\n👑 *Credit:* {CREDIT}", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="Markdown"
            )
            return
            
        data = response.json()
        
        # রেসপন্স সুন্দরভাবে ফরম্যাট করে সাজানো
        report = f"📊 *Gmail Intelligence Report*\n"
        report += f"━━━━━━━━━━━━━━━━━━━\n"
        report += f"📧 *Email:* `{email}`\n\n"
        
        if isinstance(data, dict):
            for key, val in data.items():
                if key not in ['email', 'success', 'status']:
                    report += f"• *{key.replace('_', ' ').title()}:* `{val}`\n"
        else:
            report += f"• *Result:* {str(data)[:600]}\n"
            
        report += f"\n━━━━━━━━━━━━━━━━━━━\n"
        report += f"👑 *Developer/Credit:* {CREDIT}"

        bot.edit_message_text(
            report, 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text(
            f"❌ সার্ভারে সংযোগ করতে সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n👑 *Credit:* {CREDIT}", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode="Markdown"
        )

# বট রান করা
print("🤖 Gmail OSINT Bot is running successfully with RapidAPI...")
bot.infinity_polling()
