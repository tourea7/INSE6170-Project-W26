import sqlite3
import os

#roote to database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data' , 'devices.db')

def get_connection(): 
    """Establishes a connection to the SQLITE database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """creates the tables if they doesn't exits."""
    conn = get_connection()
    cursor = conn.cursor()
    
    #Devices connected table ( Function 1)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS devices (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       ip TEXT,
                       mac TEXT UNIQUE,
                       vendor TEXT,
                       name TEXT,
                       model TEXT,
                       description TEXT,
                       first_seen TEXT,
                       last_seen TEXT
                       
                      )  
                   ''')
    # Firewall rules table ( Function 3)
    cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS firewall_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_mac TEXT,
                    allowed_ip TEXT,
                    allowed_port INTEGER,
                    protocol TEXT,
                    description TEXT
                    
                )   
                   ''')
    
    # debits table
    cursor.execute(''' 
                   CREATE TABLE IF NOT EXISTS bandwidth_history(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       device_mac TEXT,
                       timestamp TEXT,
                       data_rate REAL
                   )
                   ''')
    
    # PCAP files table
    cursor.execute(''' 
                   CREATE TABLE IF NOT EXISTS pcap_files(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       device_mac TEXT,
                       filename TEXT,
                       filepath TEXT,
                       created_at TEXT,
                       size INTEGER
                       
                   )
                   ''')
    # Alerts table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_ip TEXT,
            device_mac TEXT,
            timestamp TEXT,
            data_rate REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
    
 # Function to delete old records from the bandwidth_history table (Function 4)   
def delete_old_records(days=30):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM bandwidth_history 
        WHERE timestamp < datetime('now', ?)
    """, (f'-{days} days',))
    conn.commit()
    conn.close()
    print(f"Old records deleted (older than {days} days)")  
    
      
if __name__ == "__main__":
     init_db()  
     
     