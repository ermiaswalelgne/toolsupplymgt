# Supply Management System Tool

Welcome to the Supply Management System Tool repository. This tool performs a variety of supply management operations based on data provided in CSV files. The repository includes three primary operations that are executed using the corresponding CSV files within the `data` directory. The main functionalities are as follows:

1. **Total Order Cost Calculation and Corresponding Order ID Retrieval:**
   This operation calculates the total order cost in euros and retrieves the corresponding order ID. The results are then saved to a new CSV file named `order_prices.csv` within the `results` folder.

2. **Customer List Retrieval for Each Product ID:**
   For each product ID, this operation fetches the list of customers who have purchased the given product. The outcome is saved in a new CSV file called `product_customers.csv`.

3. **Customer Ranking by Total Amount Spent:**
   This operation filters customer IDs based on the total amount spent on purchased products and ranks customers in descending order by their total euros spent. The computed result is stored in the `customer_ranking.csv` file.

## Code Structure

The original data is organized under the `data` folder. Processed CSV files are stored in the `data/results` folder.

To execute the program, you can use command-line arguments as follows:
- To process product orders with total prices: `python3 toolsupplymgt.py -o`
- To execute all three functionalities: `python3 toolsupplymgt.py -o -c -r`

Please note that the execution results can be found in the `data/results` folder in CSV format.

This version represents an initial release, with more enhancements and improvements planned for the future.
