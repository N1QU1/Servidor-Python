import random
import os
import sys
import time
import pika
import string
import threading
import uuid
from cliente import Cliente
from pedidos import Pedidos

# Clase ejecutada por un hilo hijo del proceso interfaz, se encarga de crear la cola de 
# mensajes y de recibir los mensajes de la cola de controlador
class RpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

       
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='controlador',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return self.response

# Funcion ejecutada por el hilo productor de la interfaz
def ColaClienteInit():
    global rpc
    rpc = RpcClient()

# Funcion encargada del envio de un RPC SignIn
def SendSignIn(cliente: Cliente, rpc: RpcClient):
    
    return rpc.call(str(cliente))
# Funcion encargada del envio de un RPC Pedido
def sendPedido(pedido: Pedidos, rpc: RpcClient):
    
    return rpc.call(str(pedido))
def main():
    # Iniciar hilo productor
    client = None
    hilo = threading.Thread(target=ColaClienteInit)
    hilo.start()
    time.sleep(1)
    eject = False

    # Iniciar interfaz
    while (not eject):
        print("What do you want to do?")
        if client == None:
            print("1-sign in")
        else:
            print("Hola {}".format(client.name))
        print("2-hacer pedido")
        print("3-cancelar pedido")
        print("4-apagar")
        value = input()
        if int(value) == 1:
            print("insert your name")
            name = input()
            client = Cliente(name)
            print(SendSignIn(client,rpc))
            print("")
            print("")
           
        elif int(value) == 2:
            print("insertar ids de productos separados por comas")
            ids = input()
            if client == None:
                pedido = Pedidos("", ids)
            else:
                pedido = Pedidos(client.id, ids)
            print(sendPedido(pedido,rpc))
            
        elif int(value) == 3:
            # eliminar pedido
            print("para ti lucas mi amor")
        elif int(value) == 4:
            print("apagando terminal")
            hilo.join()
            eject = True
    

    # apagar la conexion iniciada por el hilo
    #rpc.connection.close()
# Funcion encargada del envio de un signin
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

