import sqlite3

DB_NAME = "paragon.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def insert_tenant(full_name, phone, ni, email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT tenantID FROM Tenant WHERE Email=?", (email,))
    if cur.fetchone():
        conn.close()
        raise Exception("Duplicate email")

    cur.execute("""
        INSERT INTO Tenant (fullName, Phone, national_Insurance, Email)
        VALUES (?, ?, ?, ?)
    """, (full_name, phone, ni, email))

    conn.commit()
    conn.close()

def list_tenants():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT tenantID, fullName, Email FROM Tenant")
    rows = cur.fetchall()

    conn.close()
    return rows

def get_all_tenants():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT tenantID, fullName, Phone, national_Insurance, Email
        FROM Tenant
        ORDER BY tenantID DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    for row in list_tenants():
        print(row)