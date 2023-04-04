import random
import os
import sys
import time
import pika
import threading

def parseBody(body:str):
    
    if body.find('Cliente:') >= 0:
        print("{}".format(body))
        return ""
    
    elif body.find('Pedido:') >= 0:
        for ele in body.split(";",3):
            if ele.find("id_cliente") >= 0:    
                for value in ele.split("="):
                    if value == " ":
                        return "error"
                else:   
                    print("{}".format(body))
                    return "robot"
                
    elif body.find('Robot:') >= 0:
        if body.find("not found") >= 0:
            return "not found"
        print("{}".format(body))
        return "repartidor"

def on_request(ch, method, props, body):
    verif = parseBody(str(body))
    if verif == "":
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="Cliente: Recibido")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    elif verif == "error":
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="Pedido: incorrecto")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        
        if verif == "repartidor":
            ch.basic_publish(exchange='',
                        routing_key="repartidor",
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body=body)
        elif verif == "not found":
            print("not enough products")
        
        elif 'robot':
            ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body="Pedido: correcto ")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
            ch.basic_publish(exchange='',
                        routing_key="robot",
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body=body)
 
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='controlador', durable=False, auto_delete=True)

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




