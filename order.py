class Order:
    def __init__(self, order_id, side, price, quantity, timestamp):
        if quantity <= 0:
            raise ValueError("Invalid quantity")
        if price <= 0:
            raise ValueError("Invalid price")
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp

class Orderbook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == "BUY":
            self.buy_orders.append(order)
        elif order.side == "SELL":
            self.sell_orders.append(order)
        else:
            raise ValueError("Invalid side")

    def get_best_bid(self):
        if len(self.buy_orders) == 0:
            return None
        return max(self.buy_orders, key = lambda order: (order.price, -order.timestamp))

    def get_best_ask(self):
        if len(self.sell_orders) == 0:
            return None
        return min(self.sell_orders, key=lambda order: (order.price, order.timestamp))

    def cancel_order(self, cancel_id):
        for order in self.buy_orders:
            if order.order_id == cancel_id:
                self.buy_orders.remove(order)
                return True
        for order in self.sell_orders:
            if order.order_id == cancel_id:
                self.sell_orders.remove(order)
                return True
        return False

    def get_spread(self):
        if len(self.buy_orders) == 0 or len(self.sell_orders) == 0:
            return None
        return (self.get_best_ask().price - self.get_best_bid().price)

    def match_order(self, order):
        while order.quantity > 0:
            opposite_orders = (self.sell_orders if order.side == "BUY" else self.buy_orders)
            best_opposite = (self.get_best_ask() if order.side == "BUY" else self.get_best_bid())
            if best_opposite is not None and ((order.price >= best_opposite.price and order.side == "BUY") or (order.price <= best_opposite.price and order.side == "SELL")):
                traded_quantity = min(best_opposite.quantity, order.quantity)
                order.quantity -= traded_quantity
                best_opposite.quantity -= traded_quantity
                if best_opposite.quantity == 0:
                    opposite_orders.remove(best_opposite)
            else:
                self.add_order(order)
                break




