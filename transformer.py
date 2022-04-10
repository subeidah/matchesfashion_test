from typing import (
    List,
    Tuple,
)

import pandas as pd
import seaborn as sns
import matplotlib as plt


class Transformer:

    def __init__(self):
        self

    def read_orders(self) -> pd.DataFrame:
        orders = pd.read_csv('orders.csv', header=0)
       # print(orders)
        return orders

    def enrich_orders(self, orders: pd.DataFrame, col_name: str, value: List[str]) -> pd.DataFrame:
        """
        Adds a column to the data frame

        Args:
            orders (pd.Dataframe): The dataframe to be enriched
            col_name (str): Name of the new enriched column
            value (List[str]): Data to go into the new column

        Returns:
            The enriched dataframe
        """
        
        #adding column to dataframe based on input
        
        orders[col_name] = value
       # print(orders)
        return orders     


    def split_customers(self, orders: pd.DataFrame, threshold: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits customers into two groups based on a threshold

        Args:
            orders (pd.DataFrame): The dataframe to be split
            threshold (int): Value to split the customer base on

        Returns:
            Tuple containing the split dataframes
        """
    
        low_spending_customers, high_spending_customers = [x for _, x in orders.groupby(orders['amount'] >= threshold)]
        #print(low_spending_customers, high_spending_customers)
        return(low_spending_customers, high_spending_customers)
    
        concatenated = pd.concat([low_spending_customers.assign(dataset='LSC'), 
                                  high_spending_customers.assign(dataset='HSC')])
        
        sns.scatterplot(x='customer', y='amount', data=concatenated,
                style='dataset').set_title('Low vs High spending customers')
        
        plt.show()

      
# ******************************************    
# ****************BONUS TASK****************
# ****************************************** 

#creating global variable for dataframe
transformer = Transformer()
orders = transformer.read_orders()

#Question 1: Which customer placed the highest order amount?

#first attempt but printing more data than i was looking for- only wanting customer name

#print("Customer with highest order amount is :\n" ,orders.loc[orders['amount'].idxmax()])

#finding highest value in amount column
highest_order = orders['amount'].max()
#finding which customer name this corresponds to
customer_HO= orders[orders['amount']==highest_order]['customer']
print("Customer with the highest order amount is :", customer_HO)



#Question 2: Which customer placed the lowest order amount?

lowest_order = orders['amount'].min()
customer_LO= orders[orders['amount']==lowest_order]['customer']
print("Customer with lowest order amount is :", customer_LO)

#Question 3: What was the average order amount across all customers?

print("The average order amount across all customers is:", orders['amount'].mean())

#Question 4: Which customer placed the earliest order?

date = orders['date'].min()
customer_EO= orders[orders['date']==date]['customer']
print("Customer with earliest order is :", customer_EO)

#Question 5: In which month did most of the orders happen (the year can be ignored)?

#checking datatype for date column
#print(orders.dtypes)

#changing from object to datetime
orders['date'] = pd.to_datetime(orders['date'])

#creating new month column with column name instead of int
orders['month'] = pd.to_datetime(orders['date'], format='%m').dt.month_name()

#finding most common month that orders were placed.
month = orders['month'].mode()
print("The month with the most orders was:", month)



if __name__ == '__main__':
    transformer = Transformer()
    data = transformer.read_orders()

    countries = ['GBR', 'AUS', 'USA', 'GBR', 'RUS', 'GBR', 'KOR', 'NZ']
    data = transformer.enrich_orders(data, 'Country', countries)

    threshold = 900 
    low_spending_customers, high_spending_customers = transformer.split_customers(data, threshold)
