import os
import sys
import traceback
import datetime
import uuid

class Pedidos:
    def __init__(self, c_id: str, p_id: str):
        self.prods = p_id.split(',')
        self.client_id = c_id
        self.state = "creado"
        self.id = uuid.uuid4() 
    def __str__(self):
        return "Pedido: productos = {}; id_cliente = {}; estado = {}; id_pedido = {}".format(self.prods,self.client_id,self.state,self.id)