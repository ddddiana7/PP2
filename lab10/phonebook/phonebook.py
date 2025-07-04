import psycopg2
from config import config
import csv

def create_tables():
    """Create phonebook table"""
    commands = (
        """
          CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100)
        )
        )
        """,
        """
        CREATE OR REPLACE FUNCTION insert_or_update_user(
            p_first_name VARCHAR,
            p_phone VARCHAR
        ) RETURNS VOID AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
                UPDATE phonebook SET first_name = p_first_name WHERE phone = p_phone;
            ELSE
                INSERT INTO phonebook (first_name, phone) VALUES (p_first_name, p_phone);
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
        print("Table and function created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_from_console():
    """Insert data from user input with all fields"""
    print("\n--- Add New Contact ---")
    first_name = input("First name: ").strip()
    last_name = input("Last name (optional): ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email (optional): ").strip()
    
    sql = """INSERT INTO phonebook(first_name, last_name, phone, email)
             VALUES(%s, %s, %s, %s)"""
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.callproc("insert_or_update_user", (first_name, phone))
            conn.commit()
        print("✅ Contact added/updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def insert_from_csv(filename):
    """Insert data from CSV file with all fields"""
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header row if exists
                    for row in reader:
                        if len(row) >= 4:  # Проверяем, что есть все поля
                            cur.execute(
                                """INSERT INTO phonebook(first_name, last_name, phone, email)
                                VALUES(%s, %s, %s, %s)""",
                                (row[0], row[1], row[2], row[3])
                            )
            conn.commit()
        print(f"✅ Data from '{filename}' imported successfully!")
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Database error: {error}")

def update_contact():
    """Update contact's first name or phone"""
    print("\n--- Update Contact ---")
    old_phone = input("Enter current phone number: ").strip()
    
    print("\nWhat to update?")
    print("1. First name")
    print("2. Phone number")
    choice = input("Your choice (1-2): ").strip()
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    new_name = input("New first name: ").strip()
                    cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s", 
                               (new_name, old_phone))
                elif choice == '2':
                    new_phone = input("New phone number: ").strip()
                    cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", 
                               (new_phone, old_phone))
                else:
                    print("❌ Invalid choice")
                    return
                
                if cur.rowcount == 0:
                    print("❌ No contact found with that phone number")
                else:
                    conn.commit()
                    print("✅ Contact updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def search_contacts():
    """Search contacts with filters"""
    print("\n--- Search Contacts ---")
    print("1. By first name")
    print("2. By phone number")
    print("3. Show all contacts")
    choice = input("Your choice (1-3): ").strip()
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    name = input("Enter first name: ").strip()
                    cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
                elif choice == '2':
                    phone = input("Enter phone number: ").strip()
                    cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
                elif choice == '3':
                    cur.execute("SELECT * FROM phonebook ORDER BY first_name")
                else:
                    print("❌ Invalid choice")
                    return
                
                results = cur.fetchall()
                if not results:
                    print("🔍 No contacts found")
                else:
                    print("\n--- Contacts ---")
                    for row in results:
                        #проверяем количество полей в результате
                        if len(row) == 4:  #если 4 поля (id, first_name, phone, email)
                            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}")
                        elif len(row) >= 5:  #если 5+ полей (с фамилией)
                            print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Email: {row[4]}")
                        else:  # минимальный вывод
                            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def delete_contact():
    """Delete contact by phone or name"""
    print("\n--- Delete Contact ---")
    print("Delete by:")
    print("1. First name")
    print("2. Phone number")
    choice = input("Your choice (1-2): ").strip()
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    name = input("Enter first name: ").strip()
                    cur.execute("DELETE FROM phonebook WHERE first_name = %s RETURNING *", (name,))
                elif choice == '2':
                    phone = input("Enter phone number: ").strip()
                    cur.execute("DELETE FROM phonebook WHERE phone = %s RETURNING *", (phone,))
                else:
                    print("❌ Invalid choice")
                    return
                
                deleted = cur.fetchone()
                if deleted:
                    conn.commit()
                    print(f"✅ Deleted contact: {deleted[1]} {deleted[2]}")
                else:
                    print("❌ No matching contact found")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

if __name__ == "__main__":
    create_tables()
    
    while True:
        print("\n📞 PhoneBook Menu:")
        print("1. Add contact (console)")
        print("2. Import contacts (CSV)")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Exit")
        
        choice = input("Your choice (1-6): ").strip()
        
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            filename = input("Enter CSV filename (e.g., contacts.csv): ").strip()
            insert_from_csv(filename)
        elif choice == '3':
            update_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")