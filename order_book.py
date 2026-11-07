from trade import Trade

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []
        self.trade_sequence = 0

    def add_order(self, order):
        self._validate_order(order)
        if order.side == "BUY":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)

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
        self._validate_order(order)
        while order.quantity > 0:
            opposite_orders = (self.sell_orders if order.side == "BUY" else self.buy_orders)
            best_opposite = (self.get_best_ask() if order.side == "BUY" else self.get_best_bid())
            if best_opposite is not None and ((order.price >= best_opposite.price and order.side == "BUY") or (order.price <= best_opposite.price and order.side == "SELL")):
                buy_id = order.order_id if order.side == "BUY" else best_opposite.order_id
                sell_id = best_opposite.order_id if order.side == "BUY" else order.order_id
                traded_quantity = min(best_opposite.quantity, order.quantity)
                order.quantity -= traded_quantity
                best_opposite.quantity -= traded_quantity
                if best_opposite.quantity == 0:
                    opposite_orders.remove(best_opposite)
                self.trade_sequence += 1
                self.trades.append(Trade(buy_id, sell_id, best_opposite.price, traded_quantity, self.trade_sequence))
            else:
                self.add_order(order)
                break

    def _validate_order(self, order):
        """Validate an incoming order's side and unique ID."""
        if order.side not in ("BUY", "SELL"):
            raise ValueError("Invalid side")

        if any(
                existing_order.order_id == order.order_id
                for existing_order in self.buy_orders + self.sell_orders
        ):
            raise ValueError("Duplicate order ID")