#Generate timeline of the day's customer transactions

#Add product expirations to timeline

#For each customer order
##if item is in stock
###reccord sale
###check production setpoint
###if setpoint is triggered
####if ingredients are on-hand
#####schedule oven time and inventory transaction
##else
###record missed sale

#End of the day
##if inventory setpoints are triggered
###issue new P.O.
##handle banking transactions