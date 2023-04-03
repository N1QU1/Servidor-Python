import random
import os
import sys
import time
import pika
from controlador import recepcionRobots
    

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='controlador')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='controlador', on_message_callback=recepcionRobots)

    print(" [x] Awaiting controller requests")
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


