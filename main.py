import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

#       
TOKEN = '8801113765:AAGjrmqclSXw1zDeihGCQSQnERas7tKTozQ'
API_KEY = 'in_rD06OX3qWhOHBM4rdIBV'
GROUP_LINK = 'https://t.me/+inTW2I925HcyMjU1'
CREDIT = '@SHADOW_JOKER_CTH'

bot = telebot.TeleBot(TOKEN)

#        
verified_users = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("    ", url=GROUP_LINK))
    markup.add(InlineKeyboardButton("   ", callback_data="check_join"))
    
    welcome_text = (
        f"!  IntelBase Email Intelligence   \n\n"
        f"        ,   *'  '*   \n\n"
        f" *Credit:* {CREDIT}"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    user_id = call.from_user.id
    verified_users.add(user_id)
    bot.answer_callback_query(call.id, "!    ")
    
    edit_text = (
        f" * !*\n\n"
        f"   (Email)   ,  IntelBase       \n\n"
        f" *Credit:* {CREDIT}"
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_text,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_email_lookup(message):
    user_id = message.from_user.id
    
    #        
    if user_id not in verified_users:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("    ", url=GROUP_LINK))
        markup.add(InlineKeyboardButton("   ", callback_data="check_join"))
        
        bot.reply_to(
            message, 
            f"          *'  '*   !\n\n *Credit:* {CREDIT}", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
        return

    email = message.text.strip()
    
    #   
    if '@' not in email or '.' not in email:
        bot.reply_to(message, f"          (: target@example.com)\n\n *Credit:* {CREDIT}", parse_mode="Markdown")
        return
    
    #   
    processing_msg = bot.reply_to(message, f" `{email}`      ...    ", parse_mode="Markdown")
    
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
                f"   : {data.get('error', ' ')}\n\n *Credit:* {CREDIT}", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="Markdown"
            )
            return
        
        #    
        meta = data.get('meta', {})
        breaches = data.get('data_breaches', {})
        stealer = data.get('stealer_logs', {})
        accounts = data.get('identifier', {}).get('accounts', [])
        
        report = f" *Email Intelligence Report*\n"
        report += f"\n"
        report += f" *Email:* `{meta.get('email', email)}`\n"
        report += f" *First Seen:* {meta.get('first_seen', 'N/A').split('T')[0]}\n"
        report += f" *Last Seen:* {meta.get('last_seen', 'N/A').split('T')[0]}\n\n"
        
        report += f" *Data Breaches:* {breaches.get('amount', 0)}  \n"
        report += f" *Stealer Logs Compromised:* {'  (Compromised)' if stealer.get('compromised') else '  (Safe)'}\n\n"
        
        #       
        if accounts:
            report += f" *Registered Platforms:*\n"
            for acc in accounts[:5]:
                mod = acc.get('module', {})
                name = mod.get('name_formatted', mod.get('name', 'Unknown'))
                domain = mod.get('domain', '')
                if domain:
                    report += f" [{name}](https://{domain})\n"
                else:
                    report += f" {name}\n"
            report += "\n"

        #  
        if breaches.get('results'):
            report += f" *  :*\n"
            for b in breaches.get('results', [])[:3]:
                source_info = b.get('source', {})
                report += f" {source_info.get('name', 'N/A')} ({source_info.get('date', 'N/A')})\n"
        
        report += f"\n\n"
        report += f" *Developer/Credit:* {CREDIT}"

        #   
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
            f"          \n\n *Credit:* {CREDIT}", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id,
            parse_mode="Markdown"
        )

#   
print(" Telegram Bot is running successfully...")
bot.infinity_polling()