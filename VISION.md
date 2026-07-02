# Mission

A crowdsourced grocery pricing platform that recommends
the cheapest shopping strategy based on local receipt data.

# MVP

- Submit receipts
- Store prices
- Create shopping lists
- Limit number of stores
- Recommend cheapest shopping plan

# Not MVP

- OCR receipt scanning
- Authentication
- AI product matching
- Price prediction
- Pantry tracking

# Plan
User Flow:
- User selects desired stores
- User enters grocery list
- App knows prices from multiple stores
- Algorithm finds the store where each item should come from that results in the cheapest total cost and sorts said data into a list
- User is shown:
  - Total cost
  - list of which store to buy what from to attain the cost, ie: Walmart: soap, paper, brush | Publix: Watermelon, cheese etc
  - Total Savings calculated from if they went to one store

Version 1 Scope:
- Manual price data generated from AI:
  - 3 stores
  - 20 products

- A grocery list input
- cheapest store recommendation

Database Design:
# Database Design

We will use a simple relational database. Think of it as 3 connected tables:

- Stores (where you shop)
- Products (what you buy)
- Prices (how much each store charges for each product)

This structure lets us compare prices across stores easily.

---

## Stores Table

This stores all grocery stores in the system.

| Field | Type | Description |
|------|------|-------------|
| id | integer | Unique ID for each store |
| name | text | Store name (Walmart, Aldi, Publix) |

Example:

| id | name |
|----|------|
| 1 | Walmart |
| 2 | Aldi |
| 3 | Publix |

---

## Products Table

This stores all grocery items users can add to a list.

| Field | Type | Description |
|------|------|-------------|
| id | integer | Unique ID for each product |
| name | text | Product name (Milk, Eggs, Bread) |

Example:

| id | name |
|----|------|
| 1 | Milk |
| 2 | Eggs |
| 3 | Bread |

---

## Prices Table

This is the most important table. It connects stores + products + price.

| Field | Type | Description |
|------|------|-------------|
| id | integer | Unique ID for each price entry |
| store_id | integer | Links to Stores table |
| product_id | integer | Links to Products table |
| price | float | Price of that product at that store |

Example:

| store_id | product_id | price |
|----------|------------|------|
| 1 (Walmart) | 1 (Milk) | 3.89 |
| 2 (Aldi) | 1 (Milk) | 3.69 |
| 3 (Publix) | 1 (Milk) | 4.49 |

---

## How the Data Connects

Instead of storing everything in one table, we connect them:

- Stores tell us WHERE
- Products tell us WHAT
- Prices tell us HOW MUCH

So when a user searches for "Milk", the app checks:
- Walmart price
- Aldi price
- Publix price

Then selects the cheapest option.

---

## Why This Design Works

This setup makes it easy to:
- Add new stores without changing structure
- Add new products anytime
- Compare prices instantly
- Scale later into crowdsourced receipts

---

## Future Upgrade (Not MVP)

Later we can expand Prices into:
- receipt_id (for crowdsourcing)
- date (for tracking price changes)
- quantity
- store location