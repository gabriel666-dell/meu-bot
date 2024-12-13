import os
import telebot
from telebot import types
from mercado_pago import MP  # Certifique-se de instalar o SDK: pip install mercado-pago

# Tokens obtidos das variáveis de ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

# Inicialização do bot e Mercado Pago
bot = telebot.TeleBot(TOKEN)
mp = MP(MERCADO_PAGO_ACCESS_TOKEN)

# Função para iniciar o fluxo de pagamento
@bot.callback_query_handler(func=lambda call: call.data.startswith("comprar_"))
def handle_payment(call):
    product_id = call.data.replace("comprar_", "")
    price = 20  # Ajuste o preço conforme o produto

    # Criar preferência para pagamento no Mercado Pago
    preference_data = {
        "items": [
            {
                "title": product_id.capitalize(),
                "quantity": 1,
                "unit_price": price
            }
        ],
        "back_urls": {
            "success": "https://seusite.com/success",
            "failure": "https://seusite.com/failure",
            "pending": "https://seusite.com/pending"
        }
    }

    preference = mp.preferences().create(preference_data)
    bot.send_message(call.message.chat.id, "Para completar o pagamento, clique no botão abaixo:", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Pagar no Mercado Pago", url=preference['response']['init_point'])))

# Mensagem inicial e criação de botões principais
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🛒 COMPRAR")
    btn2 = types.KeyboardButton("📌 PERFIL")
    btn3 = types.KeyboardButton("💎 RECARGA")
    btn4 = types.KeyboardButton("🆘 SUPORTE")
    btn5 = types.KeyboardButton("🤖 ALUGAR BOT")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, 
                     "Bem-vindo ao *CinePlay Bot*! Escolha uma opção abaixo:",
                     parse_mode="Markdown",
                     reply_markup=markup)

# Função para exibir produtos com botões de pagamento
@bot.message_handler(func=lambda message: message.text == "🛒 COMPRAR")
def show_products(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📺 Netflix - R$20/mês", callback_data="comprar_netflix")
    btn2 = types.InlineKeyboardButton("🎬 Amazon Prime - R$15/mês", callback_data="comprar_prime")
    btn3 = types.InlineKeyboardButton("🎵 Spotify - R$10/mês", callback_data="comprar_spotify")
    btn4 = types.InlineKeyboardButton("📡 IPTV - R$30/mês", callback_data="comprar_iptv")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, 
                     "Escolha o produto que deseja comprar:",
                     reply_markup=markup)

print("Bot está funcionando...")
bot.polling()
