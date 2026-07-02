# Smart Shopper Backend

This is the backend for Smart Shopper, a crowdsourced grocery pricing platform that recommends the cheapest shopping strategy based on store prices.

---

## 🚀 Goal

Build an API that:
- Stores grocery prices from multiple stores
- Accepts a user grocery list
- Calculates the cheapest way to shop across stores
- Returns optimized shopping plans

---

## 🧠 Core Idea

Instead of shopping at one store, Smart Shopper finds the cheapest combination of stores for your entire grocery list.

---

## 🏗️ Tech Stack

- Python
- Flask
- SQLite
- Flask-SQLAlchemy

---

## 📁 Project Structure

- `app/` → Core backend logic
- `models.py` → Database structure
- `routes.py` → API endpoints
- `services/optimizer.py` → Price optimization algorithm
- `db.py` → Database setup
- `data/seed_data.py` → Fake test data
- `run.py` → Starts server

---

## 📊 Database Overview

- Stores → grocery stores
- Products → items you can buy
- Prices → price of each product at each store

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
python run.py
```

---

## 📌 MVP Features

- Store price data
- Accept grocery list
- Return cheapest shopping plan
```