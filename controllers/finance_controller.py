from models.finance_model import FinanceModel

class FinanceController:
    def __init__(self):
        self.model = FinanceModel()

    def get_dashboard_summary(self):
        data = self.model.get_invoice_summary()
        if not data or data[0] == 0:
            return {
                'total_invoices': 0,
                'pending_total': '£0.00',
                'overdue_total': '£0.00',
                'paid_total': '£0.00',
                'total_outstanding': '£0.00',
                'collection_rate': '0%',
                'pending_count': 0,
                'overdue_count': 0,
                'paid_count': 0
            }
        total_invoices, pending, overdue, paid, pending_count, overdue_count, paid_count = data
        pending = float(pending) if pending else 0
        overdue = float(overdue) if overdue else 0
        paid = float(paid) if paid else 0
        total_outstanding = pending + overdue
        total_revenue = paid + total_outstanding
        collection_rate = (paid / total_revenue * 100) if total_revenue > 0 else 0
        return {
            'total_invoices': total_invoices,
            'pending_total': f"£{pending:,.2f}",
            'overdue_total': f"£{overdue:,.2f}",
            'paid_total': f"£{paid:,.2f}",
            'total_outstanding': f"£{total_outstanding:,.2f}",
            'collection_rate': f"{collection_rate:.1f}%",
            'pending_count': pending_count,
            'overdue_count': overdue_count,
            'paid_count': paid_count
        }

    def get_recent_transactions(self, limit=10):
        data = self.model.get_recent_transactions(limit)
        formatted = []
        for row in data:
            amount = float(row[1])
            formatted.append({
                'invoice_id': row[0],
                'amount': f"£{amount:,.2f}",
                'due_date': row[2],
                'status': row[3].capitalize(),
                'date': row[4],
                'tenant': row[5],
                'apartment': row[6]
            })
        return formatted

    def get_upcoming_due(self, days=7):
        data = self.model.get_upcoming_due_dates(days)
        formatted = []
        for row in data:
            amount = float(row[1])
            formatted.append({
                'invoice_id': row[0],
                'amount': f"£{amount:,.2f}",
                'due_date': row[2],
                'tenant': row[3],
                'apartment': row[4]
            })
        return formatted