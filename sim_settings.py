import numpy as np

#Function that relates marketing spend to customer quantity
def daily_customers(monthly_marketing_spend):
    if monthly_marketing_spend < 0:
        monthly_marketing_spend = 0
    monthly_customers = 100*monthly_marketing_spend**(1/3)+360
    rand_monthly_customers = np.random.normal(monthly_customers, (monthly_customers*0.1))
    return int(np.round(rand_monthly_customers/30,0))

#Demand curve for bakery items
def customer_demand(bread_price):
    base_demand = -1*bread_price+5
    rand_demand = int(np.round(np.random.normal(base_demand, 1),0))
    if rand_demand > 5:
        demand = 5
    elif rand_demand < 1:
        demand = 0
    else:
        demand = rand_demand
    return demand  
        
#Order generator that creates the day's customers, what they are ordering, and when they want it


#Expiration time