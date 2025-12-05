import os
import pandas as pd
import sqlite3
import glob

# --- CONFIGURATION ---
# Use environment variable or relative path for portability
CSV_FOLDER_PATH = os.environ.get('CSV_FOLDER_PATH', './CSV_DATASET')
DB_FILE_PATH = 'cars.db'  # This will be the name of your new, clean database

def create_car_database():
    """Reads all car CSVs, adds a 'brand' column, combines them, and saves to SQLite."""
    
    csv_files = glob.glob(os.path.join(CSV_FOLDER_PATH, '*.csv'))
    if not csv_files:
        print(f"Error: No CSV files found in '{CSV_FOLDER_PATH}'. Please check the path.")
        return

    print(f"Found {len(csv_files)} total files. Processing...")
    
    all_cars_dfs = []

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        
        # Skip any files with 'unclean' in the name
        if 'unclean' in filename:
            print(f"  - Skipping unclean file: {filename}")
            continue

        # --- THIS IS THE CRITICAL PART THAT FIXES THE TABLE NAME ---
        # It gets a clean brand name from the filename (e.g., 'audi.csv' -> 'audi')
        brand = filename.replace('.csv', '')
        print(f"  - Processing {filename} for brand: '{brand}'")
        
        try:
            df = pd.read_csv(file_path)
            # Add the new 'brand' column to the data
            df['brand'] = brand
            all_cars_dfs.append(df)
        except Exception as e:
            print(f"    -> Error reading {filename}: {e}")

    if not all_cars_dfs:
        print("No valid dataframes to combine. Exiting.")
        return

    print("\nCombining all data into a single 'cars' table...")
    # Combine all data into one big dataframe
    combined_df = pd.concat(all_cars_dfs, ignore_index=True)

    # Standardize column names (lowercase, no spaces) for easier querying
    combined_df.columns = combined_df.columns.str.strip().str.lower().str.replace(' ', '_')

    print(f"Saving combined data to '{DB_FILE_PATH}'...")
    conn = sqlite3.connect(DB_FILE_PATH)
    # Save everything to a SINGLE, clean table named 'cars'
    combined_df.to_sql('cars', conn, if_exists='replace', index=False)
    conn.close()

    print("\n✓ Database 'cars.db' created successfully!")
    print(f"Total cars in database: {len(combined_df)}")


if __name__ == '__main__':
    create_car_database()