import tkinter as tk
from tkinter import messagebox

class ExpenseSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Sharing App")
        self.expenses = {}
        self.users = set()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="User:").grid(row=0, column=0, sticky="w")
        self.user_entry = tk.Entry(self.root)
        self.user_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=2, column=1, pady=10)
        tk.Label(self.root, text="Expenses:").grid(row=3, column=0, sticky="w")
        self.expense_listbox = tk.Listbox(self.root, width=50, height=10)
        self.expense_listbox.grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Split Bill", command=self.split_bill).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Clear Entries", command=self.clear_entries).grid(row=6, column=0, columnspan=2, pady=10)

    def clear_entries(self):
        self.expenses = {}
        self.users = set()
        self.expense_listbox.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)


    def add_expense(self):
        user = self.user_entry.get()
        amount = self.amount_entry.get()

        if user and amount:
            self.expenses.setdefault(user, 0)
            self.expenses[user] += float(amount)
            self.users.add(user)
            self.expense_listbox.insert(tk.END, f"{user}: Rs. {amount}")
            self.user_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Failed", "Please enter both user and amount.")

    def split_bill(self):
        if len(self.users) < 2:
            messagebox.showerror("Failed", "Add expenses for at least two users.")
            return

        total_expense = sum(self.expenses.values())
        per_person_share = total_expense / len(self.users)
        owed_amounts = {user: per_person_share - self.expenses.get(user, 0) for user in self.users}

        result = "Owe Details:\n"
        for debtor, amount in owed_amounts.items():
            for creditor, credit_amount in owed_amounts.items():
                if debtor != creditor and amount > 0 and credit_amount < 0:
                    transfer_amount = min(amount, -credit_amount)
                    result += f"{debtor} owes Rs. {transfer_amount} to {creditor}\n"
                    amount -= transfer_amount
                    owed_amounts[creditor] += transfer_amount

        messagebox.showinfo("Expense Summary", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSharingApp(root)
    root.mainloop()
