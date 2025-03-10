import random
import os
import sys
import time
import pika
import threading
def recepcionRobots(ch, method, props, body):
    hilo = threading.Thread(target = work, args = (ch,method,props,body))
    hilo.start()
    return
def sendMessage(ch, method, props, body):
    ch.basic_publish(exchange='', routing_key='controlador',properties=pika.BasicProperties(correlation_id = props.correlation_id), body = body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

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
        sendMessage(ch, method, props, "Robot: Id_pedido {}".format(parseBody(body)[:-1]))
    
    else:    
        print("Products not found")
        sendMessage(ch, method, props, "Robot: not found")
    

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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='robot', durable=False, auto_delete=True)

    channel.basic_consume(queue='robot', on_message_callback=recepcionRobots, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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


                 

    