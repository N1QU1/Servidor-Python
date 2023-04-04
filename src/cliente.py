import uuid 
import pika
import sys
import os


class Cliente:
    def __init__(self, name):
        self.name = name
        self.pedidos = []
        self.id = uuid.uuid4()

    def VerPedidos(self):
        for pedido in self.pedidos:
            print(pedido)
        return
    def __str__(self):
        ids = ""
        for ele in self.pedidos:
            ids+= str(ele)
            ids+= ','
        return "Cliente: [name = {}; pedidos = {}; id = {}]".format(self.name,ids[:-1],self.id)