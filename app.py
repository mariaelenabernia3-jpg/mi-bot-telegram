import os
import telebot
from flask import Flask, request

# Tu token configurado directamente
TOKEN = "8993099784:AAHDi55-1qf4Fm6UEwYirFpPCOyWDDyVSc8"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Rutas del Bot ---

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """
    Ruta que recibe las actualizaciones de Telegram
    """
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return "El bot de Telegram está activo y funcionando en Render."

# --- Manejadores de mensajes ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    respuesta = f"¡Hola {user_name}! 👋\n\nBienvenido a mi bot desplegado en Render.\n\n¿En qué puedo ayudarte hoy?"
    bot.reply_to(message, respuesta)

@bot.message_handler(commands=['ayuda'])
def send_help(message):
    bot.reply_to(message, "Comandos disponibles:\n/start - Saludo inicial\n/ayuda - Esta lista de comandos")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Esto responde a cualquier otro mensaje que no sea un comando
    bot.reply_to(message, f"Has dicho: '{message.text}'. ¡Entendido!")

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
