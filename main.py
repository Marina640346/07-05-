import sqlite3


def init_db(conn):
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL, 
        email TEXT NOT NULL UNIQUE 
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders ( 
        order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        customer_id INTEGER NOT NULL, 
        product_id INTEGER NOT NULL, 
        quantity INTEGER NOT NULL, 
        order_date DATE NOT NULL, 
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
        FOREIGN KEY (product_id) REFERENCES products(product_id) 
    )''')
    conn.commit()


def seed_data(conn):
    cursor = conn.cursor()

    products = [
        ('iPhone 15', 'Смартфони', 35000),
        ('Samsung Galaxy S23', 'Смартфони', 32000),
        ('MacBook Air M2', 'Ноутбуки', 45000),
        ('iPad Pro', 'Планшети', 30000),
        ('Asus ROG', 'Ноутбуки', 55000)
    ]
    cursor.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)


    customers = [
        ('Олексій', 'Петренко', 'oleksii@email.com'),
        ('Марія', 'Ковальчук', 'maria@email.com'),
        ('Іван', 'Сидоренко', 'ivan@email.com')
    ]
    cursor.executemany("INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)", customers)


    orders = [
        (1, 1, 1, '2026-05-01'),
        (2, 3, 1, '2026-05-02'),
        (1, 4, 2, '2026-05-03'),
        (3, 2, 1, '2026-05-04')
    ]
    cursor.executemany("INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", orders)
    conn.commit()
    print("Початкові дані успішно додано!")




def total_sales(cursor):
    query = """
    SELECT SUM(orders.quantity * products.price) 
    FROM orders 
    JOIN products ON orders.product_id = products.product_id
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print(f"\nЗагальний обсяг продажів: {result:.2f} грн")


def orders_per_customer(cursor):
    query = """
    SELECT c.first_name, c.last_name, COUNT(o.order_id)
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    """
    cursor.execute(query)
    print("\nКількість замовлень на кожного клієнта:")
    for row in cursor.fetchall():
        print(f"{row[0]} {row[1]}: {row[2]}")


def average_order_value(cursor):
    query = """
    SELECT AVG(total_price) FROM (
        SELECT SUM(o.quantity * p.price) as total_price
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY o.order_id
    )
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print(f"\nСередній чек замовлення: {result:.2f} грн")


def popular_category(cursor):
    query = """
    SELECT p.category, COUNT(o.order_id) as order_count
    FROM products p
    JOIN orders o ON p.product_id = o.product_id
    GROUP BY p.category
    ORDER BY order_count DESC
    LIMIT 1
    """
    cursor.execute(query)
    row = cursor.fetchone()
    print(f"\nНайбільш популярна категорія: {row[0]} ({row[1]} замовлень)")


def category_counts(cursor):
    query = "SELECT category, COUNT(*) FROM products GROUP BY category"
    cursor.execute(query)
    print("\nКількість товарів у кожній категорії:")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")


def update_smartphone_prices(cursor):
    query = "UPDATE products SET price = price * 1.10 WHERE category = 'Смартфони'"
    cursor.execute(query)
    print("\nЦіни на смартфони оновлено на +10%.")


def main():
    conn = sqlite3.connect(':memory:')  # Використовуємо в пам'яті для тесту, або 'shop.db' для файлу
    init_db(conn)
    cursor = conn.cursor()

    print("--- Ласкаво просимо до системи управління магазином ---")

    while True:
        print("\nОберіть дію:")
        print("1. Додати початкові дані (Seed)")
        print("2. Загальний обсяг продажів")
        print("3. Кількість замовлень на клієнта")
        print("4. Середній чек")
        print("5. Найпопулярніша категорія")
        print("6. Товарів у категоріях")
        print("7. Оновити ціни на смартфони (+10%)")
        print("8. Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            seed_data(conn)
        elif choice == '2':
            total_sales(cursor)
        elif choice == '3':
            orders_per_customer(cursor)
        elif choice == '4':
            average_order_value(cursor)
        elif choice == '5':
            popular_category(cursor)
        elif choice == '6':
            category_counts(cursor)
        elif choice == '7':
            update_smartphone_prices(cursor)
        elif choice == '8':
            save = input("Бажаєте зберегти зміни перед виходом? (y/n): ")
            if save.lower() == 'y':
                conn.commit()
                print("Зміни збережено.")
            break
        else:
            print("Невірний вибір.")

    conn.close()


if __name__ == "__main__":
    main()