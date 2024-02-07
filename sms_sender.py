import serial
import time

# Configuración de la conexión serial con el módulo SIM7000G
puerto_serial = '/dev/ttyS0'  # Asegúrate de cambiar esto por tu puerto correcto
baudios = 115200
timeout = 1  # Timeout para la lectura de datos

# Función para enviar comandos AT al módulo
def enviar_comando(comando, tiempo_espera=2):
    with serial.Serial(puerto_serial, baudios, timeout=timeout) as ser:
        ser.write((comando + '\r\n').encode())  # Envía el comando
        time.sleep(tiempo_espera)  # Espera para que el comando se ejecute
        while ser.inWaiting() > 0:
            respuesta = ser.read(ser.inWaiting()).decode()  # Lee la respuesta
            print(respuesta)  # Imprime la respuesta para depuración

# Función principal para enviar un mensaje SMS
def enviar_sms(numero, mensaje):
    print("Inicializando módem...")
    enviar_comando('AT')  # Verifica la comunicación con el módem
    enviar_comando('AT+CMGF=1')  # Configura el módem en modo texto para SMS
    print("Enviando mensaje...")
    enviar_comando(f'AT+CMGS="{numero}"', 1)  # Comando para iniciar el envío del SMS
    with serial.Serial(puerto_serial, baudios, timeout=timeout) as ser:
        ser.write((mensaje + '\x1a').encode())  # Envía el mensaje y Ctrl+Z para enviar
        time.sleep(3)  # Espera a que el mensaje se envíe
        while ser.inWaiting() > 0:
            respuesta = ser.read(ser.inWaiting()).decode()
            print(respuesta)  # Imprime la respuesta para depuración

# Número al que se enviará el mensaje y el contenido del mensaje
numero_destino = '+593999098696'  # Cambia esto por el número al que deseas enviar el mensaje
mensaje_sms = 'Hola Mundo'

# Llamada a la función para enviar el SMS
enviar_sms(numero_destino, mensaje_sms)

