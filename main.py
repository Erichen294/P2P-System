import sqlite3

# SQLite database file name
DB_FILE = "users.db"

# Function to create the users table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY,
                 password TEXT,
                 port INTEGER
                 )''')
    conn.commit()
    conn.close()

# Function to register a new user
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Fetch the last assigned port
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT MAX(port) FROM users")
    last_port = c.fetchone()[0]
    conn.close()

    if last_port is None:
        port = 65432  # Start from 65432 if no user exists yet
    else:
        port = last_port + 1  # Increment by one for each new user

    # Insert the new user along with their assigned port
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, port) VALUES (?, ?, ?)", (username, password, port))
    conn.commit()
    conn.close()
    
    print("Registration successful!")

# Function to log in an existing user
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def main():
    create_users_table()
    
    while True:
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
