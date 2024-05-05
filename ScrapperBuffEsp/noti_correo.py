import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo():
    # Configuración del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    correo_emisor = 'ivanluyangfan15@gmail.com'
    password = 'ivan699424771'

    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = correo_emisor
    msg['To'] = 'ivanluyangfan21@gmail.com'
    msg['Subject'] = 'Notificación de skin encontrada'

    # Cuerpo del mensaje
    mensaje = 'Se ha encontrado la skin por debajo del 85%'

    # Adjuntar el mensaje al objeto del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Iniciar sesión en el servidor SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(correo_emisor, password)
        server.send_message(msg)
