# using 'maintenance log' from class diagram
# some functions in here actually make sense to go in the complaints class
# class diagram actually has to change to reflect the implemented functions

""" # methods: from use case (more methods)
    book maintenance visits
    check worker availability
    chceck worker role needed
    record resolution
    log cost and time """
    
""" class: from class diagram 
attributes: self.logid=logid
logid
apartmentid
userid
maintenancedate
timetaken
cost
notes
---
operations: def (with sql statements)
logmaintenance()
calculatetotalcost()
generatemaintenancereport()

"""

class Repair:
    def __init__(self, apartmentID, logID=None, userID=None, maintenanceDate=None, timeTaken=None, Cost=None, Notes=None):
         self.logID = logID
         self.apartmentID = apartmentID
         self.userID = userID
         self.maintenanceDate = maintenanceDate 
         self.timeTaken = timeTaken
         self.Cost= Cost
         self.Notes= Notes
    
    @staticmethod  # it's the same as booking the maintenance too   
    def log_maintenance(db, apartmentID, userID, maintenanceDate):
        query = """
        INSERT INTO MaintenanceLog
        (apartmentID, userID, maintenanceDate, Notes)
        VALUES (%s, %s, %s, %s)
        """
        db.execute(query, (apartmentID, userID, maintenanceDate, None))
    
    @staticmethod
    def calculate_total_cost(db, apartment_id):
        query = """
            SELECT SUM(Cost)
            FROM MaintenanceLog
            WHERE apartmentID=%s
        """
        result = db.fetch_one(query, (apartment_id,))
        return result[0] if result[0] else 0

    @staticmethod 
    def generate_report(db): # ask imaan though
        query = "SELECT * FROM MaintenanceLog"
        return db.fetch_all(query)
     
    @staticmethod # same as log cost and time, removed for redundancy, but this should be for the notes only
    def record_resolution(db, log_id, time_taken, cost, notes):
        query = """
            UPDATE MaintenanceLog
            SET timeTaken=%s, Cost=%s, Notes=%s
            WHERE logID=%s
        """
        db.execute(query, (time_taken, cost, notes, log_id))

    @staticmethod
    def check_availability(db, user_id, date):
        query = """
            SELECT COUNT(*)
            FROM MaintenanceLog
            WHERE userID = %s AND DATE(maintenanceDate) = DATE(%s)
        """
        result = db.fetch_one(query, (user_id, date))
        return result[0] == 0  # True if available
            
    @staticmethod
    def check_role(db, user_id, required_role="maintenance"):
        query = "SELECT Role FROM UserTbl WHERE userID = %s"
        role = db.fetch_one(query, (user_id,))

        if role is None:
            return False

        return role[0] == required_role
    # 22/02 as we dont have dummy data in the user table, it used to crash if the worker didnt exist
    
    

    # more functions

# assign priority (i need a button for this in the repairs page) 
# change the add repair and complaint buttons slightly with conditionals when refreshing the page

##################################################

# bro i dont have an issues class, unless either i make one, or just put combined functions into here, as i have done

# def get_openreq() ISSUES
# def get_completed() # gets last 5 completed ISSUES
# def complete() (resolve)






# helper functions for below:
    @staticmethod
    def get_open_complaints():

        query = """
        SELECT complaintID, apartmentID, Description, reportDate, Severity
        FROM Complaint
        WHERE Status = 'open'
        """

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_closed_complaints():

        query = """
        SELECT complaintID, apartmentID, Description, reportDate, Resolution
        FROM Complaint
        WHERE Status = 'closed'
        """

        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod  
    def get_open_repairs():

        query = """
        SELECT logID, apartmentID, userID, maintenanceDate, Notes
        FROM MaintenanceLog
        WHERE timeTaken IS NULL
        """

        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def get_completed_repairs():

        query = """
        SELECT logID, apartmentID, userID, maintenanceDate, timeTaken, Cost, Notes
        FROM MaintenanceLog
        WHERE timeTaken IS NOT NULL
        """

        cursor.execute(query)
        return cursor.fetchall()
    
    @staticmethod
    def close_complaint(complaint_id, resolution):

        query = """
        UPDATE Complaint
        SET Status = 'closed',
            Resolution = %s
        WHERE complaintID = %s
        """

        cursor.execute(query, (resolution, complaint_id))
    
    
    @staticmethod
    def complete_repair(log_id, time_taken, cost, notes):

        query = """
        UPDATE MaintenanceLog
        SET timeTaken = %s,
            Cost = %s,
            Notes = %s
        WHERE logID = %s
        """

        cursor.execute(query, (time_taken, cost, notes, log_id))
        
    
    
    @staticmethod
    def get_openrequests():
        complaints = get_open_complaints()
        repairs = get_open_repairs()

        requests = []

        for c in complaints:
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": c["Description"],
                "date": c["reportDate"],
                "worker": None,
                "priority": c["Severity"]
            })

        for r in repairs:
            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": r["Notes"],
                "date": r["maintenanceDate"],
                "worker": r["userID"],
                "priority": None
            })

        return requests
    
    def get_completed_requests():

        complaints = get_closed_complaints()
        repairs = get_completed_repairs()

        requests = []

        for c in complaints:
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": c["Description"],
                "date": c["reportDate"],
                "resolution": c["Resolution"]
            })

        for r in repairs:
            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": r["Notes"],
                "date": r["maintenanceDate"],
                "timeTaken": r["timeTaken"]
            })

        return requests

    def complete_request(request_id, request_type, time_taken, notes, cost):

        if request_type == "complaint":

            query = """
            UPDATE Complaint
            SET Status = 'closed',
            Resolution = %s
            WHERE complaintID = %s
            """

            execute_query(query, (notes, request_id))


        elif request_type == "repair":

            query = """
            UPDATE MaintenanceLog
            SET timeTaken = %s,
            Cost = %s,
            Notes = %s
            WHERE logID = %s
            """

            execute_query(query, (time_taken, cost, notes, request_id))