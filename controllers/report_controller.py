from models.report_model import ReportModel

class ReportController:
    def __init__(self):
        self.model = ReportModel()

    def get_occupancy_data(self, location=None):
        data = self.model.get_occupancy_report(location)
        formatted = []
        for row in data:
            formatted.append({
                'apartment': row[0],
                'type': row[1],
                'status': row[2],
                'city': row[3],
                'tenant': row[4] if row[4] else 'Vacant'
            })
        return formatted

    def get_financial_data(self):
        data = self.model.get_financial_report()
        formatted = []
        total_pending = total_overdue = total_paid = 0
        for row in data:
            amount = float(row[1])
            status = row[3].lower()
            if status == 'pending':
                total_pending += amount
            elif status == 'overdue':
                total_overdue += amount
            elif status == 'paid':
                total_paid += amount
            formatted.append({
                'invoice': row[0],
                'amount': f"£{amount:,.2f}",
                'due_date': row[2],
                'status': row[3].capitalize(),
                'tenant': row[4]
            })
        summary = {
            'total_pending': f"£{total_pending:,.2f}",
            'total_overdue': f"£{total_overdue:,.2f}",
            'total_paid': f"£{total_paid:,.2f}",
            'total_outstanding': f"£{total_pending + total_overdue:,.2f}"
        }
        return formatted, summary

    def get_maintenance_data(self):
        data = self.model.get_maintenance_report()
        formatted = []
        total_cost = total_hours = 0
        for row in data:
            cost = float(row[4]) if row[4] else 0
            hours = int(row[3]) if row[3] else 0
            total_cost += cost
            total_hours += hours
            formatted.append({
                'log_id': row[0],
                'apartment': row[1],
                'date': row[2],
                'hours': hours,
                'cost': f"£{cost:,.2f}",
                'notes': row[5] if row[5] else ''
            })
        summary = {
            'total_cost': f"£{total_cost:,.2f}",
            'total_hours': total_hours,
            'avg_cost_per_hour': f"£{(total_cost/total_hours if total_hours>0 else 0):,.2f}"
        }
        return formatted, summary

    def get_complaint_data(self):
        data = self.model.get_complaint_report()
        formatted = []
        severity_counts = {'1':0,'2':0,'3':0,'4':0,'5':0}
        open_complaints = 0
        for row in data:
            severity = row[2]
            status = row[3]
            severity_counts[severity] = severity_counts.get(severity,0)+1
            if status == 'open':
                open_complaints += 1
            formatted.append({
                'complaint_id': row[0],
                'description': (row[1][:50] + '...') if len(row[1])>50 else row[1],
                'severity': severity,
                'status': status.capitalize(),
                'date': row[4],
                'tenant': row[5]
            })
        summary = {
            'total': len(data),
            'open': open_complaints,
            'severity_high': severity_counts.get('5',0)+severity_counts.get('4',0),
            'severity_medium': severity_counts.get('3',0),
            'severity_low': severity_counts.get('2',0)+severity_counts.get('1',0)
        }
        return formatted, summary