import os
import mysql.connector
from mysql.connector import Error

def load_env():
    """Helper to manually parse the .env file."""
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars

def get_connection():
    """Connects to Aiven MySQL using SSL and .env configurations."""
    env = load_env()
    
    # Path to the downloaded Aiven CA certificate
    ca_path = os.path.abspath("ca.pem")
    
    if not os.path.exists(ca_path):
        print("⚠️ Warning: 'ca.pem' not found in your directory. Aiven connection might fail without SSL.")
    
    try:
        return mysql.connector.connect(
            host=env.get('DB_HOST'),
            user=env.get('DB_USER'),
            password=env.get('DB_PASSWORD'),
            database=env.get('DB_NAME', 'defaultdb'),
            port=int(env.get('DB_PORT', 3306)),
            ssl_ca=ca_path,
            ssl_disabled=False
        )
    except Error as e:
        print(f"❌ Error connecting to Aiven MySQL: {e}")
        return None

def setup_database():
    """Reads and executes schema.sql to initialize cloud tables."""
    env = load_env()
    ca_path = os.path.abspath("ca.pem")

    try:
        # Connect explicitly using the configuration pool parameters
        conn = mysql.connector.connect(
            host=env.get('DB_HOST'),
            user=env.get('DB_USER'),
            password=env.get('DB_PASSWORD'),
            port=int(env.get('DB_PORT', 3306)),
            ssl_ca=ca_path
        )
        cursor = conn.cursor()
        
        print("Reading schema.sql...")
        with open('schema.sql', 'r') as f:
            sql_script = f.read()
            
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Aiven cloud database and structural schemas initialized successfully!")
    except Error as e:
        print(f"❌ Initialization on Aiven cloud failed: {e}")

if __name__ == "__main__":
    setup_database()
