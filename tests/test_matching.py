import pytest
from order import Order
from order_book import OrderBook

def test_empty_order_book():
    book = OrderBook()

    assert book.get_best_bid() is None
    assert book.get_best_ask() is None
    assert book.get_spread() is None

def test_partial_fill():
    book = OrderBook()

    book.add_order(Order(1, "SELL", 100, 10, 1))
    book.match_order(Order(2, "BUY", 105, 4, 2))

    assert len(book.trades) == 1
    assert book.trades[0].quantity == 4
    assert book.trades[0].price == 100
    assert book.sell_orders[0].quantity == 6
    assert not book.buy_orders

def test_price_time_priority():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 100, 10, 3))
    book.add_order(Order(2, "SELL", 100, 10, 1))
    book.add_order(Order(3, "SELL", 100, 10, 2))
    book.match_order(Order(4, "BUY", 105, 5, 3))

    assert len(book.trades) == 1
    assert book.trades[0].sell_order_id == 2
    assert next((order.quantity for order in book.sell_orders if order.order_id == 2), None) == 5

def test_invalid_price():
    with pytest.raises(ValueError):
        Order(1, "BUY", 0, 10, 1)

def test_invalid_quantity():
    with pytest.raises(ValueError):
        Order(1, "BUY", 100, -10, 1)

def test_cancel_existing_order():
    book = OrderBook()
    book.add_order(Order(1, "BUY", 100, 10, 1))

    assert book.cancel_order(1)
    assert not book.buy_orders

def test_cancel_nonexistent_order():
    book = OrderBook()

    assert book.cancel_order(999) == False

def test_multiple_price_levels():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 100, 5, 1))
    book.add_order(Order(2, "SELL", 101, 8, 2))
    book.add_order(Order(3, "SELL", 102, 10, 3))
    book.match_order(Order(4, "BUY", 102, 15, 4))

    assert len(book.trades) == 3
    assert [trade.price for trade in book.trades] == [100, 101, 102]
    assert [trade.quantity for trade in book.trades] == [5, 8, 2]
    assert book.sell_orders[0].order_id == 3 and book.sell_orders[0].quantity == 8
    assert not book.buy_orders

def test_non_crossing_orders():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 105, 10, 1))
    book.match_order(Order(2, "BUY", 100, 5, 2))

    assert not book.trades
    assert book.sell_orders[0].order_id == 1 and book.buy_orders[0].order_id == 2
    assert book.get_best_bid().price == 100
    assert book.get_best_ask().price == 105
    assert book.get_spread() == 5

def test_full_fill():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 100, 10, 1))
    book.match_order(Order(2, "BUY", 100, 10, 2))

    assert len(book.trades) == 1
    assert not book.sell_orders and not book.buy_orders

def test_duplicate_order_id():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 100, 10, 1))
    with pytest.raises(ValueError):
         book.add_order(Order(1, "BUY", 100, 10, 2))

def test_duplicate_id_during_matching():
    book = OrderBook()
    book.add_order(Order(1, "SELL", 100, 10, 1))
    with pytest.raises(ValueError):
        book.match_order(Order(1, "BUY", 105, 5, 2))
    assert not book.trades

def test_invalid_side_during_matching():
    book = OrderBook()
    book.add_order(Order(1, "BUY", 100, 10, 1))
    with pytest.raises(ValueError):
        book.match_order(Order(2, "INVALID", 90, 5, 2))
    assert not book.trades
    assert book.buy_orders[0].quantity == 10



