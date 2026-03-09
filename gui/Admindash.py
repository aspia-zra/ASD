from tkinter import *
from tkinter.ttk import Progressbar, Combobox
from . import NavBar
from Models import user_session
from Models.settingBE import changeEmail, changePhone, changePassword, changeFontsize

def dashboard(main):
    for widget in main.winfo_children():
        widget.destroy()

    container = NavBar.navbar(main)

    dashboardFrame = Frame(main)
    dashboardFrame.pack(pady=20, anchor="center")

    dashboardFrame.columnconfigure(0, weight=1)
    dashboardFrame.columnconfigure(1, weight=1)
    dashboardFrame.rowconfigure(0, weight=1)
    dashboardFrame.rowconfigure(1, weight=1)

    apartmentsFrame = Frame(dashboardFrame)
    apartmentsFrame.grid(row=0, column=0, padx=20, pady=20)

    apartments = Label(apartmentsFrame, text="Apartments Occupied")
    apartments.pack(pady=20)

    aptProgress = Progressbar(apartmentsFrame, orient=HORIZONTAL, length=200, mode='determinate')
    aptProgress['value'] = 90
    aptProgress.pack(pady=10)

    rentCollected = Label(apartmentsFrame, text="Rent Collected")
    rentCollected.pack(pady=10)

    rentProgress = Progressbar(apartmentsFrame, orient=HORIZONTAL, length=200, mode='determinate')
    rentProgress['value'] = 90
    rentProgress.pack(pady=10)

    repairsMade = Label(apartmentsFrame, text="Repairs Made")
    repairsMade.pack(pady=10)

    repairsProgress = Progressbar(apartmentsFrame, orient=HORIZONTAL, length=200, mode='determinate')
    repairsProgress['value'] = 25
    repairsProgress.pack(pady=10)

    complaintsMade = Label(apartmentsFrame, text="Complaints Made")
    complaintsMade.pack(pady=10)

    complaintsProgress = Progressbar(apartmentsFrame, orient=HORIZONTAL, length=200, mode='determinate')
    complaintsProgress['value'] = 60
    complaintsProgress.pack(pady=10)

# podium
    podiumFrame = Frame(dashboardFrame)
    podiumFrame.grid(row=1, column=0, padx=20, pady=20)

    podium = Label(podiumFrame, text="Podium", font=("Arial", 18))
    podium.pack(pady=20)

# dropdowns
    dropdownsFrame = Frame(dashboardFrame)
    dropdownsFrame.grid(row=0, column=1, padx=20, pady=20)

    leasesFrame = Frame(dropdownsFrame)
    leasesFrame.pack(pady=10, anchor="center")

    leasesExpiring = Label(leasesFrame, text="Leases Expiring:", font=("Arial", 14))
    leasesExpiring.pack(side=LEFT, padx=10)

    leasesExpiringDropdown = Combobox(leasesFrame, width=20)
    leasesExpiringDropdown['values'] = ["in 30 days", "in 60 days", "in 90 days"]
    leasesExpiringDropdown.pack(side=LEFT, padx=10)

    OverdueFrame = Frame(dropdownsFrame)
    OverdueFrame.pack(pady=10, anchor="center")

    overdueRent = Label(OverdueFrame, text="Overdue Rent:", font=("Arial", 14))
    overdueRent.pack(side=LEFT, padx=10)

    overdueRentDropdown = Combobox(OverdueFrame, width=20)
    overdueRentDropdown['values'] = ["in 30 days", "in 60 days", "in 90 days"]
    overdueRentDropdown.pack(side=LEFT, padx=10)

    highPriorityFrame = Frame(dropdownsFrame)
    highPriorityFrame.pack(pady=10, anchor="center")

    highPriorityRepairs = Label(highPriorityFrame, text="High Priority Repairs:", font=("Arial", 14))
    highPriorityRepairs.pack(side=LEFT, padx=10)

    highPriorityRepairsDropdown = Combobox(highPriorityFrame, width=20)
    highPriorityRepairsDropdown['values'] = ["in 30 days", "in 60 days", "in 90 days"]
    highPriorityRepairsDropdown.pack(side=LEFT, padx=10)

#quickactions and graphs

    qgFrame = Frame(dashboardFrame)
    qgFrame.grid(row=1, column=1, padx=20, pady=20)

    # quick actions
    quickActionsFrame = Frame(qgFrame)
    quickActionsFrame.pack(pady=10, anchor="center")
    
    quickActions = Label(quickActionsFrame, text="Quick Actions", font=("Arial", 18))
    quickActions.pack(pady=20)

    addAptButton = Button(quickActionsFrame, text="Add Apartment", width=10)
    addAptButton.pack(side=LEFT, padx=10)

    createLeaseButton = Button(quickActionsFrame, text="Create Lease", width=10)
    createLeaseButton.pack(side=LEFT, padx=10)

    generalReportButton = Button(quickActionsFrame, text="General Report", width=10)
    generalReportButton.pack(side=LEFT, padx=10)

    # graphs
    graphsFrame = Frame(qgFrame)
    graphsFrame.pack(pady=10, anchor="center")

    graphs = Label(graphsFrame, text="Graphs", font=("Arial", 18))
    graphs.pack(pady=20)