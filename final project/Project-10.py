import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class GlobalHappinessData:
    def __init__(self):
        self.data = None
        self.fig = None

    # Check whether a dataset has been loaded
    def check_data(self):
        if self.data is None:
            print("\nPlease load a dataset first.")
            return False
        return True

    # Safely read integer menu choices
    @staticmethod
    def get_int(prompt):
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")
            return None

    # 1. Load dataset
    def load_data(self, file_path):
        try:
            loaded_data = pd.read_csv(file_path)
            self.data = loaded_data
            print("Dataset loaded successfully!")
            print("Rows:", len(self.data))
            print("Columns:", len(self.data.columns))

        except FileNotFoundError:
            print("CSV file not found.")
        except pd.errors.EmptyDataError:
            print("The CSV file is empty.")
        except pd.errors.ParserError as e:
            print("Error reading CSV file:", e)
        except Exception as e:
            print("Error:", e)

    # 2. Explore dataset
    def explore_data(self):
        if not self.check_data():
            return

        print("\n--- Explore Data ---")
        print("1. Display first 5 rows")
        print("2. Display last 5 rows")
        print("3. Display column names")
        print("4. Display data types")
        print("5. Display basic information")

        choice = self.get_int("Enter your choice: ")

        match choice:
            case 1:
                print(self.data.head())
            case 2:
                print(self.data.tail())
            case 3:
                print(self.data.columns.to_list())
            case 4:
                print(self.data.dtypes)
            case 5:
                self.data.info()
            case None:
                return
            case _:
                print("Invalid choice!")

    # 3. Handle missing data
    def clean_data(self):
        if not self.check_data():
            return

        print("\n--- Handle Missing Data ---")
        print("1. Display rows with missing values")
        print("2. Fill numeric missing values with mean")
        print("3. Drop rows with missing values")
        print("4. Replace missing values with a specific value")

        choice = self.get_int("Enter your choice: ")

        match choice:
            case 1:
                missing = self.data[self.data.isna().any(axis=1)]

                if missing.empty:
                    print("No missing values found.")
                else:
                    print(missing)

            case 2:
                numeric_cols = self.data.select_dtypes(
                    include=np.number
                ).columns

                if len(numeric_cols) == 0:
                    print("No numeric columns available.")
                    return

                self.data.loc[:, numeric_cols] = self.data[
                    numeric_cols
                ].fillna(self.data[numeric_cols].mean())

                print("Numeric missing values filled with mean.")

            case 3:
                before = len(self.data)
                self.data.dropna(inplace=True)
                removed = before - len(self.data)
                print(f"{removed} row(s) removed.")

            case 4:
                value = input("Enter replacement value: ")
                self.data.fillna(value, inplace=True)
                print("Missing values replaced.")

            case None:
                return

            case _:
                print("Invalid choice!")

    # 4. Mathematical operations
    
    def mathematical_operations(self):
        if not self.check_data():
            return

        numeric_cols = self.data.select_dtypes(include=np.number ).columns.to_list()

        if not numeric_cols:
            print("No numeric columns available.")
            return

        print("Numeric columns:", numeric_cols)
        column = input("Enter column name: ").strip()

        if column not in numeric_cols:
            print("Invalid numeric column!")
            return

        print("\n--- Element-wise Mathematical Operations ---")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Modulus")
        print("6. Power")
        print("7. Square")
        print("8. Square Root")
        print("9. Absolute Value")

        choice = self.get_int("Enter your choice: ")

        if choice is None or choice not in range(1, 10):
            print("Invalid choice!")
            return

        values = self.data[column]

        try:
            if choice in [1, 2, 3, 4, 5, 6]:
                n = float(input("Enter a number: "))

            match choice:
                case 1:
                    result = values + n
                case 2:
                    result = values - n
                case 3:
                    result = values * n
                case 4:
                    if n == 0:
                        print("Cannot divide by zero.")
                        return
                    result = values / n
                case 5:
                    if n == 0:
                        print("Cannot calculate modulus by zero.")
                        return
                    result = values % n
                case 6:
                    result = values ** n
                case 7:
                    result = values ** 2
                case 8:
                    if (values.dropna() < 0).any():
                        print("Cannot calculate real square roots for negative values.")
                        return
                    result = np.sqrt(values)
                case 9:
                    result = values.abs()

            print("\nOriginal values and results:")
            print(pd.DataFrame({ "Original": values,"Result": result }))

        except (ValueError, TypeError, OverflowError) as e:
            print("Error performing operation:", e)


    # 5. Combine DataFrames
    def combine_data(self):
        if not self.check_data():
            return

        print("\n--- Combine DataFrames ---")
        print("1. Concatenate DataFrames")
        print("2. Merge DataFrames using a common column")

        choice = self.get_int("Enter your choice: ")

        if choice not in (1, 2):
            if choice is not None:
                print("Invalid choice!")
            return

        file_path = input("Enter second CSV file path: ").strip()

        try:
            second_data = pd.read_csv(file_path)

        except FileNotFoundError:
            print("Second CSV file not found.")
            return
        except pd.errors.EmptyDataError:
            print("Second CSV file is empty.")
            return
        except Exception as e:
            print("Error reading second dataset:", e)
            return

        if choice == 1:
            result = pd.concat([self.data, second_data],ignore_index=True )

        else:
            common_columns = [ col for col in self.data.columns if col in second_data.columns ]

            print("Common columns:", common_columns)

            if not common_columns:
                print("No common columns available for merging.")
                return

            key = input("Enter common column name: ").strip()

            if (key not in self.data.columns or key not in second_data.columns):
                print("Column not found in both datasets.")
                return

            result = pd.merge(self.data,second_data,on=key,how="inner")

        print(result)

        save = input("Replace current dataset? (y/n): ").strip().lower()

        if save == "y":
            self.data = result
            print("Current dataset updated.")

    # 6. Split dataset
    def split_data(self):
        if not self.check_data():
            return

        print("\n--- Split Data ---")
        print("Available columns:", list(self.data.columns))

        column = input("Enter column name to split by: ").strip()

        if column not in self.data.columns:
            print("Invalid column name!")
            return

        value = input("Enter value to split: ")

        first = self.data[self.data[column].astype(str) == value]

        second = self.data[self.data[column].astype(str) != value ]

        print("\nFirst dataset:")
        print(first)

        print("\nSecond dataset:")
        print(second)

        save = input("Save both groups as CSV files? (y/n): ").strip().lower()

        if save == "y":
            try:
                first.to_csv("happiness_group_1.csv", index=False)
                second.to_csv("happiness_group_2.csv", index=False)
                print("Both groups saved successfully.")
            except Exception as e:
                print("Error saving datasets:", e)

    # 7. Search, sort and filter
    def search_sort_filter(self):
        if not self.check_data():
            return

        print("\n--- Search, Sort and Filter ---")
        print("1. Search for a value")
        print("2. Sort data")
        print("3. Filter numeric data")
        print("4. Filter by category")

        choice = self.get_int("Enter your choice: ")

        if choice is None:
            return

        try:
            match choice:
                case 1:
                    column = input("Enter column name: ").strip()

                    if column not in self.data.columns:
                        print("Invalid column!")
                        return

                    value = input("Enter value to search: ")

                    result = self.data[self.data[column].astype(str) == value ]
                    print(result)

                case 2:
                    column = input("Enter column name to sort: ").strip()

                    if column not in self.data.columns:
                        print("Invalid column!")
                        return

                    ascending = (
                        input("Ascending order? (y/n): ")
                        .strip().lower() == "y"
                    )

                    print(self.data.sort_values(by=column,ascending=ascending))

                case 3:
                    numeric_cols = self.data.select_dtypes(include=np.number).columns.tolist()

                    if not numeric_cols:
                        print("No numeric columns available.")
                        return

                    print("Numeric columns:", numeric_cols)
                    column = input("Enter numeric column: ").strip()

                    if column not in numeric_cols:
                        print("Invalid numeric column!")
                        return

                    value = float(input("Enter minimum value: "))

                    print(self.data[self.data[column] > value])

                case 4:
                    column = input("Enter category column: " ).strip()

                    if column not in self.data.columns:
                        print("Invalid column!")
                        return

                    value = input("Enter category value: ")

                    print(self.data[self.data[column].astype(str) == value])

                case _:
                    print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number.")

    # 8. Advanced operations
    def advanced_operations(self):
        if not self.check_data():
            return

        print("\n--- Advanced Operations ---")
        print("1. Create a pivot table")
        print("2. Re-index DataFrame")
        print("3. Display transformed group averages")
        print("4. Rename a column")

        choice = self.get_int("Enter your choice: ")

        if choice is None:
            return

        try:
            match choice:
                case 1:
                    print("Available columns:", list(self.data.columns))

                    index_col = input("Enter index/group column: ").strip()

                    value_col = input("Enter numeric values column: ").strip()

                    if index_col not in self.data.columns:
                        print("Invalid index column!")
                        return

                    numeric_cols = self.data.select_dtypes( include=np.number).columns

                    if value_col not in numeric_cols:
                        print("Values column must be numeric!")
                        return

                    if self.data.empty:
                        print("The dataset is empty.")
                        return

                    result = pd.pivot_table(self.data,index=index_col,values=value_col,aggfunc=["sum", "mean", "count"] )
                    print(result)

                case 2:
                    print(self.data.reset_index())

                case 3:
                    group_col = input("Enter group column: ").strip()

                    value_col = input("Enter numeric column: ").strip()

                    if group_col not in self.data.columns:
                        print("Invalid group column!")
                        return

                    numeric_cols = self.data.select_dtypes( include=np.number).columns

                    if value_col not in numeric_cols:
                        print("Invalid numeric column!")
                        return

                    result = self.data.assign(  Group_Average=self.data.groupby( group_col)[value_col].transform("mean") )

                    print(result)

                case 4:
                    print("Available columns:", list(self.data.columns))

                    old_name = input("Enter current column name: ").strip()

                    if old_name not in self.data.columns:
                        print("Invalid column name!")
                        return

                    new_name = input("Enter new column name: ").strip()

                    if not new_name:
                        print("New column name cannot be empty.")
                        return

                    if (new_name != old_name and new_name in self.data.columns):
                        print("That column name already exists!")
                        return

                    self.data.rename( columns={old_name: new_name}, inplace=True)
                    print("Column renamed successfully!")

                case _:
                    print("Invalid choice!")

        except (ValueError, TypeError) as e:
            print("Could not complete operation:", e)

    # 9. Statistical analysis
    def statistical_analysis(self):
        if not self.check_data():
            return

        numeric = self.data.select_dtypes(include=np.number)

        if numeric.empty:
            print("No numeric data available.")
            return

        print("\n--- Statistical Analysis ---")
        print("1. Sum")
        print("2. Mean")
        print("3. Median")
        print("4. Standard deviation")
        print("5. Variance")
        print("6. Minimum and maximum")
        print("7. Percentiles")
        print("8. Correlation")
        print("9. Full descriptive statistics")
        print("10. Group-wise analysis")

        choice = self.get_int("Enter your choice: ")

        if choice is None:
            return

        try:
            match choice:
                case 1:
                    print(numeric.sum())

                case 2:
                    print(numeric.mean())

                case 3:
                    print(numeric.median())

                case 4:
                    print(numeric.std())

                case 5:
                    print(numeric.var())

                case 6:
                    print("Minimum:\n", numeric.min())
                    print("Maximum:\n", numeric.max())

                case 7:
                    print("25th percentile:\n", numeric.quantile(0.25))
                    print("50th percentile:\n", numeric.quantile(0.50))
                    print("75th percentile:\n", numeric.quantile(0.75))

                case 8:
                    print(numeric.corr())

                case 9:
                    print(numeric.describe())
                    print("\nStandard deviation:\n", numeric.std())
                    print("\nVariance:\n", numeric.var())
                    print(
                        "\nQuartiles:\n",
                        numeric.quantile([0.25, 0.50, 0.75])
                    )

                case 10:
                    group_col = input(
                        "Enter group column: "
                    ).strip()

                    metric = input("Enter numeric column to analyze: ").strip()

                    if group_col not in self.data.columns:
                        print("Invalid group column!")
                        return

                    if metric not in numeric.columns:
                        print("Invalid numeric column!")
                        return

                    result = self.data.groupby(group_col)[metric].agg( ["sum", "mean", "count", "min", "max"]
                    )

                    print(result)

                case _:
                    print("Invalid choice!")

        except (ValueError, TypeError) as e:
            print("Could not calculate statistics:", e)

    # 10. Visualization: multiple plots adapted for the World Happiness Report
    def visualize_data(self):
        if not self.check_data():
            return

        while True:
            print("\nVisualization Menu")
            print("1. Bar Plot")
            print("2. Line Plot")
            print("3. Scatter Plot")
            print("4. Pie Chart")
            print("5. Histogram")
            print("6. Box Plot")
            print("7. Violin Plot")
            print("8. Heatmap")

            try:
                choice = int(input("Choose plot type: "))
            except ValueError:
                print("Please enter an integer.")
                continue


            if choice not in range(1, 9):
                print("Invalid choice.")
                continue

            print("\nAvailable columns:")
            for col in self.data.columns:
                print(col)

            try:
                # 1. Bar Plot
                if choice == 1:
                    x = input("Enter X-axis column: ").strip()
                    y = input("Enter Y-axis column: ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid data available.")
                        continue

                    sns.barplot(data=data, x=x, y=y)
                    plt.title(f"{y} by {x}")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 2. Line Plot
                elif choice == 2:
                    x = input("Enter X-axis column: ").strip()
                    y = input("Enter Y-axis column: ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid data available.")
                        continue

                    sns.lineplot(data=data, x=x, y=y)
                    plt.title(f"{y} by {x}")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 3. Scatter Plot
                elif choice == 3:
                    x = input("Enter X-axis column: ").strip()
                    y = input("Enter Y-axis column: ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[x] = pd.to_numeric(data[x], errors="coerce")
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("Choose two numeric columns.")
                        continue

                    sns.scatterplot(data=data, x=x, y=y)
                    plt.title(f"{y} vs {x}")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 4. Pie Chart
                elif choice == 4:
                    x = input("Enter category column (X): ").strip()
                    y = input("Enter numeric column (Y): ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid data available.")
                        continue

                    pie_data = data.groupby(x)[y].sum()

                    if pie_data.empty or pie_data.sum() == 0:
                        print("No valid values for pie chart.")
                        continue

                    pie_data.plot.pie(autopct="%1.1f%%",figsize=(7, 7) )
                    plt.title(f"{y} by {x}")
                    plt.ylabel("")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 5. Histogram
                elif choice == 5:
                    x = input("Enter column for histogram: ").strip()

                    if x not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    values = pd.to_numeric(self.data[x], errors="coerce").dropna()

                    if values.empty:
                        print("Choose a numeric column.")
                        continue

                    plt.hist(values, bins=10, edgecolor="black")
                    plt.xlabel(x)
                    plt.ylabel("Frequency")
                    plt.title(f"Distribution of {x}")
                    plt.xticks(rotation=45, ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 6. Box Plot
                elif choice == 6:
                    x = input("Enter X-axis column: ").strip()
                    y = input("Enter Y-axis column: ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid data available.")
                        continue

                    sns.boxplot(data=data, x=x, y=y)
                    plt.title(f"{y} by {x}")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 7. Violin Plot
                elif choice == 7:
                    x = input("Enter X-axis column: ").strip()
                    y = input("Enter Y-axis column: ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid data available.")
                        continue

                    sns.violinplot(data=data, x=x, y=y)
                    plt.title(f"{y} by {x}")
                    plt.xticks(rotation=45,ha="right")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                # 8. Heatmap
                elif choice == 8:
                    x = input("Enter first numeric column (X): ").strip()
                    y = input("Enter second numeric column (Y): ").strip()

                    if x not in self.data.columns or y not in self.data.columns:
                        print("Invalid column name.")
                        continue

                    data = self.data[[x, y]].copy()
                    data[x] = pd.to_numeric(data[x], errors="coerce")
                    data[y] = pd.to_numeric(data[y], errors="coerce")
                    data = data.dropna(subset=[x, y])

                    if data.empty:
                        print("No valid numeric data available.")
                        continue

                    correlation = data[[x, y]].corr()

                    sns.heatmap(correlation,annot=True,cmap="coolwarm",fmt=".2f")
                    plt.title(f"Correlation between {x} and {y}")
                plt.xticks(rotation=45,ha="right")
                plt.grid(True)
                plt.tight_layout()
                plt.show()

            except Exception as e:
                plt.close("all")
                print("Could not create plot:", e)

    # 11. Save visualization
    def save_visualization(self):
        if self.fig is None:
            print("Please generate a visualization first.")
            return

        file_name = input( "Enter file name (for example, plot.png): ").strip()

        if not file_name:
            print("File name cannot be empty.")
            return

        try:
            self.fig.savefig( file_name,dpi=300,bbox_inches="tight" )
            print("Visualization saved successfully:", file_name)

        except Exception as e:
            print("Error saving visualization:", e)

    # 12. Main menu
    def main(self):
        while True:
            print("\n------- Global Happiness Report Analysis -------")
            print("1. Load Dataset")
            print("2. Explore Data")
            print("3. Perform DataFrame Operations")
            print("4. Handle Missing Data")
            print("5. Generate Descriptive Statistics")
            print("6. Data Visualization")
            print("7. Save Visualization")
            print("8. Exit")
            print("-----------------------------------------------------")

            choice = self.get_int("Enter your choice: ")

            if choice is None:
                continue

            match choice:
                case 1:
                    file_path = input("Enter the path of the dataset (CSV file): ").strip()
                    self.load_data(file_path)

                case 2:
                    self.explore_data()

                case 3:
                    # Submenu loops until the user chooses option 6
                    while True:
                        print("\n--- DataFrame Operations ---")
                        print("1. Mathematical Operations")
                        print("2. Combine DataFrames")
                        print("3. Split Data")
                        print("4. Search, Sort and Filter")
                        print("5. Advanced Operations")
                        print("6. Return to Main Menu")

                        choice = self.get_int("Enter your choice: " )

                        match choice:
                            case 1:
                                self.mathematical_operations()
                            case 2:
                                self.combine_data()
                            case 3:
                                self.split_data()
                            case 4:
                                self.search_sort_filter()
                            case 5:
                                self.advanced_operations()
                            case 6:
                                print("Moving back to main menu")
                                break
                            case _:
                                print("Invalid choice!")

                case 4:
                    self.clean_data()

                case 5:
                    self.statistical_analysis()

                case 6:
                    self.visualize_data()

                case 7:
                    self.save_visualization()

                case 8:
                    print("Exiting the program. Goodbye!")
                    break

                case _:
                    print("Invalid choice!")


if __name__ == "__main__":
    analyzer = GlobalHappinessData()
    analyzer.main()
