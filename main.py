# -*- coding: utf-8 -*-
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# আপনার টেলিগ্রাম বট টোকেন ও এপিআই কি
TOKEN = '8801113765:AAGjrmqclSXw1zDeihGCQSQnERas7tKTozQ'
API_KEY = 'in_rD06OX3qWhOHBM4rdIBV'
GROUP_LINK = 'https://t.me/+inTW2I925HcyMjU1'
CREDIT = '@SHADOW_JOKER_CTH'

bot = telebot.TeleBot(TOKEN)

# মেমোরিতে ভেরিফাই করা ইউজারদের স্টোর করার জন্য সেট
verified_users = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
    markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
    
    welcome_text = (
        f"স্বাগতম! 🕵️‍♂️ IntelBase Email Intelligence বটে আপনাকে স্বাগতম।\n\n"
        f"বটটি ব্যবহার করতে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন, তারপর নিচে *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন।\n\n"
        f"👑 *Credit:* {CREDIT}"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.from_user.id
    verified_users.add(user_id)
    bot.answer_callback_query(call.id, "ধন্যবাদ! আপনার ভেরিফিকেশন সফল হয়েছে।")
    
    # ইউজারকে লেখার সুবিধা দেওয়ার জন্য নিচে একটি স্থায়ী রিপ্লাই কিবোর্ড যুক্ত করা হলো
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton("🔍 কীভাবে সার্চ করব?"))
    
    edit_text = (
        f"✅ *ভেরিফিকেশন সফল!*\n\n"
        f"এখন নিচের চ্যাট বক্সে যেকোনো জিমেইল (Email) অ্যাড্রেস লিখে পাঠান (যেমন: `example@gmail.com`), আমি IntelBase থেকে সেটির ইন্টেলিজেন্স রিপোর্ট বের করে দেব।\n\n"
        f"👑 *Credit:* {CREDIT}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_text,
        parse_mode="Markdown"
    )
    # একটি আলাদা মেসেজে রিপ্লাই কিবোর্ড পাঠানো
    bot.send_message(call.message.chat.id, "👇 নিচ থেকে সাহায্য নিতে পারেন অথবা সরাসরি ইমেইল লিখে পাঠান:", reply_markup=reply_markup)

@bot.message_handler(func=lambda message: True)
def handle_email_lookup(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # সাহায্য বা নির্দেশিকা দেখার জন্য বাটন হ্যান্ডেল করা
    if text == "🔍 কীভাবে সার্চ করব?":
        bot.reply_to(message, f"💡 বটি ব্যবহার করতে চ্যাট বক্সে সরাসরি যেকোনো ইমেইল লিখে পাঠিয়ে দিন। যেমন:\n`target@gmail.com`\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return

    # ইউজার গ্রুপে জয়েন করেছে কি না চেক করা
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
        bot.reply_to(message, f"❌ দয়া করে একটি সঠিক জিমেইল বা ইমেইল অ্যাড্রেস পাঠান। (যেমন: target@example.com)\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    
    # প্রসেসিং মেসেজ পাঠানো
    processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য ডেটা স্ক্যান করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
    
    try:
        url = "https://api.intelbase.is/lookup/email"
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "timeout_ms": 10000,
            "include_data_breaches": True
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code != 200:
            bot.edit_message_text(
                f"❌ লুকআপ ব্যর্থ হয়েছে: {data.get('error', 'অজানা সমস্যা।')}\n\n👑 *Credit:* {CREDIT}", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="Markdown"
            )
            return
        
        # ডাটা প্রসেস ও সাজানো
        meta = data.get('meta', {})
        breaches = data.get('data_breaches', {})
        stealer = data.get('stealer_logs', {})
        accounts = data.get('identifier', {}).get('accounts', [])
        
        report = f"📊 *Email Intelligence Report*\n"
        report += f"━━━━━━━━━━━━━━━━━━━\n"
        report += f"📧 *Email:* `{meta.get('email', email)}`\n"
        report += f"📅 *First Seen:* {meta.get('first_seen', 'N/A').split('T')[0]}\n"
        report += f"📅 *Last Seen:* {meta.get('last_seen', 'N/A').split('T')[0]}\n\n"
        
        report += f"⚠️ *Data Breaches:* {breaches.get('amount', 0)} টি সোর্স\n"
        report += f"💻 *Stealer Logs Compromised:* {'🚨 হ্যাঁ (Compromised)' if stealer.get('compromised') else '✅ সুরক্ষিত (Safe)'}\n\n"
        
        # রেজিস্টার্ড অ্যাকাউন্ট বা প্ল্যাটফর্মের লিংক যুক্ত করা
        if accounts:
            report += f"🌐 *Registered Platforms:*\n"
            for acc in accounts[:5]:
                mod = acc.get('module', {})
                name = mod.get('name_formatted', mod.get('name', 'Unknown'))
                domain = mod.get('domain', '')
                if domain:
                    report += f"• [{name}](https://{domain})\n"
                else:
                    report += f"• {name}\n"
            report += "\n"

        # ব্রিচ সোর্সসমূহ
        if breaches.get('results'):
            report += f"🔍 *প্রধান ব্রিচ সোর্সসমূহ:*\n"
            for b in breaches.get('results', [])[:3]:
                source_info = b.get('source', {})
                report += f"• {source_info.get('name', 'N/A')} ({source_info.get('date', 'N/A')})\n"
        
        report += f"\n━━━━━━━━━━━━━━━━━━━\n"
        report += f"👑 *Developer/Credit:* {CREDIT}"

        # ফাইনাল রেজাল্ট পাঠানো
        bot.edit_message_text(
            report, 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        print(e)
        bot.edit_message_text(
            f"❌ সার্ভারে সংযোগ করতে সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n👑 *Credit:* {CREDIT}", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode="Markdown"
        )

# বট রান করা
print("🤖 Telegram Bot is running successfully...")
bot.infinity_polling()
