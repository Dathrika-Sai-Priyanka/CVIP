import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

class MedicalAppointmentScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Appointment Scheduler")
        self.patient = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Date (DD-MM-YYYY):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Time (HH:MM AM/PM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)
        self.am_pm_var = tk.StringVar(self.root)
        self.am_pm_var.set("AM") 
        self.am_pm_dropdown = tk.OptionMenu(self.root, self.am_pm_var, "AM", "PM")
        self.am_pm_dropdown.grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Schedule Appointment", command=self.schedule_appointment).grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def validate_date(self, date):
        day, month, year = map(int, date.split('-'))
        if month > 12:
            return False, "Month should be between 01 and 12."
        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_days = 29
            else:
                max_days = 28
        elif month in {4, 6, 9, 11}:
            max_days = 30
        else:
            max_days = 31

        if day < 1 or day > max_days:
            return False, f"Day should be between 01 and {max_days}."
        else:
            pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$'
            if re.match(pattern, date):
                return True, None
            else:
                return False, "Invalid date format. Please use DD-MM-YYYY."

    def validate_time(self, time):
        pattern = r'^\d{2}:\d{2} [AP]M$'
        return re.match(pattern, time)

    def schedule_appointment(self):
        name = self.name_entry.get()
        date_str = self.date_entry.get()
        time_str = self.time_entry.get() + " " + self.am_pm_var.get()  # Combine time and AM/PM
        if name and date_str and time_str:
            is_valid_date, date_error = self.validate_date(date_str)
            if is_valid_date:
                if self.validate_time(time_str):
                    appointment_datetime = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %I:%M %p")
                    current_datetime = datetime.now()
                    if appointment_datetime < current_datetime:
                        messagebox.showerror("Failed", "The selected appointment date and time has already passed.")
                    else:
                        if name in self.patient:
                            self.patient[name].append({"date": date_str, "time": time_str})
                        else:
                            self.patient[name] = [{"date": date_str, "time": time_str}]
                        messagebox.showinfo("Success", "Appointment scheduled successfully!")
                else:
                    messagebox.showerror("Failed", "Invalid time format. Please use HH:MM AM/PM.")
            else:
                messagebox.showerror("Failed", date_error)
        else:
            messagebox.showerror("Failed", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalAppointmentScheduler(root)
    root.mainloop()
