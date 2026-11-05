"""Tiny shop app.

In simple words: a shop gets messy orders. This small program
cleans the orders and prints the true total sales.

Cleaning rules (same story as the data-pipeline project):
- the same order written two times -> keep only the last row
- an order with no amount -> drop it
- an order with a negative amount -> drop it
"""

import csv
import pathlib

DATA_FILE = pathlib.Path(__file__).with_name("sample_orders.csv")


def load_orders(path=DATA_FILE):
    """Read the orders file and return a list of rows (dicts)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean_orders(rows):
    """Clean messy rows. Returns a list of clean order dicts."""
    by_id = {}
    for row in rows:
        order_id = (row.get("order_id") or "").strip()
        amount_text = (row.get("amount") or "").strip()
        if not order_id or not amount_text:
            continue  # no order id or no amount -> drop the row
        try:
            amount = float(amount_text)
        except ValueError:
            continue  # amount is not a number -> drop the row
        if amount < 0:
            continue  # negative amount is a mistake -> drop the row
        # If this order_id was seen before, this later row replaces it,
        # so a duplicate is kept only once, at its last value.
        by_id[order_id] = {
            "order_id": order_id,
            "customer": (row.get("customer") or "").strip(),
            "product": (row.get("product") or "").strip(),
            "amount": amount,
        }
    return list(by_id.values())


def total_sales(clean_rows):
    """Add up the amounts of all clean orders."""
    return round(sum(r["amount"] for r in clean_rows), 2)


def main():
    rows = load_orders()
    clean = clean_orders(rows)
    print(f"Raw orders: {len(rows)}")
    print(f"Clean orders: {len(clean)}")
    print(f"Total sales: {total_sales(clean):.2f}")


if __name__ == "__main__":
    main()
