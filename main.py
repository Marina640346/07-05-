import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

cursor.execute("""
INSERT INTO products (name, category, price)
VALUES
('iPhone 15', 'смартфони', 42000),
('Samsung Galaxy S24', 'смартфони', 38000),
('Lenovo Legion 5', 'ноутбуки', 52000),
('MacBook Air M3', 'ноутбуки', 61000),
('iPad Air', 'планшети', 32000),
('Samsung Tab S9', 'планшети', 29000)
""")

cursor.execute("""
INSERT INTO customers (first_name, last_name, email)
VALUES
('Іван', 'Петренко', 'ivan@gmail.com'),
('Олена', 'Коваль', 'olena@gmail.com'),
('Максим', 'Шевченко', 'maksym@gmail.com')
""")

cursor.execute("""
INSERT INTO orders (customer_id, product_id, quantity, order_date)
VALUES
(1, 1, 1, '2026-05-07'),
(2, 3, 1, '2026-05-07'),
(3, 5, 2, '2026-05-07'),
(1, 2, 1, '2026-05-08')
""")

while True:
    print("\n1 - Показати товари")
    print("2 - Показати клієнтів")
    print("3 - Показати замовлення")
    print("4 - Сумарний обсяг продажів")
    print("5 - Кількість замовлень на кожного клієнта")
    print("6 - Середній чек")
    print("7 - Найбільш популярна категорія")
    print("8 - Кількість товарів кожної категорії")
    print("9 - Підвищити ціни смартфонів на 10%")
    print("0 - Вихід")

    choice = input("Ваш вибір: ")

    if choice == "1":
        cursor.execute("SELECT * FROM products")

        for row in cursor.fetchall():
            print(row)

    elif choice == "2":
        cursor.execute("SELECT * FROM customers")

        for row in cursor.fetchall():
            print(row)

    elif choice == "3":
        cursor.execute("SELECT * FROM orders")

        for row in cursor.fetchall():
            print(row)

    elif choice == "4":
        cursor.execute("""
        SELECT SUM(products.price * orders.quantity)
        FROM orders
        INNER JOIN products
        ON orders.product_id = products.product_id
        """)

        print("Сума продажів:", cursor.fetchone()[0])

    elif choice == "5":
        cursor.execute("""
        SELECT customers.first_name,
               customers.last_name,
               COUNT(orders.order_id)
        FROM customers
        INNER JOIN orders
        ON customers.customer_id = orders.customer_id
        GROUP BY customers.customer_id
        """)

        for row in cursor.fetchall():
            print(row)

    elif choice == "6":
        cursor.execute("""
        SELECT AVG(products.price * orders.quantity)
        FROM orders
        INNER JOIN products
        ON orders.product_id = products.product_id
        """)

        print("Середній чек:", cursor.fetchone()[0])

    elif choice == "7":
        cursor.execute("""
        SELECT products.category,
               COUNT(orders.order_id) AS total_orders
        FROM orders
        INNER JOIN products
        ON orders.product_id = products.product_id
        GROUP BY products.category
        ORDER BY total_orders DESC
        LIMIT 1
        """)

        print(cursor.fetchone())

    elif choice == "8":
        cursor.execute("""
        SELECT category,
               COUNT(*)
        FROM products
        GROUP BY category
        """)

        for row in cursor.fetchall():
            print(row)

    elif choice == "9":
        cursor.execute("""
        UPDATE products
        SET price = price * 1.10
        WHERE category = 'смартфони'
        """)
        print("Ціни смартфонів оновлено")

    elif choice == "0":
        save = input("Зберегти зміни? (так/ні): ")

        if save.lower() == "так":
            conn.commit()
            print("Зміни збережено")
        else:
            conn.rollback()1

            print("Зміни скасовано")

        break

conn.close()
