from create import Offices, Homes, Agents, Listings, Buyers, Sellers, Sales, Commission, engine, Base
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, insert
from sqlalchemy.schema import Index

# Start the session to query data into the database
Session = sessionmaker(bind=engine)
session = Session()

# Used to print results more legibly
def print_result(outputs):
    for output in outputs:
        print(output)


### QUESTION 1: Find the top 5 offices with the most sales for that month
Index('idx_offices_agents', Agents.agent_id, Agents.office_id) # composite index to group agents by office
# Top sales by number of sales made (ignoring price of sale)
top_office_sale_counts = session.query(
    Offices.name, func.count(Sales.sale_id)
    ).\
        join(Agents, Sales.agent_id == Agents.agent_id).\
        join(Offices, Agents.office_id == Offices.office_id).\
        group_by(Offices.office_id).\
        order_by(func.count(Sales.sale_id).desc()).\
        limit(5)

print('Question 1 (part 1): Top 5 offices this month, by number of sales:')
print_result(top_office_sale_counts)
print('--------------------------\n')

# Top sales by account of all sales (highlighting magnitude of sales made)
top_office_sale_amount = session.query(
    Offices.name, func.sum(Sales.price_sold)
    ).\
        join(Agents, Sales.agent_id == Agents.agent_id).\
        join(Offices, Agents.office_id == Offices.office_id).\
        group_by(Offices.office_id).\
        order_by(func.sum(Sales.price_sold).desc()).\
        limit(5)

print('Question 1 (part 2): Top 5 offices this month, by amount earned:')
print_result(top_office_sale_amount)
print('--------------------------\n')

### QUESTION 1 SANITY CHECK ###
# This wouldn't be included for the real estate company's summary information 
# and would be too large an output with reallife data (imagine hundreds of sales)
# However, it is useful to check our results from above for the purpose of this assignment. 
validate_top_offices = session.query(
    Offices.name, Sales.sale_id, Sales.price_sold, Agents.agent_id, Agents.office_id
    ).\
        join(Agents, Offices.office_id == Agents.office_id).\
        join(Sales, Agents.agent_id == Sales.agent_id).\
        order_by(Agents.office_id).\
        all()

print('Expanding all office sales data to check question 1:')
print_result(validate_top_offices)
print('==========================\n')


### QUESTION 2: Find the top 5 estate agents who have sold the most for the month
Index('idx_agent_groups', Sales.agent_id) # index to group same agents together 
top_agents= session.query(
    Agents.first_name, Agents.last_name, func.sum(Sales.price_sold), Agents.email
    ).\
        join(Agents, Sales.agent_id == Agents.agent_id).\
        group_by(Agents.agent_id).\
        order_by(func.sum(Sales.price_sold).desc()).\
        limit(5)

print('Question 2: Top 5 agents this month, by their total amount in sales:')
print_result(top_agents)
print('--------------------------\n')

### QUESTION 2 SANITY CHECK ###
# Again, just checking our results above but not realistic for the scenario. 
validate_top_agents = session.query(
    Sales.sale_id, Agents.first_name, Agents.last_name, Sales.price_sold
    ).\
        join(Sales, Agents.agent_id == Sales.agent_id).\
        order_by(Sales.sale_id).\
        order_by(Agents.agent_id).\
        all()

print('Expanding all agent sales data to check question 2:')
print_result(validate_top_agents)
print('==========================\n')


### QUESTION 3: Calculate the commission that each estate agent must receive and store the results in a separate table.
# referencing INSERT ... FROM SELECT documentation: https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert
# Select all data from other tables to populate the new Commission Table
session.query(Commission).delete() 
selection_agent_commissions= session.query(
    Agents.agent_id, Agents.first_name, Agents.last_name, Agents.email, func.sum(Sales.commission)
    ).\
        join(Agents, Sales.agent_id == Agents.agent_id).\
        group_by(Agents.agent_id).\
        order_by(func.sum(Sales.commission).desc()).\
        filter(Sales.month_sold == int(str(datetime.date.today().year) + str(datetime.date.today().month)))

#Insert our selection into the table
insertion = insert(Commission).from_select(['commission_id', 'first_name', 'last_name', 'email', 'commission_amount'], selection_agent_commissions)
session.execute(insertion)
session.commit()

# Query all data (except IDs) from the commission table to print
commission_data = session.query(
    Commission.first_name, Commission.last_name, Commission.email, Commission.commission_amount)

print('Question 3: Commission data (now stored in a new table):')
print_result(commission_data)
print('--------------------------\n')

### QUESTION 3 SANITY CHECK ###
# Check to make sure only this month is included in the commission table (only one old sale is in the datebase)
session.query(Commission).delete()
# monthly filter is removed
validate_agent_commissions= session.query(
    Agents.agent_id, Agents.first_name, Agents.last_name, Agents.email, func.sum(Sales.commission)
    ).\
        join(Agents, Sales.agent_id == Agents.agent_id).\
        group_by(Agents.agent_id).\
        order_by(func.sum(Sales.commission).desc())

#Insert our selection into the table
insertion = insert(Commission).from_select(['commission_id', 'first_name', 'last_name', 'email', 'commission_amount'], selection_agent_commissions)
session.execute(insertion)
session.commit()

# Query all data (except IDs) from the commission table to print
commission_data = session.query(
    Commission.first_name, Commission.last_name, Commission.email, Commission.commission_amount)

print('Commission data across all months (should have more entries and commission than above):')
print_result(validate_agent_commissions)
print('==========================\n')


### QUESTION 4: For all houses that were sold that month, calculate the average number of days on the market.
days_on_market = session.query(
    Homes.address,  func.julianday(Sales.date_sold) - func.julianday(Homes.date_listed)
    ).\
        join(Sales, Homes.home_id == Sales.home_id).\
        filter(Sales.month_sold == int(str(datetime.date.today().year) + str(datetime.date.today().month)))

print('Question 4: Days on the market for home sales this month:')
print_result(days_on_market)
print('----------------------------\n')

### QUESTION 4 SANITY CHECK ###
# Check only this month's sales are returned (only one old sale is in the datebase)
validate_days_on_market = session.query(
    Homes.address,  func.julianday(Sales.date_sold) - func.julianday(Homes.date_listed)
    ).\
        join(Sales, Homes.home_id == Sales.home_id)

print('Checking days on the market without filtering for this month:')
print_result(validate_days_on_market)
print('=============================\n')


### QUESTION 5: For all houses that were sold that month, calculate the average selling price. 
average_selling_price = session.query(
    func.round(func.avg(Sales.price_sold), 2)
    ).\
        filter(Sales.month_sold == int(str(datetime.date.today().year) + str(datetime.date.today().month)))

print('Question 5: Average selling price for homes sold this month:')
print_result(average_selling_price)
print('----------------------------\n')

### QUESTION 5 SANITY CHECK ###
# Check only this month's sales were returned above (only one old sale is in the datebase)
validate_average_selling_price = session.query(func.round(func.avg(Sales.price_sold), 2))

all_selling_prices = session.query(
    Homes.address, Sales.price_sold
    ).\
        join(Sales, Homes.home_id == Sales.home_id).\
        filter(Sales.month_sold == int(str(datetime.date.today().year) + str(datetime.date.today().month)))

print('All costs of houses sold this month for a sanity-check of the average:')
print_result(all_selling_prices)
print('----------------------------\n')

print('Checking average selling price across all months (this should be different from above if filter worked):')
print_result(validate_average_selling_price)
print('=============================\n')