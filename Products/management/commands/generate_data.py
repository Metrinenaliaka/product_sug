import sqlite3
import random
from faker import Faker
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Generate dummy data for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        # Step 1: Create tables
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS Categories (
            CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            CategoryName TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductType TEXT NOT NULL,
            CategoryID INTEGER NOT NULL,
            Attributes TEXT,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
        );

        CREATE TABLE IF NOT EXISTS UserInteractions (
            InteractionID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            InteractionType TEXT NOT NULL,
            InteractionCount INTEGER DEFAULT 1,
            InteractionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        );
        ''')
        print("Tables created successfully!")

        # Step 2: Insert data
        categories = ["Electronics", "Books", "Clothing", "Home Appliances"]
        for category in categories:
            cursor.execute("INSERT INTO Categories (CategoryName) VALUES (?)", (category,))
        
        print("Categories inserted successfully!")

        # Insert products
        categories_from_db = cursor.execute("SELECT * FROM Categories").fetchall()
        for _ in range(50):
            category = random.choice(categories_from_db)
            product_type = fake.word()
            attributes = fake.sentence(nb_words=10)
            cursor.execute("INSERT INTO Products (ProductType, CategoryID, Attributes) VALUES (?, ?, ?)",
                           (product_type, category[0], attributes))
        print("Products inserted successfully!")

        # Insert users
        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            cursor.execute("INSERT INTO Users (Username, Email) VALUES (?, ?)",\
                            (username, email))
        print("Users inserted successfully!")

        # Insert user interactions
        users_from_db = cursor.execute("SELECT * FROM Users").fetchall()
        products_from_db = cursor.execute("SELECT * FROM Products").fetchall()
        interaction_types = ["like", "dislike", "view", "purchase"]

        for _ in range(100):
            user = random.choice(users_from_db)
            product = random.choice(products_from_db)
            interaction_type = random.choice(interaction_types)
            interaction_count = random.randint(1, 10)
            cursor.execute(
                "INSERT INTO UserInteractions (UserID, ProductID,\
                    InteractionType, InteractionCount) VALUES (?, ?, ?, ?)",
                (user[0], product[0], interaction_type, interaction_count))
        print("User interactions inserted successfully!")

        conn.commit()
        conn.close()
        print("Database populated successfully!")
