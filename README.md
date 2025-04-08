# bakery_sim
Business transaction simulator for a bakery. (python, SQL)

This project uses python and embeded SQL statments to simulate the business transactions that happen at a fictional bakery. After the simulation is run, the databases are written to excel files and a text document is generated that has some KPI's. The user can change the input variables to see how it affects bakery operations.

sim.py: This is the main file that runs the program. Here, the user updates variables to change the sim. Databases are created, the starting conditions are set, a loop simulates daily bakery operation, and finally a report is generated.

#################
# user inputs
db_name = 'test'

sim_days = 59

monthly_marketing_spend = 1200.00 #dollars

bread_price = 4.50 #dollars

bread_cost = 1.50 #dollars

ingredient_buy_setpoint = 5 #available batches of ingredients

ingredient_buy_qty = 15 #batches of ingredients

bake_batch_setpoint = 20 #available loaves

starting_account_balance = 10000.00

rent_expense = 1500.00

payroll_expense = 700.00
#################


create_db.py: This file stores the function that creates the databases. There are four databases: sale, ingredients, bread, and bank.

transactions.py: this file stores the business transaction functions. Functions include: customer_purchase, bake_batch, purchase_ingredients, pay_bill, and deposit_revenue.

operations.py: This file stores functions that do practical things with the databases like check quantities or update values. Functions include: expired_batch, finished_bread, bread_check, ingredient_check, ingredient_delivery, purchase_ingredient_check, credit_expense, bread_sold, and account_balance.

order_generator.py: This file uses mathmatic functions and random number generators to simulate customer behavior. This is where the program decides how many customers will show up at the store, when they they will show up at the store, and how much bread they want to buy.

report.py: This file generates the text that shows the KPI's for the simulation.

Sim Name: test

    Sim Days: 59

    Monthly Marketing Spend: $1200.00

    Bread Cost: $1.50

    Bread Price: $4.50

    Ingredient Buy Setpoint: 5

    Ingredient Buy Qty: 15

    Bake Batch Setpoint: 20

    Starting Account Balance: $10000.00

    Rent Expense: $1500.00

    Payroll Expense: $700.00
 
    ------------------------------------------

    Total Revenue: $32710.50

    Total Expense: $22250.00

    Net Income: $10460.50

    Profit Margin: 32.0%

    Final Account Balance: $20460.50

    Total Credit Expense: $0.00

    ------------------------------------------

    Average Daily Customers: 128

    Average Order Size: 1.2

    Average Missed Orders: 27.3

    Used Oven Capacity: 49.0%

    Average Expired Loaves: 0.0
    