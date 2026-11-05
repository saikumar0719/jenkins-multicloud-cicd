from app.main import clean_orders, load_orders, total_sales


def test_clean_removes_duplicates_missing_and_negative():
    rows = [
        {"order_id": "1", "customer": "A", "product": "Bag", "amount": "100"},
        {"order_id": "1", "customer": "A", "product": "Bag", "amount": "150"},
        {"order_id": "2", "customer": "B", "product": "Hat", "amount": ""},
        {"order_id": "3", "customer": "C", "product": "Hat", "amount": "-50"},
        {"order_id": "4", "customer": "D", "product": "Shoes", "amount": "200"},
    ]
    clean = clean_orders(rows)
    assert [r["order_id"] for r in clean] == ["1", "4"]
    assert clean[0]["amount"] == 150  # last duplicate wins
    assert total_sales(clean) == 350


def test_sample_data_total():
    clean = clean_orders(load_orders())
    # 11 raw rows - 1 duplicate - 1 missing - 1 negative = 8 clean orders
    assert len(clean) == 8
    assert total_sales(clean) == 10550.00
