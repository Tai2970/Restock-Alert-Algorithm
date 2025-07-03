Restock Alert Algorithm
This project implements a lightweight restock alert system for supermarkets. The algorithm calculates shelf quantity changes using basic product information and simulated sales data, identifying when items need to be restocked (ALERT) or reordered entirely (ORDER). It requires no external sensors, relying only on point-of-sale behavior.

How to Run
You must have Python 3 installed. Required packages:
pandas
tabulate

Step 1: Install Dependencies
pip install pandas tabulate

Step 2: Run the Program
python main.py

Output
The script will simulate product sales and display:
Runtime and peak memory usage
Table of ALERT items (need restocking)
Table of ORDER items (fully out of stock, with suggested order)

Final Submission Tag
This submission is tagged as: v1.0-final
Please refer to that tag for the officially submitted version.
