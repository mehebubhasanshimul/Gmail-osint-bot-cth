# -*- coding: utf-8 -*-
import telebot
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# কনফিগারেশন
TOKEN = '8801113765:AAGjrmqclSXw1zDeihGCQSQnERas7tKTozQ'  # আপনার টেলিগ্রাম বট টোকেন
GROUP_LINK = 'https://t.me/+inTW2I925HcyMjU1'  # আপনার টেলিগ্রাম গ্রুপ লিংক
CREDIT = 'https://t.me/SHADOW_JOKER_CTH'

bot = telebot.TeleBot(TOKEN)
verified_users = set()

# ব্রাউজার হেডার (বট ব্লকিং এড়ানোর জন্য)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ১. Gravatar থেকে নাম ও প্রোফাইল পিকচার বের করার ফাংশন
def get_gravatar_info(email):
    try:
        email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
        url = f"https://www.gravatar.com/{email_hash}.json"
        response = requests.get(url, timeout=5, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            entry = data.get('entry', [{}])[0]
            display_name = entry.get('displayName', None)
            avatar_url = entry.get('thumbnailUrl', None)
            return display_name, avatar_url
    except:
        pass
    return None, None

# ২. সাধারণ সাইট চেকার ফাংশন
def check_site(name, url):
    try:
        response = requests.get(url, timeout=4, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            return name, True
        return name, False
    except:
        return name, False

# ৩. স্পেশাল পাবলিক এপিআই/এন্ডপয়েন্ট চেকার (Keybase & HackerNews)
def check_keybase(username):
    try:
        url = f"https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}"
        res = requests.get(url, timeout=4, headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            if data.get("them"):
                return "Keybase", True
    except:
        pass
    return "Keybase", False

def check_hackernews(username):
    try:
        url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
        res = requests.get(url, timeout=4, headers=HEADERS)
        if res.status_code == 200 and res.json() is not None:
            return "HackerNews", True
    except:
        pass
    return "HackerNews", False

# ৪. একসঙ্গে ২০+ সাইট স্ক্যান করার মূল ফাংশন
def scan_email_on_sites(email):
    found_sites = []
    username = email.split('@')[0]
    
    # স্পেশাল প্ল্যাটফর্ম চেক
    kb_name, kb_status = check_keybase(username)
    if kb_status: found_sites.append(kb_name)
    
    hn_name, hn_status = check_hackernews(username)
    if hn_status: found_sites.append(hn_name)

    # জনপ্রিয় ওয়েবসাইটসমূহের তালিকা
    sites = [
        ("GitHub", f"https://github.com/{username}"),
        ("Twitter / X", f"https://twitter.com/{username}"),
        ("SoundCloud", f"https://soundcloud.com/{username}"),
        ("Vimeo", f"https://vimeo.com/{username}"),
        ("Flickr", f"https://www.flickr.com/photos/{username}"),
        ("Behance", f"https://www.behance.net/{username}"),
        ("Dribbble", f"https://dribbble.com/{username}"),
        ("Medium", f"https://medium.com/@{username}"),
        ("Pinterest", f"https://www.pinterest.com/{username}"),
        ("TikTok", f"https://www.tiktok.com/@{username}"),
        ("Reddit", f"https://www.reddit.com/user/{username}"),
        ("Steam", f"https://steamcommunity.com/id/{username}"),
        ("TradingView", f"https://www.tradingview.com/u/{username}"),
        ("Wattpad", f"https://www.wattpad.com/user/{username}"),
        ("SlideShare", f"https://www.slideshare.net/{username}"),
        ("Substack", f"https://{username}.substack.com"),
        ("WordPress", f"https://{username}.wordpress.com"),
        ("Disqus", f"https://disqus.com/by/{username}"),
        ("Last.fm", f"https://www.last.fm/user/{username}"),
        ("Couchsurfing", f"https://www.couchsurfing.com/people/{username}")
    ]

    # মাল্টি-থ্রেডিং (ThreadPoolExecutor) ব্যবহার করে দ্রুত স্ক্যান করা
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_site, name, url): name for name, url in sites}
        for future in futures:
            try:
                name, exists = future.result()
                if exists:
                    found_sites.append(name)
            except:
                pass

    return list(set(found_sites))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
    markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
    
    welcome_text = (
        f"স্বাগতম! 🕵️‍♂️ *API-less Email OSINT Bot*\n\n"
        f"বটটি ব্যবহার করতে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং নিচে *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন।\n\n"
        f"👑 *Credit:* {CREDIT}"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.from_user.id
    verified_users.add(user_id)
    bot.answer_callback_query(call.id, "ভেরিফিকেশন সফল হয়েছে!")
    
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton("🔍 কীভাবে সার্চ করব?"), KeyboardButton("ℹ️ বটের তথ্য"))
    
    edit_text = (
        f"✅ *ভেরিফিকেশন সফল!*\n\n"
        f"এখন চ্যাট বক্সে যেকোনো জিমেইল অ্যাড্রেস লিখে পাঠান (যেমন: `example@gmail.com`)। আমি বিনা এপিআই-তে ২০+ ওয়েবসাইটে স্ক্যান করে অ্যাকাউন্ট, নাম ও ছবি বের করে দেব।\n\n"
        f"👑 *Credit:* {CREDIT}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_text,
        parse_mode="Markdown"
    )
    bot.send_message(call.message.chat.id, "👇 ইমেইল লিখে পাঠান:", reply_markup=reply_markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if text == "🔍 কীভাবে সার্চ করব?":
        bot.reply_to(message, f"💡 **ব্যবহারবিধি:**\nচ্যাট বক্সে সরাসরি যেকোনো ইমেইল অ্যাড্রেস লিখে পাঠিয়ে দিন। যেমন:\n`target@gmail.com`\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    elif text == "ℹ️ বটের তথ্য":
        bot.reply_to(message, f"🤖 **API-less OSINT Scanner v4.0**\nকোনো এপিআই খরচ ছাড়াই সরাসরি ২০+ সাইট ও Gravatar স্ক্যান করে।\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
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
    
    if '@' not in email or '.' not in email:
        bot.reply_to(message, f"❌ দয়া করে একটি সঠিক ইমেইল অ্যাড্রেস পাঠান।\n\n👑 *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    
    processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য ডেটা ও সাইট স্ক্যান করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
    
    try:
        # Gravatar থেকে নাম ও ছবি চেক
        name, avatar = get_gravatar_info(email)
        
        # ২০+ সাইটে স্ক্যান
        matched_sites = scan_email_on_sites(email)
        
        report = f"📊 *API-less OSINT Report*\n"
        report += f"━━━━━━━━━━━━━━━━━━━\n"
        report += f"📧 *Target Email:* `{email}`\n\n"
        
        if name or avatar:
            report += f"👤 *Public Profile Info:*\n"
            if name:
                report += f"• **Name:** {name}\n"
            if avatar:
                report += f"• **Picture:** [View Avatar Link]({avatar})\n"
            report += f"\n"
        
        if matched_sites:
            report += f"✅ *সফলভাবে পাওয়া অ্যাকাউন্ট ({len(matched_sites)} টি):*\n"
            for site in matched_sites:
                report += f"• {site}\n"
        else:
            report += f"⚠️ এই ইমেইলে কোনো পাবলিক অ্যাকাউন্ট বা প্রোফাইল মেলেনি।\n"
            
        report += f"\n━━━━━━━━━━━━━━━━━━━\n"
        report += f"👑 *Developer/Credit:* {CREDIT}"

        bot.edit_message_text(
            report, 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id, 
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
        
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text(
            f"❌ স্ক্যান করার সময় সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n👑 *Credit:* {CREDIT}", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode="Markdown"
        )

# বট রান করা
print("🤖 Final API-less OSINT Bot is running successfully...")
bot.infinity_polling()
