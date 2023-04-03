import random
import os
import sys
import time
import pika
import threading

def recepcionRepartidores(ch, method, properties, body):
    
    counter = 0
    probability = random.randint(0,10)
    wait = random.randint(10,20)
    while (probability != random.randint(0,10)):
        if (counter == 2):
            print("Bro estas en casa?")
            return
        time.sleep(wait)
        counter += 1
    print("Mensaje llego con exito")

def recepcionRobots(ch, method, props, body):
    wait = random.randint(5,10)
    probability = random.randint(0,10)
    ceiling = random.randint(0,10)

    if (probability >= ceiling):
        time.sleep(wait)
        ch.basic_publish(exchange='', routing_key=props.reply_to,properties=pika.BasicProperties(correlation_id = props.correlation_id), body = body)
        
    else:
        print("dame una alegria")
        ch.basic_publish(exchange='', routing_key=props.reply_to,properties=pika.BasicProperties(correlation_id = props.correlation_id), body = "Not enough products")
        return
    
    return


def parseBody(body:str):
    print(body.find('Cliente:'))
    if body.find('Cliente:') >= 0:
        print("Client signup efectivo {}".format(body))
        return ""
    elif body.find('Pedido:') >= 0:
        for ele in body.split(";",3):
            if ele.find("id_cliente") >= 0:    
                for value in ele.split("="):
                    if value == " ":
                        return "error"
                else:   
                    print("Formato de pedido correcto: {}".format(body))
                    return "robot"
    elif body.find('Robot:') >= 0:
        print("Elementos suficientes: {}".format(body))
        return "repartidor"

def on_request(ch, method, props, body):
    verif = parseBody(str(body))
    if verif == "":
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="recibido correctamente")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    elif verif == "error":
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="Pedido incorrecto")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        if verif == "repartidores":
            hilo = threading.Thread(target=recepcionRepartidores, args = (ch, method, props, body))
            hilo.start()
        else: 
            ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="Pedido correcto")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #echar un ojo al envio de mensaje

            hilo = threading.Thread(target=recepcionRobots, args = (ch, method, props, body))
            hilo.start()
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='controlador')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='controlador', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
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




