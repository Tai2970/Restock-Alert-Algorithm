import time
import tracemalloc
import random
import pandas as pd
from tabulate import tabulate

# Step 1: Define Item Class
class Item:
    def __init__(self, item_id, name, case_size, display_quantity, unit_width, aisle, level, side):
        self.item_id = item_id
        self.name = name
        self.case_size = case_size
        self.display_quantity = display_quantity
        self.unit_width = unit_width  # cm
        self.aisle = aisle
        self.level = level
        self.side = side  # 'A' = Left, 'B' = Right
        self.position = f"Aisle {aisle} - Level {level} - Side {side}"

        self.shelf_capacity = case_size * display_quantity
        self.threshold = self.shelf_capacity - case_size
        self.current_quantity = self.shelf_capacity
        self.shelf_space_used = self.shelf_capacity * self.unit_width

        self.alert_confirmed = False
        self.status = "OK"
        self.confirmation_code = None

# Step 2: Helper Function
def get_shelf_side(side):
    return "Left" if side == 'A' else "Right"

# Step 3: Generate Product List
product_list = []
for i in range(1, 101):
    aisle = random.randint(1, 5)
    level = random.randint(1, 5)
    side = random.choice(['A', 'B'])

    item = Item(
        item_id=f"P{i:03}",
        name=f"Item {i}",
        case_size=random.choice([6, 12, 24]),
        display_quantity=random.choice([2, 3, 4]),
        unit_width=random.uniform(4.0, 10.0),
        aisle=aisle,
        level=level,
        side=side
    )
    product_list.append(item)

# Step 4: Simulate Sales
sales_data = []
for _ in range(1000):
    item = random.choice(product_list)
    quantity = random.randint(1, 5)
    sales_data.append((item.item_id, quantity))

# Step 5: Alert Logic
def find_item_by_id(item_id):
    return next((i for i in product_list if i.item_id == item_id), None)

def generate_code(item):
    return f"C-{item.item_id[-3:]}"

def check_alert(item):
    if item.current_quantity == 0:
        item.status = "ORDER"
        item.confirmation_code = None
    elif item.current_quantity <= item.threshold and item.current_quantity <= 0.5 * item.shelf_capacity:
        item.status = "ALERT"
        item.confirmation_code = generate_code(item)
    else:
        item.status = "OK"
        item.confirmation_code = None

def update_sales(sales_data):
    for item_id, qty in sales_data:
        item = find_item_by_id(item_id)
        if item:
            item.current_quantity = max(0, item.current_quantity - qty)
            check_alert(item)

# Step 6: Run + Measure
start = time.time()
tracemalloc.start()

update_sales(sales_data)

end = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Runtime: {end - start:.4f} seconds")
print(f"Peak Memory: {peak / 1024:.2f} KB")

# Step 7: Summarize Alerts
summary = {"ALERT": 0, "ORDER": 0, "OK": 0}
for item in product_list:
    summary[item.status] += 1
print("Alert Summary:", summary)

# Step 8: Build DataFrames
full_df = pd.DataFrame([{
    "Item ID": item.item_id,
    "Name": item.name,
    "Aisle": item.aisle,
    "Level": item.level,
    "Side": get_shelf_side(item.side),
    "Position": item.position,
    "Shelf Capacity": item.shelf_capacity,
    "Current Qty": item.current_quantity,
    "Threshold": item.threshold,
    "Unit Width (cm)": round(item.unit_width, 2),
    "Shelf Space Used (cm)": round(item.shelf_space_used, 2),
    "Status": item.status,
    "Confirmation Code": item.confirmation_code
} for item in product_list])

# ALERT Table
alert_df = full_df[(full_df["Status"] == "ALERT") & (full_df["Confirmation Code"].notnull())]
alert_df = alert_df.sort_values(by="Current Qty").reset_index(drop=True)

# ORDER Table
order_df = full_df[full_df["Status"] == "ORDER"].copy().reset_index(drop=True)
order_df.loc[:, "Suggested Order (cases)"] = order_df["Shelf Capacity"] // product_list[0].case_size

# Step 9: Display with Tabulate
from tabulate import tabulate

print("\n" + "="*80)
print("ALERT ITEMS (NEED RESTOCK)")
print("="*80)
print(tabulate(alert_df.head(20), headers="keys", showindex=True, tablefmt="fancy_grid"))

print("\n" + "="*80)
print("ORDER REPORT (ITEMS FULLY OUT OF STOCK)")
print("="*80)
print(tabulate(order_df.head(20), headers="keys", showindex=True, tablefmt="fancy_grid"))
