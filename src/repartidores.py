import random
import os
import sys
import time
import threading
import pika
#problema en colision entre callback de funcion estoy haciendo un bucle raro entre la recepcion y el envio por accidente, tengo que separar las funciones para que asi tenga sentido

def recepcionRepartidor(ch, method, props, body):
    print("Mensaje recibido con exito" )
    hilo = threading.Thread(target = work, args = (ch,method,props,body))
    hilo.start() 
    return

def work(ch, method, properties, body):
    
    counter = 0
    probability = random.randint(0,10)
    wait = random.randint(10,20)
    while (probability != random.randint(0,10)):
        if (counter == 2):
            print("Intentos agotados, no hay nadie en casa")
            return
        time.sleep(wait)
        counter += 1
    print("Mensaje llego con exito")

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='repartidor', durable=False, auto_delete=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='repartidor', on_message_callback=recepcionRepartidor)

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



