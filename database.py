import sqlite3


DATABASE_NAME = "cafe.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =====================================================
    # MENU
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    # =====================================================
    # ORDERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_type TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # =====================================================
    # ORDER ITEMS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (menu_id) REFERENCES menu(id)
        )
    """)

    # =====================================================
    # CAFE TABLES
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cafe_tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER UNIQUE NOT NULL,
            seats INTEGER NOT NULL,
            status TEXT DEFAULT 'Available'
        )
    """)

    # =====================================================
    # RESERVATIONS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            table_id INTEGER NOT NULL,
            reservation_date TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            status TEXT DEFAULT 'Reserved',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (table_id) REFERENCES cafe_tables(id)
        )
    """)

    # =====================================================
    # INVENTORY
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            minimum_stock REAL DEFAULT 5
        )
    """)

    # =====================================================
    # FEEDBACK
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # =====================================================
    # DEFAULT DATA
    # =====================================================

    create_default_users(cursor)
    create_default_tables(cursor)
    create_default_menu(cursor)

    connection.commit()
    connection.close()


# =========================================================
# DEFAULT USERS
# =========================================================

def create_default_users(cursor):

    users = [
        (
            "Cafe Admin",
            "admin@brewbytes.com",
            "admin123",
            "Admin"
        ),
        (
            "Demo Customer",
            "customer@gmail.com",
            "customer123",
            "Customer"
        )
    ]

    for user in users:

        cursor.execute("""
            SELECT id
            FROM users
            WHERE email = ?
        """, (user[1],))

        existing_user = cursor.fetchone()

        if existing_user is None:

            cursor.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role
                )
                VALUES (?, ?, ?, ?)
            """, user)


# =========================================================
# DEFAULT TABLES
# =========================================================

def create_default_tables(cursor):

    for table_number in range(1, 11):

        cursor.execute("""
            SELECT id
            FROM cafe_tables
            WHERE table_number = ?
        """, (table_number,))

        existing_table = cursor.fetchone()

        if existing_table is None:

            cursor.execute("""
                INSERT INTO cafe_tables
                (
                    table_number,
                    seats,
                    status
                )
                VALUES (?, ?, ?)
            """, (
                table_number,
                4,
                "Available"
            ))


# =========================================================
# DEFAULT MENU
# =========================================================

def create_default_menu(cursor):

    menu_items = [

        # COFFEE
        (
            "Cappuccino",
            "Coffee",
            160,
            "Rich espresso with steamed milk",
            "☕"
        ),
        (
            "Cold Coffee",
            "Coffee",
            140,
            "Creamy chilled coffee",
            "🥤"
        ),
        (
            "Espresso",
            "Coffee",
            120,
            "Strong and classic espresso",
            "☕"
        ),
        (
            "Café Latte",
            "Coffee",
            150,
            "Smooth espresso with creamy milk",
            "☕"
        ),

        # PIZZA
        (
            "Margherita Pizza",
            "Pizza",
            280,
            "Classic cheese pizza",
            "🍕"
        ),
        (
            "Veggie Pizza",
            "Pizza",
            320,
            "Fresh vegetables and cheese",
            "🍕"
        ),

        # BURGERS
        (
            "Classic Burger",
            "Burgers",
            220,
            "Crispy burger served with fries",
            "🍔"
        ),
        (
            "Veg Burger",
            "Burgers",
            190,
            "Crispy vegetable patty burger",
            "🍔"
        ),

        # DESSERTS
        (
            "Chocolate Cake",
            "Desserts",
            180,
            "Soft chocolate cake",
            "🍰"
        ),
        (
            "Brownie",
            "Desserts",
            150,
            "Warm chocolate brownie",
            "🍫"
        ),

        # BEVERAGES
        (
            "Fresh Lime Soda",
            "Beverages",
            100,
            "Refreshing lime soda",
            "🥤"
        ),
        (
            "Mango Shake",
            "Beverages",
            160,
            "Creamy mango shake",
            "🥭"
        )
    ]

    for item in menu_items:

        cursor.execute("""
            SELECT id
            FROM menu
            WHERE name = ?
        """, (item[0],))

        existing_item = cursor.fetchone()

        if existing_item is None:

            cursor.execute("""
                INSERT INTO menu
                (
                    name,
                    category,
                    price,
                    description,
                    image,
                    available
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                1
            ))


# =========================================================
# AUTHENTICATE USER
# =========================================================

def authenticate_user(email, password, role):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role
        FROM users
        WHERE email = ?
        AND password = ?
        AND role = ?
    """, (
        email,
        password,
        role
    ))

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# GET USER BY ID
# =========================================================

def get_user_by_id(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# GET MENU ITEMS - CUSTOMER
# =========================================================

def get_menu_items():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            price,
            description,
            image,
            available
        FROM menu
        WHERE available = 1
        ORDER BY category, name
    """)

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# GET ALL MENU ITEMS - ADMIN
# =========================================================

def get_all_menu_items():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            price,
            description,
            image,
            available
        FROM menu
        ORDER BY category, name
    """)

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# GET MENU BY CATEGORY
# =========================================================

def get_menu_by_category(category):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            price,
            description,
            image,
            available
        FROM menu
        WHERE category = ?
        AND available = 1
        ORDER BY name
    """, (category,))

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# GET SINGLE MENU ITEM
# =========================================================

def get_menu_item(menu_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            price,
            description,
            image,
            available
        FROM menu
        WHERE id = ?
    """, (menu_id,))

    item = cursor.fetchone()

    connection.close()

    return item


# =========================================================
# ADD MENU ITEM
# =========================================================

def add_menu_item(
    name,
    category,
    price,
    description="",
    image="☕",
    available=1
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO menu
        (
            name,
            category,
            price,
            description,
            image,
            available
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        category,
        price,
        description,
        image,
        available
    ))

    connection.commit()

    menu_id = cursor.lastrowid

    connection.close()

    return menu_id


# =========================================================
# UPDATE MENU ITEM
# =========================================================

def update_menu_item(
    menu_id,
    name,
    category,
    price,
    description="",
    image="☕",
    available=1
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE menu
        SET
            name = ?,
            category = ?,
            price = ?,
            description = ?,
            image = ?,
            available = ?
        WHERE id = ?
    """, (
        name,
        category,
        price,
        description,
        image,
        available,
        menu_id
    ))

    connection.commit()

    connection.close()


# =========================================================
# DELETE MENU ITEM
# =========================================================

def delete_menu_item(menu_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM menu
        WHERE id = ?
    """, (menu_id,))

    connection.commit()

    connection.close()


# =========================================================
# CREATE ORDER
# =========================================================

def create_order(
    user_id,
    order_type,
    cart_items,
    total
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO orders
        (
            user_id,
            order_type,
            total,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        order_type,
        total,
        "Pending"
    ))

    order_id = cursor.lastrowid

    for menu_id, quantity, price in cart_items:

        cursor.execute("""
            INSERT INTO order_items
            (
                order_id,
                menu_id,
                quantity,
                price
            )
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            menu_id,
            quantity,
            price
        ))

    connection.commit()
    connection.close()

    return order_id


# =========================================================
# GET ORDER
# =========================================================

def get_order(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            order_type,
            total,
            status,
            created_at
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    return order


# =========================================================
# GET ALL ORDERS
# =========================================================

def get_all_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            order_type,
            total,
            status,
            created_at
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    connection.close()

    return orders


# =========================================================
# GET CUSTOMER ORDERS
# =========================================================

def get_customer_orders(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            order_type,
            total,
            status,
            created_at
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    orders = cursor.fetchall()

    connection.close()

    return orders


# =========================================================
# GET ORDER ITEMS
# =========================================================

def get_order_items(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            order_items.id,
            menu.name,
            order_items.quantity,
            order_items.price
        FROM order_items
        JOIN menu
        ON order_items.menu_id = menu.id
        WHERE order_items.order_id = ?
    """, (order_id,))

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

def update_order_status(
    order_id,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (
        status,
        order_id
    ))

    connection.commit()

    connection.close()


# =========================================================
# GET AVAILABLE TABLES
# =========================================================

def get_available_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            table_number,
            seats,
            status
        FROM cafe_tables
        WHERE status = 'Available'
        ORDER BY table_number
    """)

    tables = cursor.fetchall()

    connection.close()

    return tables


# =========================================================
# UPDATE TABLE STATUS
# =========================================================

def update_table_status(
    table_id,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE cafe_tables
        SET status = ?
        WHERE id = ?
    """, (
        status,
        table_id
    ))

    connection.commit()

    connection.close()


# =========================================================
# CREATE RESERVATION
# =========================================================

def create_reservation(
    user_id,
    table_id,
    reservation_date,
    reservation_time,
    guests
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reservations
        (
            user_id,
            table_id,
            reservation_date,
            reservation_time,
            guests,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        table_id,
        reservation_date,
        reservation_time,
        guests,
        "Reserved"
    ))

    reservation_id = cursor.lastrowid

    cursor.execute("""
        UPDATE cafe_tables
        SET status = 'Reserved'
        WHERE id = ?
    """, (table_id,))

    connection.commit()
    connection.close()

    return reservation_id


# =========================================================
# GET INVENTORY
# =========================================================

def get_inventory():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            item_name,
            category,
            quantity,
            unit,
            minimum_stock
        FROM inventory
        ORDER BY item_name
    """)

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# ADD INVENTORY ITEM
# =========================================================

def add_inventory_item(
    item_name,
    category,
    quantity,
    unit,
    minimum_stock
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory
        (
            item_name,
            category,
            quantity,
            unit,
            minimum_stock
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        item_name,
        category,
        quantity,
        unit,
        minimum_stock
    ))

    connection.commit()

    connection.close()


# =========================================================
# ADD FEEDBACK
# =========================================================

def add_feedback(
    user_id,
    rating,
    message
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (
            user_id,
            rating,
            message
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        rating,
        message
    ))

    connection.commit()

    connection.close()


# =========================================================
# GET FEEDBACK
# =========================================================

def get_all_feedback():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            feedback.id,
            users.name,
            feedback.rating,
            feedback.message,
            feedback.created_at
        FROM feedback
        JOIN users
        ON feedback.user_id = users.id
        ORDER BY feedback.id DESC
    """)

    feedback = cursor.fetchall()

    connection.close()

    return feedback


# =========================================================
# START DATABASE
# =========================================================

if __name__ == "__main__":

    initialize_database()

    print("-----------------------------------")
    print("     BREW & BYTES CAFÉ")
    print("-----------------------------------")
    print("Database initialized successfully!")
    print("Users       : Ready")
    print("Menu        : Ready")
    print("Orders      : Ready")
    print("Tables      : Ready")
    print("Inventory   : Ready")
    print("Feedback    : Ready")
    print("-----------------------------------")