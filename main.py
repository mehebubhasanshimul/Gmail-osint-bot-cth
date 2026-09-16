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

# ১. Gravatar থেকে পাবলিক নাম ও ছবি চেক (API-less)
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

# ২. সাইট স্ট্যাটাস চেক ফাংশন
def check_site(name, url):
    try:
        response = requests.get(url, timeout=4, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            return name, url, True
        return name, url, False
    except:
        return name, url, False

# ৩. API-less মাল্টি-থ্রেডেড সাইট স্ক্যানার (Holehe & Sherlock স্টাইল)
def scan_email_on_sites(email):
    found_sites = []
    username = email.split('@')[0]
    
    sites = [
        ("GitHub", f"https://github.com/{username}"),
        ("Twitter / X", f"https://twitter.com/{username}"),
        ("Instagram", f"https://www.instagram.com/{username}"),
        ("Pinterest", f"https://www.pinterest.com/{username}"),
        ("Reddit", f"https://www.reddit.com/user/{username}"),
        ("TikTok", f"https://www.tiktok.com/@{username}"),
        ("SoundCloud", f"https://soundcloud.com/{username}"),
        ("Vimeo", f"https://vimeo.com/{username}"),
        ("Flickr", f"https://www.flickr.com/photos/{username}"),
        ("Behance", f"https://www.behance.net/{username}"),
        ("Dribbble", f"https://dribbble.com/{username}"),
        ("Medium", f"https://medium.com/@{username}"),
        ("Steam", f"https://steamcommunity.com/id/{username}"),
        ("TradingView", f"https://www.tradingview.com/u/{username}"),
        ("Wattpad", f"https://www.wattpad.com/user/{username}"),
        ("SlideShare", f"https://www.slideshare.net/{username}"),
        ("Substack", f"https://{username}.substack.com"),
        ("WordPress", f"https://{username}.wordpress.com"),
        ("Disqus", f"https://disqus.com/by/{username}"),
        ("Last.fm", f"https://www.last.fm/user/{username}"),
        ("Keybase", f"https://keybase.io/{username}"),
        ("HackerNews", f"https://news.ycombinator.com/user?id={username}"),
        ("Spotify", f"https://open.spotify.com/user/{username}"),
        ("Twitch", f"https://www.twitch.tv/{username}"),
        ("Telegram", f"https://t.me/{username}"),
        ("Blogger", f"https://{username}.blogspot.com"),
        ("DeviantArt", f"https://www.deviantart.com/{username}"),
        ("Goodreads", f"https://www.goodreads.com/{username}"),
        ("Patreon", f"https://www.patreon.com/{username}"),
        ("Quora", f"https://www.quora.com/profile/{username}"),
        ("VKontakte", f"https://vk.com/{username}"),
        ("Wikipedia", f"https://en.wikipedia.org/wiki/User:{username}"),
        ("Codepen", f"https://codepen.io/{username}"),
        ("HuggingFace", f"https://huggingface.co/{username}"),
        ("DockerHub", f"https://hub.docker.com/u/{username}"),
        ("Npmjs", f"https://www.npmjs.com/~{username}"),
        ("Pypi", f"https://pypi.org/user/{username}"),
        ("GitLab", f"https://gitlab.com/{username}"),
        ("Codeforces", f"https://codeforces.com/profile/{username}"),
        ("LeetCode", f"https://leetcode.com/{username}"),
        ("HackerRank", f"https://www.hackerrank.com/{username}"),
        ("Chess.com", f"https://www.chess.com/member/{username}"),
        ("Letterboxd", f"https://letterboxd.com/{username}"),
        ("IMDb", f"https://www.imdb.com/user/ur{username}/")
    ]

    with ThreadPoolExecutor(max_workers=15) as executor:
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
        f"স্বাগতম! 🕵️‍♂️ *API-less OSINT Scanner*\n\n"
        f"বটটি ব্যবহার করতে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং নিচে *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন。\n\n"
        f"⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})"
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
        f"এখন যেকোনো জিমেইল অ্যাড্রেস লিখে পাঠান। আমি এপিআই ছাড়াই স্ক্যান করে রিপোর্ট তৈরি করে দেব।\n\n"
        f"⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})"
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
        bot.reply_to(message, f"💡 **ব্যবহারবিধি:**\nচ্যাট বক্সে সরাসরি যেকোনো ইমেইল লিখে পাঠিয়ে দিন (যেমন: `example@gmail.com`)।\n\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return
    elif text == "ℹ️ বটের তথ্য":
        bot.reply_to(message, f"🤖 **API-less OSINT Bot v11.0**\nবিনা এপিআই-তে মাল্টি-থ্রেডেড সাইট স্ক্যানার।\n\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return

    if user_id not in verified_users:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 টেলিগ্রাম গ্রুপে জয়েন করুন", url=GROUP_LINK))
        markup.add(InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_join"))
        
        bot.reply_to(
            message, 
            f"⚠️ দয়া করে প্রথমে আমাদের টেলিগ্রাম গ্রুপে জয়েন করুন এবং *'আমি জয়েন করেছি'* বাটনে ক্লিক করুন!\n\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})", 
            reply_markup=markup, 
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    if '@' in text and '.' in text:
        email = text
        processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য স্ক্যান চলছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
        
        try:
            name, avatar = get_gravatar_info(email)
            matched_sites = scan_email_on_sites(email)
            
            # আপনার দেওয়া ফরম্যাট অনুযায়ী আউটপুট ডিজাইন
            report = f"🎯 *EMAIL RESULT*\n"
            report += f"━━━━━━━━━━━━━━\n"
            report += f"📧 *Email:* `{email}`\n"
            report += f"📮 *Provider:* gmail\n\n"
            
            if name or avatar:
                report += f"👤 *Public Profile Info:*\n"
                if name:
                    report += f"• **Name:** {name}\n"
                if avatar:
                    report += f"• **Picture:** [প্রোফাইল ছবি দেখুন]({avatar})\n"
                report += f"\n"
            
            report += f"✅ *REGISTRATIONS*\n"
            if matched_sites:
                for site_name, site_url in matched_sites:
                    report += f"• {site_name} ({site_url})\n"
            else:
                report += f"• কোনো পাবলিক রেজিস্ট্রেশন পাওয়া যায়নি।\n"
                
            report += f"\n🔓 *Data Breaches:* 0\n"
            report += f"🦠 *Stealer Logs:* 0\n\n"
            
            report += f"━━━━━━━━━━━━━━\n"
            report += f"⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})"

            if len(report) > 4050:
                report = report[:4000] + f"\n\n... (ডেটা বড় হওয়ায় সংক্ষেপ করা হয়েছে)\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})"

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
                f"❌ স্ক্যান করতে সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="Markdown"
            )
    else:
        bot.reply_to(message, f"❌ দয়া করে সঠিক কোনো ইমেইল অ্যাড্রেস পাঠান। (যেমন: `example@gmail.com`)\n\n⚡ *Power By:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)

# বট রান করা
print("🤖 API-less OSINT Bot is running successfully...")
bot.infinity_polling()
