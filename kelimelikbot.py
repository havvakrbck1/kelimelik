import telebot
import random

TOKEN = ''  
bot = telebot.TeleBot(TOKEN)


def kelimeleri_yukle():
    with open('kelimeler.txt', 'r', encoding='utf-8') as f:
        return [kelime.strip().lower() for kelime in f if kelime.strip()]

tum_kelimeler = kelimeleri_yukle()
oyuncular = {}


@bot.message_handler(commands=['start', 'basla'])
def baslat(message):
    user_id = message.from_user.id
    kelime = random.choice(tum_kelimeler)
    karisik = ''.join(random.sample(kelime, len(kelime)))
    oyuncular[user_id] = {'kelime': kelime, 'puan': oyuncular.get(user_id, {}).get('puan', 0)}
    bot.reply_to(message, f"Hadi başlayalım! Bu harflerle anlamlı bir kelime bul: 🔤 {karisik}")


@bot.message_handler(func=lambda m: True)
def kontrol_et(message):
    user_id = message.from_user.id
    if user_id in oyuncular:
        cevap = message.text.strip().lower()
        dogru_kelime = oyuncular[user_id]['kelime']
        
        if cevap == dogru_kelime:
            oyuncular[user_id]['puan'] += 1
            bot.reply_to(message, f"🎉 Doğru! Puanın: {oyuncular[user_id]['puan']}")
        else:
            bot.reply_to(message, f"❌ Yanlış. Doğru kelime: {dogru_kelime}")
        
       
        yeni_kelime = random.choice(tum_kelimeler)
        karisik = ''.join(random.sample(yeni_kelime, len(yeni_kelime)))
        oyuncular[user_id]['kelime'] = yeni_kelime
        bot.send_message(message.chat.id, f"Yeni kelime geliyor! 🔤 {karisik}")

@bot.message_handler(commands=['puan'])
def puan_goster(message):
    user_id = message.from_user.id
    puan = oyuncular.get(user_id, {}).get('puan', 0)
    bot.reply_to(message, f"🎯 Şu anki puanınız: {puan}")

bot.polling()
