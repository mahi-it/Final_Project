#Import the requied libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# CSV file and valid expense categories
file="expenses.csv"
categories = ["Food", "Transport", "Utilities", "Entertainment",
    "Education", "Shopping", "Health", "Other"]


# Class to manage expense tracking operations
class ExpenseTracker:

    def __init__(self):
        # Load existing expenses or create a new CSV file
        if os.path.exists(file):
            self.df = pd.read_csv(file)

            # Convert Date and Amount to the correct data types
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            self.df["Amount"] = pd.to_numeric(self.df["Amount"])

            # Replace missing dates with today's date
            self.df["Date"] = self.df["Date"].fillna(pd.Timestamp.today())
            self.df["Date"] = self.df["Date"].dt.strftime("%Y-%m-%d")

            # Replace missing amounts with mean value of the total amount
            self.df["Amount"] = self.df["Amount"].fillna(self.df["Amount"].mean())

            # Replace missing categories and descriptions
            self.df["Category"] = self.df["Category"].fillna("Other")
            self.df["Description"] = self.df["Description"].fillna("No description")

            # Save the dataset without an index column
            self.df.to_csv(file, index=False)

        else:
            self.df = pd.DataFrame( columns=["Date", "Amount", "Category", "Description"])
            self.df.to_csv(file, index=False)

    def add_expense(self, date, amount, category, description):
        # Validate and save a new expense
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            amount = float(amount)

            if amount <= 0:
                print("Amount must be positive.")
                return

            category = category.strip().title()
            if category not in categories:
                print("Invalid category.")
                return

            if not description.strip():
                print("Description cannot be empty.")
                return

            new_row = pd.DataFrame([{"Date": date,"Amount": amount,"Category": category,"Description": description.strip() }])

            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.df.to_csv(file, index=False)
            print("Expense added successfully.")

        except ValueError:
            print("Enter a valid date and amount.")

    def get_summary(self):
        # Calculate basic expense statistics
        if self.df.empty:
            print("No expenses available.")
            return

        amounts = pd.to_numeric(self.df["Amount"])
        print("\nTotal expenses:", np.sum(amounts))
        print("Average expense:", np.mean(amounts))
        print("Highest expense:", np.max(amounts))
        print("Lowest expense:", np.min(amounts))

        print("\nCategory-wise spending:")
        print(self.df.groupby("Category")["Amount"].sum())

    def filter_expenses(self):
        # Filter expenses by category, date, or amount
        print("1. Category")
        print("2. Date range")
        print("3. Amount range")

        choice = int(input("Choose filter: "))
        data = self.df.copy()

        if choice == 1:
            category = input("Enter category: ").strip().title()
            data = data[data["Category"] == category]

        elif choice == 2:
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")

            try:
                dates = pd.to_datetime(data["Date"])
                start_date = pd.to_datetime(start, format="%Y-%m-%d")
                end_date = pd.to_datetime(end, format="%Y-%m-%d")

                if start_date > end_date:
                    print("Invalid date range.")
                    return

                data = data[(dates >= start_date) & (dates <= end_date)]

            except ValueError:
                print("Enter valid dates.")
                return

        elif choice == 3:
            try:
                low = float(input("Minimum amount: "))
                high = float(input("Maximum amount: "))

                if low < 0 or high < low:
                    print("Invalid amount range.")
                    return

                data = data[ (data["Amount"] >= low) &(data["Amount"] <= high)]

            except ValueError:
                print("Enter valid amounts.")
                return

        else:
            print("Invalid choice.")
            return

        if data.empty:
            print("No matching expenses found.")
        else:
            print(data.to_string(index=False))
            print("Filtered total:", data["Amount"].sum())

    def generate_report(self):
        # Generate and save an expense report
        if self.df.empty:
            print("No expenses available.")
            return

        total = self.df["Amount"].sum()
        average = self.df["Amount"].mean()
        category = self.df.groupby("Category")["Amount"].sum()

        report = ( f"EXPENSE TRACKER REPORT\n"
            f"----------------------\n"
            f"Number of expenses: {len(self.df)}\n"
            f"Total spending: Rs. {total:.2f}\n"
            f"Average expense: Rs. {average:.2f}\n"
            f"Highest spending category: {category.idxmax()}\n"
            f"{category.to_string()}\n")

        print(report)

        with open("expense_report.txt", "w") as report_file:
            report_file.write(report)

        print("Report saved.")

    # Visualize spending by category using Seaborn
    def show_bar_chart(self, category):
        plt.figure(figsize=(8, 4))
        sns.barplot(x=category.index, y=category.values)
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (Rs.)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    # Visualize monthly spending trends using Matplotlib
    def show_line_plot(self, monthly):
        plt.figure(figsize=(8, 4))
        plt.plot( monthly.index.astype(str), monthly.values, marker="o",linestyle="--",color="hotpink")
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Amount (Rs.)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    # Show each category's share of total spending
    def show_pie_chart(self, category):
        plt.figure(figsize=(6, 6))
        plt.pie(category.values, labels=category.index,autopct='%1.1f%%' )
        plt.title("Spending Distribution")
        plt.show()

    # Show the distribution of expense amounts
    def show_histogram(self, data):
        plt.figure(figsize=(8, 4))
        sns.histplot(data=data, x="Amount", bins=8)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount (Rs.)")
        plt.ylabel("Frequency")
        plt.show()


# Main function to display the menu and run the tracker
def main():
    tracker = ExpenseTracker()

    while True:
        print("\n---------EXPENSE TRACKER-----------")
        print("1. Add expense")
        print("2. View summary")
        print("3. Filter expenses")
        print("4. Generate report")
        print("5. Show charts")
        print("6. View all expenses")
        print("7. Exit")

        try:
            choice = int(input("Enter choice: "))

            match choice:
                case 1:
                    date = input("Date (YYYY-MM-DD): ")
                    amount = input("Amount: ")
                    category = input("Category: ")
                    description = input("Description: ")

                    tracker.add_expense(
                        date, amount, category, description
                    )

                case 2:
                    tracker.get_summary()

                case 3:
                    tracker.filter_expenses()

                case 4:
                    tracker.generate_report()

                case 5:
                    if tracker.df.empty:
                        print("No expenses available.")
                    else:
                        # Prepare data for category and monthly charts
                        data = tracker.df.copy()
                        data["Date"] = pd.to_datetime(data["Date"])
                        data["Amount"] = pd.to_numeric(data["Amount"])

                        category = data.groupby("Category")["Amount"].sum()
                        monthly = data.groupby(data["Date"].dt.to_period("M")
                        )["Amount"].sum()

                        # Display the chart selection menu
                        while True:
                            print("\n----------- CHOOSE A CHART ---------")
                            print("1. Bar Chart")
                            print("2. Pie Chart")
                            print("3. Line Plot")
                            print("4. Histogram")
                            print("5. Go Back")

                            chart_choice = int( input("Enter chart choice: ") )

                            match chart_choice:
                                case 1:
                                    tracker.show_bar_chart(category)
                                case 2:
                                    tracker.show_pie_chart(category)
                                case 3:
                                    tracker.show_line_plot(monthly)
                                case 4:
                                    tracker.show_histogram(data)
                                case 5:
                                    print("Going back to main Menu")
                                    break
                                case _:
                                    print("Invalid chart choice.")

                case 6:
                    print(tracker.df.to_string(index=False))

                case 7:
                    print("Thank you for using Expense Tracker!")
                    break

                case _:
                    print("Please enter a choice from 1 to 7.")

        except ValueError:
            print("Please enter integer value only.")


# Run the program when this file is executed directly
if __name__ == "__main__":
    main()