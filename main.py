# -*- coding: utf-8 -*-
import telebot
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# কনফিগারেশন
TOKEN = '8801113765:AAGjrmqclSXw1zDeihGCQSQnERas7tKTozQ'
GROUP_LINK = 'https://t.me/+inTW2I925HcyMjU1'
CREDIT_NAME = '@SHADOW_JOKER_CTH'
CREDIT_URL = 'https://t.me/SHADOW_JOKER_CTH'

bot = telebot.TeleBot(TOKEN)
verified_users = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Gravatar থেকে নাম ও ছবি চেক
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

# সাইট চেক ফাংশন (নাম এবং ইউআরএল সহ রিটার্ন করবে)
def check_site(name, url):
    try:
        response = requests.get(url, timeout=4, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            return name, url, True
        return name, url, False
    except:
        return name, url, False

# Keybase চেক
def check_keybase(username):
    try:
        url = f"https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}"
        res = requests.get(url, timeout=4, headers=HEADERS)
        if res.status_code == 200:
            data = res.json()
            if data.get("them"):
                return "Keybase", f"https://keybase.io/{username}", True
    except:
        pass
    return "Keybase", "", False

# HackerNews চেক
def check_hackernews(username):
    try:
        url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
        res = requests.get(url, timeout=4, headers=HEADERS)
        if res.status_code == 200 and res.json() is not None:
            return "HackerNews", f"https://news.ycombinator.com/user?id={username}", True
    except:
        pass
    return "HackerNews", "", False

# সাইট স্ক্যান করার মূল ফাংশন
def scan_email_on_sites(email):
    found_sites = []
    username = email.split('@')[0]
    
    # স্পেশাল প্ল্যাটফর্ম চেক
    kb_name, kb_url, kb_status = check_keybase(username)
    if kb_status: found_sites.append((kb_name, kb_url))
    
    hn_name, hn_url, hn_status = check_hackernews(username)
    if hn_status: found_sites.append((hn_name, hn_url))

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

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_site, name, url): (name, url) for name, url in sites}
        for future in futures:
            try:
                name, url, exists = future.result()
                if exists:
                    found_sites.append((name, url))
            except:
                pass

    return found_sites

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
    markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
    
    welcome_text = (
        f"স্বাগতম! 🕵️‍♂️ *API-less Email OSINT Bot*\n\n"
        f"বটটি ব্যবহার করতে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং নিচে *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন।\n\n"
        f"👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.from_user.id
    verified_users.add(user_id)
    bot.answer_callback_query(call.id, "ভেরিফিকেশন সফল হয়েছে!")
    
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton("🔍 কীভাবে সার্চ করব?"), KeyboardButton("ℹ️ বটের তথ্য"))
    
    edit_text = (
        f"✅ *ভেরিফিকেশন সফল!*\n\n"
        f"এখন চ্যাট বক্সে যেকোনো জিমেইল অ্যাড্রেস লিখে পাঠান। আমি সরাসরি ক্লিকযোগ্য লিংক সহ অ্যাকাউন্ট রিপোর্ট বের করে দেব।\n\n"
        f"👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    bot.send_message(call.message.chat.id, "👇 ইমেইল লিখে পাঠান:", reply_markup=reply_markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if text == "🔍 কীভাবে সার্চ করব?":
        bot.reply_to(message, f"💡 **ব্যবহারবিধি:**\nচ্যাট বক্সে সরাসরি যেকোনো ইমেইল অ্যাড্রেস লিখে পাঠিয়ে দিন।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return
    elif text == "ℹ️ বটের তথ্য":
        bot.reply_to(message, f"🤖 **API-less OSINT Scanner v5.0**\nক্লিকযোগ্য লিংক সহ সরাসরি সোশ্যাল মিডিয়া অ্যাকাউন্ট চেক করে।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return

    if user_id not in verified_users:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
        markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
        
        bot.reply_to(
            message, 
            f"⚠️ দয়া করে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন!\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", 
            reply_markup=markup, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    email = text
    
    if '@' not in email or '.' not in email:
        bot.reply_to(message, f"❌ দয়া করে একটি সঠিক ইমেইল অ্যাড্রেস পাঠান।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return
    
    processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য ডেটা ও সাইট স্ক্যান করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
    
    try:
        name, avatar = get_gravatar_info(email)
        matched_sites = scan_email_on_sites(email)
        
        report = f"📊 *API-less OSINT Report*\n"
        report += f"━━━━━━━━━━━━━━━━━━━\n"
        report += f"📧 *Target Email:* `{email}`\n\n"
        
        if name or avatar:
            report += f"👤 *Public Profile Info:*\n"
            if name:
                report += f"• **Name:** {name}\n"
            if avatar:
                report += f"• **Picture:** [প্রোফাইল ছবি দেখুন]({avatar})\n"
            report += f"\n"
        
        if matched_sites:
            report += f"✅ *সফলভাবে পাওয়া অ্যাকাউন্ট ({len(matched_sites)} টি):*\n"
            # প্রতিটি প্ল্যাটফর্মের পাশে সরাসরি ক্লিকযোগ্য লিংক যুক্ত করা হলো
            for site_name, site_url in matched_sites:
                report += f"• [{site_name}]({site_url})\n"
        else:
            report += f"⚠️ এই ইমেইলে কোনো পাবলিক অ্যাকাউন্ট বা প্রোফাইল মেলেনি।\n"
            
        report += f"\n━━━━━━━━━━━━━━━━━━━\n"
        report += f"👑 *Developer/Credit:* [{CREDIT_NAME}]({CREDIT_URL})"

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
            f"❌ স্ক্যান করার সময় সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

# বট রান করা
print("🤖 Final Fixed OSINT Bot is running successfully...")
bot.infinity_polling()
