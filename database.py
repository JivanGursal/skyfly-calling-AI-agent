import sqlite3

def init_db():
    conn = sqlite3.connect('skyfly_leads.db')
    cursor = conn.cursor()
    # Skyfly Leads Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            service_interested TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            budget TEXT,
            status TEXT DEFAULT 'New'
        )
    ''')
    conn.commit()
    conn.close()

def insert_lead(name, service, contact, budget="Not Specified"):
    conn = sqlite3.connect('skyfly_leads.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (customer_name, service_interested, contact_info, budget)
        VALUES (?, ?, ?, ?)
    ''', (name, service, contact, budget))
    conn.commit()
    conn.close()