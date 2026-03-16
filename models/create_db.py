import sqlite3

# Connect (this will create pams.db)
conn = sqlite3.connect('pams.db')
cursor = conn.cursor()

# Enable foreign keys
cursor.execute('PRAGMA foreign_keys = ON;')

# Create tables (adapted from MySQL dump)

# Location table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Location (
    locationID INTEGER PRIMARY KEY AUTOINCREMENT,
    City TEXT NOT NULL,
    Address TEXT NOT NULL,
    Phone TEXT
)
''')

# UserTbl table
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserTbl (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName TEXT NOT NULL,
    Phone TEXT,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    Role TEXT CHECK(Role IN ('admin','manager','maintenance','frontdesk')) NOT NULL,
    locationID INTEGER,
    FOREIGN KEY (locationID) REFERENCES Location(locationID) ON DELETE SET NULL
)
''')

# Tenant table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Tenant (
    tenantID INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName TEXT NOT NULL,
    Phone TEXT,
    national_Insurance TEXT,
    Email TEXT UNIQUE,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status TEXT DEFAULT 'active' CHECK(Status IN ('active','inactive'))
)
''')

# Apartment table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Apartment (
    apartmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    locationID INTEGER NOT NULL,
    apartmentNumber TEXT NOT NULL,
    Type TEXT,
    monthlyRent REAL NOT NULL,
    Status TEXT DEFAULT 'available' CHECK(Status IN ('available','occupied','maintenance')),
    FOREIGN KEY (locationID) REFERENCES Location(locationID) ON DELETE CASCADE
)
''')

# LeaseAgreement table
cursor.execute('''
CREATE TABLE IF NOT EXISTS LeaseAgreement (
    leaseID INTEGER PRIMARY KEY AUTOINCREMENT,
    tenantID INTEGER NOT NULL,
    apartmentID INTEGER NOT NULL,
    startDate TEXT NOT NULL,
    endDate TEXT NOT NULL,
    depositAmount REAL,
    monthlyRent REAL NOT NULL,
    Status TEXT DEFAULT 'active' CHECK(Status IN ('active','ended','renewal')),
    FOREIGN KEY (tenantID) REFERENCES Tenant(tenantID) ON DELETE CASCADE,
    FOREIGN KEY (apartmentID) REFERENCES Apartment(apartmentID) ON DELETE CASCADE
)
''')

# Invoice table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Invoice (
    invoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
    leaseID INTEGER NOT NULL,
    Amount REAL NOT NULL,
    dueDate TEXT NOT NULL,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status TEXT DEFAULT 'pending' CHECK(Status IN ('paid','pending','overdue')),
    Description TEXT,
    FOREIGN KEY (leaseID) REFERENCES LeaseAgreement(leaseID) ON DELETE CASCADE
)
''')

# Complaint table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Complaint (
    complaintID INTEGER PRIMARY KEY AUTOINCREMENT,
    tenantID INTEGER NOT NULL,
    apartmentID INTEGER NOT NULL,
    Description TEXT NOT NULL,
    reportDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Severity TEXT NOT NULL DEFAULT '1' CHECK(Severity IN ('1','2','3','4','5')),
    Status TEXT DEFAULT 'open' CHECK(Status IN ('open','closed')),
    Resolution TEXT,
    FOREIGN KEY (tenantID) REFERENCES Tenant(tenantID) ON DELETE CASCADE,
    FOREIGN KEY (apartmentID) REFERENCES Apartment(apartmentID) ON DELETE CASCADE
)
''')

# MaintenanceLog table
cursor.execute('''
CREATE TABLE IF NOT EXISTS MaintenanceLog (
    logID INTEGER PRIMARY KEY AUTOINCREMENT,
    apartmentID INTEGER NOT NULL,
    userID INTEGER,
    maintenanceDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    timeTaken INTEGER,
    Cost REAL,
    Notes TEXT,
    FOREIGN KEY (apartmentID) REFERENCES Apartment(apartmentID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES UserTbl(userID) ON DELETE SET NULL
)
''')

# ReportLog table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ReportLog (
    reportID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    reportType TEXT NOT NULL,
    Period TEXT NOT NULL,
    Generated_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Data TEXT,
    FOREIGN KEY (userID) REFERENCES UserTbl(userID) ON DELETE SET NULL
)
''')

# Commit and close
conn.commit()
print(" Tables created successfully.")