from order import Order
from order_book import OrderBook


def main():
    # Initialize order book
    book = OrderBook()

    # Create orders
    sell1 = Order(1, "SELL", 100, 5, 1)
    sell2 = Order(2, "SELL", 101, 8, 2)
    buy1 = Order(3, "BUY", 102, 10, 3)

    # Add existing sell orders
    book.add_order(sell1)
    book.add_order(sell2)

    # Match incoming buy order
    book.match_order(buy1)

    # Display executed trades
    print("=== Trade History ===")

    for trade in book.trades:
        print(f"Buy ID: {trade.buy_order_id}")
        print(f"Sell ID: {trade.sell_order_id}")
        print(f"Price: ${trade.price}")
        print(f"Quantity: {trade.quantity}")
        print(f"Execution Sequence: {trade.timestamp}")
        print("--------------------")

    # Display remaining orders
    print("\n=== Remaining Orders ===")

    for order in book.buy_orders:
        print(f"BUY #{order.order_id}: {order.quantity} @ ${order.price}")

    for order in book.sell_orders:
        print(f"SELL #{order.order_id}: {order.quantity} @ ${order.price}")


if __name__ == "__main__":
    main()