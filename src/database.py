import pickle
import pedidos

"""
La clase DatabaseController debera encapsular la siguiente
funcionalidad: registro de usuarios y almacenamiento 
de los pedidos de cada cliente.
""" 
class DatabaseController:
    def __init__(self, filename) -> None:
        self.file = filename
        # self.users = {"id1": "user1","user2": "id2"}
        self.users = {}
        # self.orders = {"id1": ["order_id1", "order_id2"], "id2": ["order_id3"]}
        self.orders = {}

    def register(self, id, username) -> bool:
        if id not in self.users:
            self.users[id] = username
            return True
        else:
            return False
        
    def userIsRegistered(self, id) -> bool:
        return id in self.users

    def addOrder(self, id, order: pedidos.Pedido) -> None:
        if id in self.orders:
            self.orders[id].append(order)
        else:
            self.orders[id] = [order]

    def getOrders(self, username):
        return self.orders[username]
    
    def cancelOrder(self, id, order: pedidos.Pedido):
        if id in self.orders:
            self.orders[id].remove(order)

    # def setStateOrder(self, )

    def save(self):
        with open(self.file, "wb") as f:
            pickle.dump((self.users, self.orders), f)

# Tests para DatabaseController
