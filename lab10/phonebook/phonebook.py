import psycopg2
from config import config
import csv

# ORIGINAL FUNCTIONS (1-5) - UNCHANGED
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
        """,
        """

        #проверяет есть ли в таблице запись с телефоном, если есть - обновляет имя для телефона, если нет - вставляет новую запись
        CREATE OR REPLACE FUNCTION insert_or_update_user(
            p_first_name VARCHAR,
            p_phone VARCHAR
        ) RETURNS VOID AS $$ #обрамление текста
        BEGIN
            IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
                UPDATE phonebook SET first_name = p_first_name WHERE phone = p_phone;
            ELSE
                INSERT INTO phonebook (first_name, phone) VALUES (p_first_name, p_phone);
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """,
        """
        CREATE OR REPLACE FUNCTION insert_many_users(
            users TEXT[][]
        ) RETURNS TEXT[] AS $$
        DECLARE
            incorrect_data TEXT[];
            user_record TEXT[];
            phone_text TEXT;
            i INT := 1; #это объявление и инициализация переменной-счётчика
        BEGIN
            incorrect_data := '{}';
            
            FOREACH user_record SLICE 1 IN ARRAY users
            LOOP
                IF array_length(user_record, 1) < 2 THEN
                    incorrect_data := array_append(incorrect_data, 
                        format('User %s: Missing name or phone', i));
                ELSE
                    phone_text := user_record[2];
                    
                    -- Simple phone validation (just digits, at least 5 characters)
                    IF phone_text ~ '^[0-9]{5,}$' THEN
                        PERFORM insert_or_update_user(user_record[1], phone_text);
                    ELSE
                        incorrect_data := array_append(incorrect_data, 
                            format('User %s: %s - Invalid phone format', i, phone_text));
                    END IF;
                END IF;
                i := i + 1;
            END LOOP;
            
            RETURN incorrect_data;
        END;
        $$ LANGUAGE plpgsql;
        """,
        """
        CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(
            search_term VARCHAR
        ) AS $$
        BEGIN
            DELETE FROM phonebook 
            WHERE first_name = search_term OR phone = search_term;
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
        print("Table and functions/procedures created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_from_console():
    """Insert data from user input"""
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
                cur.execute(sql, (first_name, last_name, phone, email))
            conn.commit()
        print("✅ Contact added successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def insert_from_csv(filename):
    """Insert data from CSV file (format: first_name,last_name,phone,email)"""
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header row if exists
                    for row in reader:
                        cur.execute(
                            """INSERT INTO phonebook(first_name, last_name, phone, email)
                            VALUES(%s, %s, %s, %s)""",
                            row
                        )
            conn.commit()
        print(f"✅ Data from '{filename}' imported successfully!")
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Database error: {error}")

def update_contact():#обновление контакта
    """Update contact's first name or phone"""
    print("\n--- Update Contact ---")
    phone = input("Enter the phone number of the contact to update: ").strip()
    
    print("\nWhat to update?")
    print("1. First name")
    print("2. Phone number")
    choice = input("Your choice (1-2): ").strip()
    
    if choice == '1':
        new_name = input("New first name: ").strip()
        sql = "UPDATE phonebook SET first_name = %s WHERE phone = %s"
        params = (new_name, phone)
    elif choice == '2':
        new_phone = input("New phone number: ").strip()
        sql = "UPDATE phonebook SET phone = %s WHERE phone = %s"
        params = (new_phone, phone)
    else:
        print("❌ Invalid choice")
        return
    
    try:
        params_config = config()
        with psycopg2.connect(**params_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if cur.rowcount == 0:
                    print("❌ No contact found with that phone number")
                else:
                    conn.commit()
                    print("✅ Contact updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def search_contacts():#гибкий поиск
    """Search contacts with filters"""
    print("\n--- Search Contacts ---")
    print("1. By first name")
    print("2. By phone number")
    print("3. Show all contacts")
    choice = input("Your choice (1-3): ").strip()
    
    try:
        params = config()#словарь с параметрами подключения к базе данных, которая возвращается функцией config
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                if choice == '1': #by name
                    name = input("Enter first name: ").strip()
                    cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
                elif choice == '2':#by phone number
                    phone = input("Enter phone number: ").strip()
                    cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
                elif choice == '3':#all contacts
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
                        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Email: {row[4]}")
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

# --------------------------
# NEW FUNCTIONS (6-10) - ADDED WITHOUT MODIFYING ORIGINAL
# --------------------------
def search_by_pattern(pattern):
    """Search contacts by pattern (name, surname, phone)"""
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                query = """
                SELECT * FROM phonebook 
                WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone LIKE %s
                ORDER BY first_name
                """
                search_pattern = f"%{pattern}%"
                cur.execute(query, (search_pattern, search_pattern, search_pattern))
                
                results = cur.fetchall()
                if not results:
                    print("🔍 No contacts found matching the pattern")
                else:
                    print(f"\n--- Contacts matching '{pattern}' ---")
                    for row in results:
                        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Email: {row[4]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def insert_or_update_user(): #обновляет имя при совпадении телефона
    """Insert or update user using stored procedure"""
    print("\n--- Insert/Update User ---")
    first_name = input("First name: ").strip()
    phone = input("Phone number: ").strip()
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.callproc("insert_or_update_user", (first_name, phone))
            conn.commit()
        print("✅ User added/updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def insert_many_users():#пакетно добавление с валидацией
    """Insert many users using stored procedure"""
    print("\n--- Insert Many Users ---")
    print("Enter users in format 'name,phone'. One per line. Enter 'done' when finished.")
    
    users = []
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'done':
            break
        users.append(user_input.split(','))
    
    if not users:
        print("❌ No users provided")
        return
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Convert to 2D array for PostgreSQL
                users_array = [[u[0], u[1]] for u in users]
                cur.execute("SELECT insert_many_users(%s)", (users_array,))
                incorrect_data = cur.fetchone()[0]
                
                if incorrect_data:
                    print("\n❌ Incorrect data:")
                    for item in incorrect_data:
                        print(f"- {item}")
                else:
                    print("✅ All users processed successfully!")
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def get_paginated_records():
    """Get records with pagination"""
    print("\n--- Paginated Records ---")
    limit = input("Number of records per page: ").strip()
    offset = input("Offset (start from record): ").strip()
    
    try:
        limit = int(limit)
        offset = int(offset)
    except ValueError:
        print("❌ Please enter valid numbers")
        return
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY first_name LIMIT %s OFFSET %s", (limit, offset))
                results = cur.fetchall()
                
                if not results:
                    print("🔍 No contacts found in this range")
                else:
                    print(f"\n--- Contacts (showing {len(results)} records) ---")
                    for row in results:
                        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Email: {row[4]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

def delete_by_username_or_phone():#удаляет по имени/телефону
    """Delete by username or phone using stored procedure"""
    print("\n--- Delete by Username or Phone ---")
    search_term = input("Enter username or phone to delete: ").strip()
    
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Call the stored procedure
                cur.execute("CALL delete_by_username_or_phone(%s)", (search_term,))
                conn.commit()
                
                # Check if any rows were affected
                if cur.rowcount > 0:
                    print(f"✅ Deleted {cur.rowcount} contact(s)")
                else:
                    print("❌ No matching contact found")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")

#MAIN MENU (Extended with new options)
if __name__ == "__main__":
    create_tables()  #Ensure table exists
    
    while True:
        print("\n📞 PhoneBook Menu:")
        print("1. Add contact (console)")
        print("2. Import contacts (CSV)")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Search by pattern (name/phone)")
        print("7. Insert/update user (stored procedure)")
        print("8. Insert many users (with validation)")
        print("9. Get paginated records")
        print("10. Delete by username/phone (procedure)")
        print("11. Exit")
        
        choice = input("Your choice (1-11): ").strip()
        
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
            pattern = input("Enter search pattern: ").strip()
            search_by_pattern(pattern)
        elif choice == '7':
            insert_or_update_user()
        elif choice == '8':
            insert_many_users()
        elif choice == '9':
            get_paginated_records()
        elif choice == '10':
            delete_by_username_or_phone()
        elif choice == '11':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")