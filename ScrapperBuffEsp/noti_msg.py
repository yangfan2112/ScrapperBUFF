import telebot

# Token del bot de Telegram
TOKEN = '6540640494:AAHDkgxzv54rXSP1w-KRDLvxWS6cbJNYijE'

# Crear una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Función para enviar el mensaje
def enviar_mensaje(skin, media_precios, skin_barata):
    chat_id = '6554298004'  # ID del chat al que quieres enviar el mensaje
    mensaje = f'Se ha encontrado la skin {skin} por debajo del 85%. Precio medio: {media_precios} || Skin encontrada: {skin_barata}.'

    # Enviar el mensaje
    bot.send_message(chat_id, mensaje)
