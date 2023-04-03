import random
import os
import sys
import time
from controlador import recepcionRepartidores
import pika
#problema en colision entre callback de funcion estoy haciendo un bucle raro entre la recepcion y el envio por accidente, tengo que separar las funciones para que asi tenga sentido
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='repartidores')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='repartidores', on_message_callback=recepcionRepartidores)

    print(" [x] Awaiting robot requests")
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

