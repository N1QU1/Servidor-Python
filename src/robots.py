import random
import os
import sys
import time
import pika
import threading
def recepcionRobots(ch, method, props, body):
    print("Mensaje recibido con exito" )
    hilo = threading.Thread(target = work, args = (ch,method,props,body))
    hilo.start()
    return

def work(ch, method, props, body):
    wait = random.randint(5,10)
    probability = random.randint(0,10)
    ceiling = random.randint(0,10)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    ch = connection.channel()

        
    if (probability >= ceiling):
        time.sleep(wait)
        print("Envio de pedido")
        ch.basic_publish(exchange='', routing_key="controlador",properties=pika.BasicProperties(correlation_id = props.correlation_id), body = "Robot: Id_pedido {}".format(parseBody(body)[:-1]))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Products not found")
        ch.basic_publish(exchange='', routing_key="controlador",properties=pika.BasicProperties(correlation_id = props.correlation_id), body = "Robot: not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def parseBody(body):
    body = str(body)
    i = 0
    for ele in body.split(";",3):
        if ele.find("id_pedido") >= 0:
            for value in ele.split(" = ", 1):
                if i == 1:
                    return value
                else:
                    i+=1
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='robot', durable=False, auto_delete=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='robot', on_message_callback=recepcionRobots)

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


                 

    