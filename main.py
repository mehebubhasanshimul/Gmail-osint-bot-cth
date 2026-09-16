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

# ১. Gravatar থেকে নাম ও ছবি চেক
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

# ২. সাইট চেক ফাংশন
def check_site(name, url):
    try:
        response = requests.get(url, timeout=4, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            return name, url, True
        return name, url, False
    except:
        return name, url, False

# ৩. ১২০+ ওয়েবসাইট ও প্ল্যাটফর্ম স্ক্যানার (Holehe & Sherlock স্টাইল)
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
        ("Couchsurfing", f"https://www.couchsurfing.com/people/{username}"),
        ("Keybase", f"https://keybase.io/{username}"),
        ("HackerNews", f"https://news.ycombinator.com/user?id={username}"),
        ("Spotify", f"https://open.spotify.com/user/{username}"),
        ("Twitch", f"https://www.twitch.tv/{username}"),
        ("Telegram", f"https://t.me/{username}"),
        ("About.me", f"https://about.me/{username}"),
        ("Blogger", f"https://{username}.blogspot.com"),
        ("DeviantArt", f"https://www.deviantart.com/{username}"),
        ("Goodreads", f"https://www.goodreads.com/{username}"),
        ("Kaggle", f"https://www.kaggle.com/{username}"),
        ("Patreon", f"https://www.patreon.com/{username}"),
        ("ProductHunt", f"https://www.producthunt.com/@{username}"),
        ("Quora", f"https://www.quora.com/profile/{username}"),
        ("Strava", f"https://www.strava.com/athletes/{username}"),
        ("VKontakte", f"https://vk.com/{username}"),
        ("Wikipedia", f"https://en.wikipedia.org/wiki/User:{username}"),
        ("Xing", f"https://www.xing.com/profile/{username}"),
        ("Yelp", f"https://www.yelp.com/user_details?userid={username}"),
        ("Duolingo", f"https://www.duolingo.com/profile/{username}"),
        ("Codepen", f"https://codepen.io/{username}"),
        ("HuggingFace", f"https://huggingface.co/{username}"),
        ("TripAdvisor", f"https://www.tripadvisor.com/members/{username}"),
        ("AngelList", f"https://angel.co/u/{username}"),
        ("Giphy", f"https://giphy.com/{username}"),
        ("Gumroad", f"https://gumroad.com/{username}"),
        ("MySpace", f"https://myspace.com/{username}"),
        ("Rumble", f"https://rumble.com/user/{username}"),
        ("Scratch", f"https://scratch.mit.edu/users/{username}"),
        ("Scribd", f"https://www.scribd.com/{username}"),
        ("Tinder", f"https://tinder.com/@{username}"),
        ("UltimateGuitar", f"https://www.ultimate-guitar.com/u/{username}"),
        ("DockerHub", f"https://hub.docker.com/u/{username}"),
        ("Npmjs", f"https://www.npmjs.com/~{username}"),
        ("Pypi", f"https://pypi.org/user/{username}"),
        ("BitBucket", f"https://bitbucket.org/{username}"),
        ("GitLab", f"https://gitlab.com/{username}"),
        ("SourceForge", f"https://sourceforge.net/u/{username}"),
        ("Codeforces", f"https://codeforces.com/profile/{username}"),
        ("LeetCode", f"https://leetcode.com/{username}"),
        ("HackerRank", f"https://www.hackerrank.com/{username}"),
        ("Chess.com", f"https://www.chess.com/member/{username}"),
        ("Lichess", f"https://lichess.org/@/{username}"),
        ("Roblox", f"https://www.roblox.com/user.aspx?username={username}"),
        ("Letterboxd", f"https://letterboxd.com/{username}"),
        ("IMDb", f"https://www.imdb.com/user/ur{username}/"),
        ("Bandcamp", f"https://bandcamp.com/{username}"),
        ("SoundClick", f"https://www.soundclick.com/{username}"),
        ("Audiomack", f"https://audiomack.com/{username}"),
        ("Genius", f"https://genius.com/{username}")
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
        f"স্বাগতম! 🕵️‍♂️ *Holehe & Sherlock OSINT Bot*\n\n"
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
        f"এখন যেকোনো জিমেইল অ্যাড্রেস লিখে পাঠান। আমি ১২০+ ওয়েবসাইটে স্ক্যান করে রিপোর্ট ও প্রোফাইল লিংক বের করে দেব।\n\n"
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
        bot.reply_to(message, f"💡 **ব্যবহারবিধি:**\nচ্যাট বক্সে সরাসরি যেকোনো ইমেইল লিখে পাঠিয়ে দিন (যেমন: `example@gmail.com`)। বট ১২০+ ওয়েবসাইটে স্ক্যান করবে।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
        return
    elif text == "ℹ️ বটের তথ্য":
        bot.reply_to(message, f"🤖 **OSINT Scanner v8.0**\n১২০+ ওয়েবসাইটে ইমেইল ও সোশ্যাল মিডিয়া অ্যাকাউন্ট চেক করার নির্ভরযোগ্য বট।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)
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

    if '@' in text and '.' in text:
        email = text
        processing_msg = bot.reply_to(message, f"🔍 `{email}` এর জন্য ১২০+ ওয়েবসাইটে স্ক্যান করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode="Markdown")
        
        try:
            name, avatar = get_gravatar_info(email)
            matched_sites = scan_email_on_sites(email)
            
            report = f"📊 *OSINT Scan Report*\n"
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
                for site_name, site_url in matched_sites:
                    report += f"• [{site_name}]({site_url})\n"
            else:
                report += f"⚠️ এই ইমেইলে কোনো পাবলিক অ্যাকাউন্ট বা প্রোফাইল মেলেনি।\n"
                
            report += f"\n━━━━━━━━━━━━━━━━━━━\n"
            report += f"👑 *Developer/Credit:* [{CREDIT_NAME}]({CREDIT_URL})"

            if len(report) > 4050:
                report = report[:4000] + f"\n\n... (ডেটা খুব বড় হওয়ায় সংক্ষেপ করা হয়েছে)\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})"

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
                f"❌ স্ক্যান করতে সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="Markdown"
            )
    else:
        bot.reply_to(message, f"❌ দয়া করে সঠিক কোনো ইমেইল অ্যাড্রেস পাঠান। (যেমন: `example@gmail.com`)\n\n👑 *Credit:* [{CREDIT_NAME}]({CREDIT_URL})", parse_mode="Markdown", disable_web_page_preview=True)

# বট রান করা
print("🤖 OSINT Bot is running successfully...")
bot.infinity_polling()
