from app.services.prices import create_price
import random

products = [
    "Milk",
    "Eggs",
    "Bread",
    "Butter",
    "Cheddar Cheese",
    "Greek Yogurt",
    "Chicken Breast",
    "Ground Beef",
    "Bacon",
    "Turkey Slices",
    "Ham",
    "Rice",
    "Pasta",
    "Spaghetti Sauce",
    "Peanut Butter",
    "Grape Jelly",
    "Cereal",
    "Oatmeal",
    "Flour",
    "Sugar",
    "Salt",
    "Black Pepper",
    "Olive Oil",
    "Vegetable Oil",
    "Potatoes",
    "Onions",
    "Tomatoes",
    "Lettuce",
    "Carrots",
    "Broccoli",
    "Apples",
    "Bananas",
    "Grapes",
    "Oranges",
    "Strawberries",
    "Frozen Pizza",
    "Frozen Vegetables",
    "Orange Juice",
    "Apple Juice",
    "Coffee",
    "Tea Bags",
    "Soda (12-pack)",
    "Bottled Water",
    "Paper Towels",
    "Toilet Paper",
    "Dish Soap",
    "Laundry Detergent",
    "Trash Bags",
    "Toothpaste",
    "Shampoo"
]

stores = [
    "Walmart",
    "Aldi",
    "Publix"
]

items = []

for product in products:
    for store in stores:
        items.append(
            {
                "store_name": store,
                "product_name": product,
                "price": round(random.uniform(.50, 15), 2)
            }
        )


for item in items:
    create_price(
        item["store_name"],
        item["product_name"],
        item["price"]
    )

print("Database seeded successfully!")