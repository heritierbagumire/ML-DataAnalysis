import psycopg2
from faker import Faker
from datetime import datetime
import random

# Establish a database connection
connection = psycopg2.connect(
    host="localhost",        # Replace with your host
    database="prismaDB",     # Replace with your database name
    user="postgres",         # Replace with your username
    password="Fomula123!" # Replace with your password
)
cursor = connection.cursor()

# Initialize Faker for generating mock data
fake = Faker()

# Function to batch-insert data into Users
def insert_users(batch_size, total_rows):
    print("Inserting users...")
    existing_usernames = set()  # To track already inserted usernames
    for _ in range(0, total_rows, batch_size):
        users = []
        while len(users) < batch_size:
            username = fake.user_name()
            # Ensure the username is unique
            if username not in existing_usernames:
                users.append(
                    (
                        fake.uuid4(),
                        username,
                        fake.password(),
                        random.choice(["ADMIN", "GENERAL_USER", "SURVIVOR"]),
                        datetime.now(),
                        datetime.now(),
                    )
                )
                existing_usernames.add(username)  # Track the username
        cursor.executemany(
            """
            INSERT INTO "User" (id, username, password, role, "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            , users
        )
        connection.commit()
        print(f"Inserted {_ + batch_size}/{total_rows} users")

# Function to batch-insert data into EducationalContent
def insert_educational_content(batch_size, total_rows):
    print("Inserting educational content...")
    for _ in range(0, total_rows, batch_size):
        educational_content = [
            (
                fake.uuid4(),
                fake.sentence(nb_words=6),
                fake.paragraph(nb_sentences=3),
                "ARTICLE",
                fake.url(),
                datetime.now(),
                datetime.now(),
            )
            for _ in range(batch_size)
        ]
        cursor.executemany(
            """
            INSERT INTO "EducationalContent" (id, title, description, "contentType", "contentUrl", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            , educational_content
        )
        connection.commit()
        print(f"Inserted {_ + batch_size}/{total_rows} educational content rows")

# Insert data
try:
    insert_users(batch_size=1000, total_rows=500000)
    insert_educational_content(batch_size=1000, total_rows=500000)
    print("Data insertion complete!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    connection.close()
