import json
import os
import telebot

# Obtener el token del bot de las variables de entorno
# ¡IMPORTANTE! NUNCA hardcodees tu token directamente en el código.
# Lo configuraremos en Netlify más tarde.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: La variable de entorno TELEGRAM_BOT_TOKEN no está configurada.")
    # En un entorno de producción, podrías querer lanzar una excepción o registrar el error.
    # Para este ejemplo, intentaremos continuar, pero el bot no funcionará sin el token.
    # En Netlify Functions, si esto falla, la función simplemente no se inicializará correctamente.

bot = telebot.TeleBot(BOT_TOKEN)

# --- Manejadores de Mensajes del Bot ---

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    """
    Maneja los comandos /start y /hello.
    """
    bot.reply_to(message, "¡Hola! Soy tu bot de Telegram desplegado en Netlify. 👋")
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

# --- Función Principal para Netlify Functions ---

def handler(event, context):
    """
    Esta es la función que Netlify ejecutará cuando reciba una solicitud HTTP.
    """
    if event['httpMethod'] == 'POST':
        # Telegram envía actualizaciones como solicitudes POST
        try:
            # Parsear el cuerpo de la solicitud JSON a un objeto Update de Telebot
            update = telebot.types.Update.de_json(event['body'])
            # Procesar la actualización con el bot
            bot.process_new_updates([update])
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Update processed successfully"})
            }
        except Exception as e:
            print(f"Error procesando la actualización: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({"message": f"Error processing update: {e}"})
            }
    else:
        # Responder a otros métodos HTTP (GET, etc.)
        return {
            'statusCode': 405,
            'body': json.dumps({"message": "Method Not Allowed. This endpoint only accepts POST requests from Telegram."})
        }