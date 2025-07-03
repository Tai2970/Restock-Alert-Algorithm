A lightweight supermarket restock alert algorithm using POS data.

How to Run:

1. Clone the repository:

git clone https://github.com/Tai2970/Restock-Alert-Algorithm.git
cd Restock-Alert-Algorithm

2. Make sure Python 3 is installed with the following packages:

pip install pandas tabulate

3. Run the program:

python main.py

This algorithm simulates shelf quantity using POS sales and predefined shelf rules. It identifies items that require restocking (ALERT) or reordering (ORDER), assigns confirmation codes, and generates a suggested order report. No external sensors or system integration are required.

Runtime and memory usage are also printed for performance evaluation.

Screenshots of output:

Runtime + Peak Memory + Alert Summary

ALERT Items Table

ORDER Items Table with Suggested Order column
