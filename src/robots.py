import random
import os
import sys
import time
import pika
from controlador import recepcionRobots
    

def main():
    con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    ch = con.channel()

    ch.queue_declare(queue='robots')

    ch.basic_consume(on_message_callback = recepcionRobots, queue='robots', auto_ack=True)
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


