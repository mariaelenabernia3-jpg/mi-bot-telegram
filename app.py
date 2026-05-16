import json
import os
import telebot
from flask import Flask, request, abort

app = Flask(__name__)

# Obtener el token del bot de las variables de entorno
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    # Si el token no está configurado, la aplicación no debería iniciar correctamente
    # En un entorno de producción, esto debería ser un error crítico.
    print("Error: La variable de entorno TELEGRAM_BOT_TOKEN no está configurada.")
    # Podrías lanzar una excepción o registrar el error, pero por ahora, el bot no funcionará.
    # Asegúrate de que esta variable esté configurada en Render.
    exit(1) # Salir si el token no está disponible

bot = telebot.TeleBot(BOT_TOKEN)

# --- Manejadores de Mensajes del Bot ---

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    """
    Maneja los comandos /start y /hello.
    """
    bot.reply_to(message, "¡Hola! Soy tu bot de Telegram desplegado en Render. 👋")
    bot.reply_to(message, "Envía /ayuda para ver los comandos disponibles.")

@bot.message_handler(commands=['ayuda'])
def send_help(message):
    """
    Maneja el comando /ayuda.
    """
    help_text = """
    Comandos disponibles:
    /start - Saludo inicial
    /hello - Saludo
    /ayuda - Muestra esta ayuda
    Cualquier otro mensaje te lo repito (echo).
    """
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """
    Maneja cualquier otro mensaje y lo repite (echo).
    """
    bot.reply_to(message, f"Me dijiste: {message.text}")

# --- Endpoint para el Webhook de Telegram ---

# Telegram enviará las actualizaciones a esta ruta
# Es buena práctica incluir el token en la ruta del webhook para una seguridad básica.
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200 # Devolver un 200 OK a Telegram
    else:
        # Si no es una solicitud JSON, es un acceso no autorizado o incorrecto
        abort(403)

# --- Ruta de bienvenida (opcional, para saber que el servicio está activo) ---

@app.route('/')
def home():
    return "Tu bot de Telegram está corriendo en Render. Configura el webhook de Telegram para este servicio."

if __name__ == '__main__':
    # Esto es principalmente para probar localmente. Render usará Gunicorn.
    port = int(os.environ.get('PORT', 5000)) # Render asigna un puerto a través de la variable de entorno PORT
    app.run(host='0.0.0.0', port=port)