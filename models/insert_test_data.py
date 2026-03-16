import sqlite3

conn = sqlite3.connect('pams.db')
cursor = conn.cursor()

# Clear existing data 
cursor.execute("DELETE FROM Invoice")
cursor.execute("DELETE FROM LeaseAgreement")
cursor.execute("DELETE FROM Apartment")
cursor.execute("DELETE FROM Tenant")
cursor.execute("DELETE FROM UserTbl")
cursor.execute("DELETE FROM Location")

# Insert a location
cursor.execute('''
INSERT INTO Location (City, Address, Phone) VALUES (?, ?, ?)
''', ('Bristol', '123 High Street', '0117 123 4567'))
location_id = cursor.lastrowid

# Insert a user (frontdesk)
cursor.execute('''
INSERT INTO UserTbl (fullName, Phone, Email, Password, Role, locationID) VALUES (?, ?, ?, ?, ?, ?)
''', ('John Smith', '0117 111 2222', 'john@paragon.com', 'password123', 'frontdesk', location_id))

# Insert two tenants
cursor.execute('''
INSERT INTO Tenant (fullName, Phone, national_Insurance, Email) VALUES (?, ?, ?, ?)
''', ('Alice Brown', '0117 333 4444', 'AB123456C', 'alice@email.com'))
tenant1_id = cursor.lastrowid

cursor.execute('''
INSERT INTO Tenant (fullName, Phone, national_Insurance, Email) VALUES (?, ?, ?, ?)
''', ('Bob Wilson', '0117 555 6666', 'BW789012D', 'bob@email.com'))
tenant2_id = cursor.lastrowid

# Insert two apartments
cursor.execute('''
INSERT INTO Apartment (locationID, apartmentNumber, Type, monthlyRent, Status) VALUES (?, ?, ?, ?, ?)
''', (location_id, 'A101', '2 Bedroom', 1200.00, 'occupied'))
apt1_id = cursor.lastrowid

cursor.execute('''
INSERT INTO Apartment (locationID, apartmentNumber, Type, monthlyRent, Status) VALUES (?, ?, ?, ?, ?)
''', (location_id, 'A102', '1 Bedroom', 950.00, 'available'))
apt2_id = cursor.lastrowid

# Insert leases
cursor.execute('''
INSERT INTO LeaseAgreement (tenantID, apartmentID, startDate, endDate, depositAmount, monthlyRent, Status)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', (tenant1_id, apt1_id, '2025-01-01', '2025-12-31', 1200.00, 1200.00, 'active'))
lease1_id = cursor.lastrowid

cursor.execute('''
INSERT INTO LeaseAgreement (tenantID, apartmentID, startDate, endDate, depositAmount, monthlyRent, Status)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', (tenant2_id, apt2_id, '2025-02-01', '2026-01-31', 950.00, 950.00, 'active'))
lease2_id = cursor.lastrowid

# Insert invoices
cursor.execute('''
INSERT INTO Invoice (leaseID, Amount, dueDate, Status, Description) VALUES (?, ?, ?, ?, ?)
''', (lease1_id, 1200.00, '2025-02-01', 'pending', 'February rent'))

cursor.execute('''
INSERT INTO Invoice (leaseID, Amount, dueDate, Status, Description) VALUES (?, ?, ?, ?, ?)
''', (lease1_id, 1200.00, '2025-03-01', 'pending', 'March rent'))

cursor.execute('''
INSERT INTO Invoice (leaseID, Amount, dueDate, Status, Description) VALUES (?, ?, ?, ?, ?)
''', (lease2_id, 950.00, '2025-03-01', 'paid', 'March rent'))

conn.commit()
print(" Comprehensive sample data inserted.")
conn.close()