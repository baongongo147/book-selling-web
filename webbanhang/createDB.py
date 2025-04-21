import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# List of queries to create tables and define schema
queries = [
    """
    CREATE TABLE account_emailaddress (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email VARCHAR(254) NOT NULL,
      verified TINYINT(1) NOT NULL,
      primary_email TINYINT(1) NOT NULL,
      user_id INTEGER NOT NULL,
      UNIQUE (user_id, email),
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE account_emailconfirmation (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created DATETIME NOT NULL,
      sent DATETIME DEFAULT NULL,
      key VARCHAR(64) NOT NULL UNIQUE,
      email_address_id INTEGER NOT NULL,
      FOREIGN KEY (email_address_id) REFERENCES account_emailaddress (id)
    );
    """,
    """
    CREATE TABLE app_customer (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(200) DEFAULT NULL,
      email VARCHAR(200) DEFAULT NULL,
      user_id INTEGER DEFAULT NULL UNIQUE,
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE app_order (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date_order DATETIME NOT NULL,
      complete TINYINT(1) DEFAULT NULL,
      transaction_id VARCHAR(200) DEFAULT NULL,
      customer_id INTEGER DEFAULT NULL,
      FOREIGN KEY (customer_id) REFERENCES app_customer (id)
    );
    """,
    """
    CREATE TABLE app_orderitem (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      quantity INTEGER DEFAULT NULL,
      date_added DATETIME NOT NULL,
      order_id INTEGER DEFAULT NULL,
      product_id INTEGER DEFAULT NULL,
      FOREIGN KEY (order_id) REFERENCES app_order (id),
      FOREIGN KEY (product_id) REFERENCES app_product (id)
    );
    """,
    """
    CREATE TABLE app_product (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(200) DEFAULT NULL,
      price DOUBLE NOT NULL,
      digital TINYINT(1) DEFAULT NULL,
      image VARCHAR(100) DEFAULT NULL
    );
    """,
    """
    CREATE TABLE app_shippingaddress (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      address VARCHAR(200) DEFAULT NULL,
      city VARCHAR(200) DEFAULT NULL,
      state VARCHAR(200) DEFAULT NULL,
      mobile VARCHAR(10) DEFAULT NULL,
      date_added DATETIME NOT NULL,
      customer_id INTEGER DEFAULT NULL,
      order_id INTEGER DEFAULT NULL,
      FOREIGN KEY (customer_id) REFERENCES app_customer (id),
      FOREIGN KEY (order_id) REFERENCES app_order (id)
    );
    """,
    """
    CREATE TABLE auth_group (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(150) NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE auth_group_permissions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      group_id INTEGER NOT NULL,
      permission_id INTEGER NOT NULL,
      UNIQUE (group_id, permission_id),
      FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
      FOREIGN KEY (group_id) REFERENCES auth_group (id)
    );
    """,
    """
    CREATE TABLE auth_permission (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(255) NOT NULL,
      content_type_id INTEGER NOT NULL,
      codename VARCHAR(100) NOT NULL,
      UNIQUE (content_type_id, codename),
      FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
    );
    """,
    """
    CREATE TABLE auth_user (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      password VARCHAR(128) NOT NULL,
      last_login DATETIME DEFAULT NULL,
      is_superuser TINYINT(1) NOT NULL,
      username VARCHAR(150) NOT NULL UNIQUE,
      first_name VARCHAR(150) NOT NULL,
      last_name VARCHAR(150) NOT NULL,
      email VARCHAR(254) NOT NULL,
      is_staff TINYINT(1) NOT NULL,
      is_active TINYINT(1) NOT NULL,
      date_joined DATETIME NOT NULL
    );
    """,
    """
    CREATE TABLE auth_user_groups (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      group_id INTEGER NOT NULL,
      UNIQUE (user_id, group_id),
      FOREIGN KEY (group_id) REFERENCES auth_group (id),
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE auth_user_user_permissions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      permission_id INTEGER NOT NULL,
      UNIQUE (user_id, permission_id),
      FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE django_admin_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action_time DATETIME NOT NULL,
      object_id TEXT,
      object_repr VARCHAR(200) NOT NULL,
      action_flag INTEGER UNSIGNED NOT NULL CHECK (action_flag >= 0),
      change_message TEXT NOT NULL,
      content_type_id INTEGER DEFAULT NULL,
      user_id INTEGER NOT NULL,
      FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE django_content_type (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      app_label VARCHAR(100) NOT NULL,
      model VARCHAR(100) NOT NULL,
      UNIQUE (app_label, model)
    );
    """,
    """
    CREATE TABLE django_migrations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      app VARCHAR(255) NOT NULL,
      name VARCHAR(255) NOT NULL,
      applied DATETIME NOT NULL
    );
    """,
    """
    CREATE TABLE django_session (
      session_key VARCHAR(40) NOT NULL PRIMARY KEY,
      session_data TEXT NOT NULL,
      expire_date DATETIME NOT NULL
    );
    """,
    """
    CREATE TABLE socialaccount_socialaccount (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      provider VARCHAR(200) NOT NULL,
      uid VARCHAR(191) NOT NULL,
      last_login DATETIME NOT NULL,
      date_joined DATETIME NOT NULL,
      extra_data TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      UNIQUE (provider, uid),
      FOREIGN KEY (user_id) REFERENCES auth_user (id)
    );
    """,
    """
    CREATE TABLE socialaccount_socialapp (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      provider VARCHAR(30) NOT NULL,
      name VARCHAR(40) NOT NULL,
      client_id VARCHAR(191) NOT NULL,
      secret VARCHAR(191) NOT NULL,
      key VARCHAR(191) NOT NULL,
      provider_id VARCHAR(200) NOT NULL,
      settings TEXT NOT NULL DEFAULT '{}'
    );
    """,
    """
    CREATE TABLE socialaccount_socialtoken (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      token TEXT NOT NULL,
      token_secret TEXT NOT NULL,
      expires_at DATETIME DEFAULT NULL,
      account_id INTEGER NOT NULL,
      app_id INTEGER DEFAULT NULL,
      UNIQUE (app_id, account_id),
      FOREIGN KEY (account_id) REFERENCES socialaccount_socialaccount (id),
      FOREIGN KEY (app_id) REFERENCES socialaccount_socialapp (id)
    );
    """
]

# Execute each query to create the tables
for query in queries:
    cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("finish")