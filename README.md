

#  A simple tool for supply managment system

This is tool supply company management system performs the following three operations based on using the CSV data as a source:
- 1: Calculate the total order cost with euro and save it along with the order id.
   It then saves the result to a file called order_prices.csv under the results folder file.

- 2:  For each product id, it fetches the list of customers who have purchased a given product.
    And save the result to a  product_customers.csv file.

- 3: It filter customer id with the total amount spent on purchased products, it than rank the customer in descending order by total_euros
     The result of this computation is saved into the customer_ranking.csv file.



# Code structure 
Raw data are stored under the data folder. Processed CSV files will be stored inside the data/results folder.
 
 To run the program you can use a command-line argument as follows, for instance  
 > python3 toolsupplymgt.py -o true -- > [mandatory] this will Processing product order with total price 
 > python3 toolsupplymgt.py -o true -c true -r true -- >  this will execute all three functionalities
 
 Note: the result of the execution can be found data/results folder in a CSV file.

 This is the first version and more improvements will come soon...