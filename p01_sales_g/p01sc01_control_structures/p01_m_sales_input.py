import csv
import datetime
import os

def get_amount():
    while True:
        try:
            amount = float(input("Amount: "))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

def get_date():
    while True:
        try:
            year = int(input("Year (2000-2999): "))
            if 2000 <= year <= 2999:
                break
            else:
                print("Year must be between 2000 and 2999.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")
    while True:
        try:
            month = int(input("Month (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print("Month must be between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid month.")
    while True:
        try:
            day = int(input("Day (1-28): "))
            if 1 <= day <= 28:
                break
            else:
                print("Day must be between 1 and 28.")
        except ValueError:
            print("Invalid input. Please enter a valid day.")
    return datetime.date(year, month, day)

def get_region():
    while True:
        region = input("Region ('w', 'm', 'c', 'e'): ")
        if region in ['w', 'm', 'c', 'e']:
            return region
        else:
            print("Region must be one of the following: ('w', 'm', 'c', 'e').")

def get_date_from_string(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def add_sales(sales_data):
    amount = get_amount()
    date = get_date()
    region = get_region()
    sales_data.append({
        "date": date,
        "quarter": (date.month - 1) // 3 + 1,
        "region": region,
        "amount": amount
    })
    print(f"Sales for {date} is added.")

def view_sales(sales_data):
    if not sales_data:
        print("No sales to view.")
        return
    print("     Date           Quarter        Region                  Amount ")
    print("-----------------------------------------------------------------")
    for i, sales in enumerate(sales_data, start=1):
        print(f"{i}.   {sales['date']}     {sales['quarter']}              {sales['region']}                   {sales['amount']:.1f}")
    print("-----------------------------------------------------------------")
    print(f"TOTAL                                                     {sum(s['amount'] for s in sales_data):.1f}")

def import_sales(sales_data, imported_files):
    filename = input("Enter name of file to import: ")
    if filename in imported_files:
        print("File has already been imported.")
        return
    if not filename.startswith("sales_q") or not filename.endswith(".csv"):
        print("Filename doesn't follow the expected format of 'sales_qn_yyyy_r.csv.")
        return
    if filename[-6] not in ['w', 'm', 'c', 'e']:
        print("Filename doesn't include one of the following region codes: ['w', 'm', 'c', 'e'].")
        return
    try:
        with open(os.path.join("p01_files", filename), "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                try:
                    date = get_date_from_string(row[0])
                    if date is None:
                        print("File contains bad data. Please correct the data in the file and try again.")
                        return
                    quarter = int(row[1])
                    region = row[2]
                    amount = float(row[3])
                    sales_data.append({
                        "date": date,
                        "quarter": quarter,
                        "region": region,
                        "amount": amount
                    })
                except (ValueError, IndexError):
                    print("File contains bad data. Please correct the data in the file and try again.")
                    return
            imported_files.add(filename)
            print("Imported sales added to list.")
    except FileNotFoundError:
        print("No such file or directory.")

def save_sales(imported_files):
    with open(os.path.join("p01_files", "imported_files.txt"), "w") as file:
        for filename in imported_files:
            file.write(filename + "\n")
    print("Saved sales records.")

def main():
    sales_data = []
    imported_files = set()
    while True:
        print("\n1. Add sales")
        print("2. View sales")
        print("3. Import sales")
        print("4. Save sales")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_sales(sales_data)
        elif choice == "2":
            view_sales(sales_data)
        elif choice == "3":
            import_sales(sales_data, imported_files)
        elif choice == "4":
            save_sales(imported_files)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()