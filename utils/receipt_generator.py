

from datetime import datetime


def generate_receipt(invoice_id, tenant_name, amount, due_date, status):

    filename = f"receipt_{invoice_id}.txt"

    with open(filename, "w") as file:
        file.write("================================\n")
        file.write("   PARAGON APARTMENT SYSTEM\n")
        file.write("================================\n")
        file.write(f"Receipt Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        file.write("--------------------------------\n")
        file.write(f"Invoice ID:   {invoice_id}\n")
        file.write(f"Tenant:       {tenant_name}\n")
        file.write(f"Amount:       {amount}\n")
        file.write(f"Due Date:     {due_date}\n")
        file.write(f"Status:       {status}\n")
        file.write("--------------------------------\n")
        file.write("Thank you for your payment.\n")
        file.write("================================\n")

    return filename