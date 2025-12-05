import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
# Set this to the name of the database file you want to explore.
DB_FILE = 'cars.db' 

def list_tables(conn):
    """Lists all tables in the connected database."""
    print("\nTABLES IN THE DATABASE:")
    print("-" * 25)
    try:
        # Use a system query to get all table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        return tables
    except Exception as e:
        print(f"An error occurred while listing tables: {e}")
        return []

def view_table_schema(conn, table_name):
    """Displays the schema (columns and data types) for a given table."""
    print(f"\nSCHEMA FOR TABLE: '{table_name}'")
    print("-" * (25 + len(table_name)))
    try:
        # Using pandas is the easiest way to get a nicely formatted schema
        df = pd.read_sql_query(f"PRAGMA table_info({table_name});", conn)
        if df.empty:
            print("Table not found or has no columns.")
        else:
            print(df[['name', 'type', 'notnull']])
    except Exception as e:
        print(f"An error occurred: {e}. Is the table name correct?")

def view_table_rows(conn, table_name):
    """Displays the first N rows of a given table."""
    try:
        row_count_str = input("How many rows to display? (default is 5): ")
        limit = int(row_count_str) if row_count_str.isdigit() else 5

        print(f"\nFIRST {limit} ROWS OF TABLE: '{table_name}'")
        print("-" * (30 + len(table_name)))
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
        
        if df.empty:
            print("Table is empty or does not exist.")
        else:
            # Configure pandas to show all columns
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df)

    except Exception as e:
        print(f"An error occurred: {e}. Is the table name correct?")

def run_custom_query(conn):
    """Allows the user to run a custom SQL SELECT query."""
    print("\n--- RUN CUSTOM SQL QUERY ---")
    print("Enter your SELECT query below. Press Enter twice to execute.")
    print("Example: SELECT customer_state, COUNT(*) FROM customers GROUP BY customer_state;")
    
    query_lines = []
    while True:
        line = input("> ")
        if not line:
            break
        query_lines.append(line)
    
    query = " ".join(query_lines).strip()
    
    if not query:
        print("No query entered.")
        return

    print("\nExecuting query...")
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("Query executed successfully but returned no results.")
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df)
    except Exception as e:
        print(f"\n❌ QUERY FAILED: {e}")


def main():
    """Main function to run the interactive explorer."""
    
    if not os.path.exists(DB_FILE):
        print(f"❌ ERROR: Database file '{DB_FILE}' not found!")
        print("Please make sure the script is in the same directory as your database file.")
        return

    print(f"🐍 Welcome to the SQLite Database Explorer for '{DB_FILE}'!")
    
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        
        while True:
            print("\n--- MENU ---")
            print("1. List all tables")
            print("2. View table schema (columns)")
            print("3. View first N rows of a table")
            print("4. Run a custom SQL query")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                list_tables(conn)
            elif choice == '2':
                table_name = input("Enter table name to see schema: ")
                view_table_schema(conn, table_name)
            elif choice == '3':
                table_name = input("Enter table name to see rows: ")
                view_table_rows(conn, table_name)
            elif choice == '4':
                run_custom_query(conn)
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Make sure you have pandas installed:
    # pip install pandas
    main()