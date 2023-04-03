import random
import os
import sys
import time
from controlador import RecepcionRepartidores
import pika


def main():
    con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    ch = con.channel()

    ch.queue_declare(queue='repartidores')

    ch.basic_consume(on_message_callback = RecepcionRepartidores, queue='repartidores', auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    ch.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
print("Cola abierta.")
