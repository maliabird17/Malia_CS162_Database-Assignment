from datetime import date
from create import Offices, Agents, Listings, Homes, Buyers, Sales, Sellers, engine, Base
from sqlalchemy.orm import sessionmaker

# Before inserting data, start a session
Session = sessionmaker(bind=engine)
session = Session()

### DATA TO BE INSERTED ###
offices = [
    Offices(name = 'SF Real Estate'),
    Offices(name = 'London Real Estate'),
    Offices(name = 'Nice Real Estate'),
    Offices(name = 'Buenos Aires Real Estate')
]

homes = [
    Homes(beds=1, baths=1, address='22 Nathaniel', zipcode='94103', price_listed= 800000.00, date_listed=date(2021,9,21), month_listed=20219),
    Homes(beds=1, baths=1, address='73A Peter St', zipcode='06000', price_listed= 400000.00, date_listed=date(2021,9,28), month_listed=20219),
    Homes(beds=3, baths=3, address='100 Esmeralda', zipcode='24012', price_listed= 90000.00, date_listed=date(2021,9,24), month_listed=20219),
    Homes(beds=2, baths=1.5, address='5 Rue Delille', zipcode='10009', price_listed= 100000.00, date_listed=date(2021,1,1), month_listed=20211),
    Homes(beds=1, baths=1, address='16 Turk St', zipcode='94102', price_listed= 50000.00, date_listed=date(2021,6,12), month_listed=20216),
    Homes(beds=1, baths=1, address='110 Market St', zipcode='94101', price_listed= 2000000.00, date_listed=date(2021,12,25), month_listed=202112),
    Homes(beds=2, baths=2.5, address='33 Exmouth', zipcode='EC1R 4QL', price_listed= 570000.00, date_listed=date(2021,4,16), month_listed=20214, sold=True),
    Homes(beds=3, baths=1.5, address='91 Clerkenwell Rd', zipcode='EC1R 5BX', price_listed= 200000.00, date_listed=date(2021,1,17), month_listed=20211),
]

agents = [
    Agents(office_id=1, first_name = 'Dwight', last_name='Schrute', email='dwight@estates.com'),
    Agents(office_id=2, first_name = 'Jim', last_name='Halpert', email='jim@estates.com'),
    Agents(office_id=3, first_name = 'Michael', last_name='Scott',  email='michael@estates.com'),
    Agents(office_id=4, first_name = 'Pam', last_name='Beesly', email='pam@estates.com'),
    Agents(office_id=1, first_name = 'Angela', last_name='Martin', email='angela@estates.com'),
    Agents(office_id=1, first_name = 'Stanley', last_name='Hudson', email='stanley@estates.com'),
    Agents(office_id=2, first_name = 'Toby', last_name='Flenderson', email='toby@estates.com'),
    Agents(office_id=2, first_name = 'Kevin', last_name='Malone', email='kev@estates.com'),
    Agents(office_id=3, first_name = 'Andy', last_name='Bernard', email='andy@estates.com'),
    Agents(office_id=4, first_name = 'Erin', last_name='Hannon', email='erin@estates.com'),
    Agents(office_id=4, first_name = 'Oscar', last_name='Martinez', email='oscar@estates.com'),
    Agents(office_id=4, first_name = 'Phyllis', last_name='Vance', email='phylissvance@estates.com'),
    Agents(office_id=4, first_name = 'Meredith', last_name='Palmer', email='meredith@estates.com'),
    Agents(office_id=4, first_name = 'Kelly', last_name='Kapoor', email='kelly@estates.com'),
    Agents(office_id=4, first_name = 'Ryan', last_name='Howard', email='ryan@estates.com')
]

sellers = [
    Sellers(first_name = 'Malia', last_name='Bird', email='mbird@gmail.com'),
    Sellers(first_name = 'Finn', last_name='Macken', email='finnian@gmail.com'),
    Sellers(first_name = 'Leo', last_name='Ware', email='beware@gmail.com'),
    Sellers(first_name = 'Laura', last_name='Ruiz', email='lau@gmail.com'),
    Sellers(first_name = 'Gal', last_name='Rubin', email='rubs@gmail.com')
]

# Including edgecase where multiple listings are listed by the same agent 
listings = [
    Listings(home_id=1, agent_id=1, seller_id=4),
    Listings(home_id=2, agent_id=2, seller_id=1),
    Listings(home_id=3, agent_id=2, seller_id=1),
    Listings(home_id=4, agent_id=7, seller_id=1),
    Listings(home_id=5, agent_id=8, seller_id=3),
    Listings(home_id=6, agent_id=3, seller_id=3),
    Listings(home_id=7, agent_id=6, seller_id=4)
]

buyers = [
    Buyers(first_name = 'Toph', last_name='Beifong', email='metal_bender@gmail.com'),
    Buyers(first_name = 'Firelord', last_name='Ozai', email='crazy@yahoo.com'),
    Buyers(first_name = 'Avatar', last_name='Kyoshi',  email='kyoshi@gmail.com'),
    Buyers(first_name = 'Princess', last_name='Yue', email='moon@sky.com')
]

# adding all the data defined in the lists above
session.add_all(offices)
session.add_all(homes)
session.add_all(agents)
session.add_all(sellers)
session.add_all(listings)
session.add_all(buyers)
# Including one old sale (won't be included in this month's sales for checking query filters)
session.add(Sales(home_id=7, agent_id=13, buyer_id=1, price_sold=200000.00, date_sold=date(2022,9,21), month_sold=20222))
session.commit() # commit all database additions in this session


## Transaction Function 
# Referencing: https://riptutorial.com/sqlalchemy/example/6625/transactions and https://docs.sqlalchemy.org/en/20/core/connections.html 
def transaction(home_id, agent_id, buyer_id, price_sold):
    session = Session() # start individual session for a transaction
    # Try completing the sale data entry 
    try: 
        session.add(Sales(home_id=home_id, agent_id=agent_id, buyer_id=buyer_id, price_sold=price_sold))
        home_sold = session.query(Homes).get(home_id)
        home_sold.sold = True # update the sold status of the the specified home
        session.commit()
    # If something interupts or fails in the transaction, do not commit to database and rollback
    except: 
        session.rollback()
        raise

# Including purchases made by the same buyer and sold by the same agent
# Sold prices include price points in each commission range
transaction(1, 1, 2, 200000.00)
transaction(2, 1, 1, 400000.00)
transaction(3, 9, 2, 1100000.00)
transaction(4, 4, 2, 2000000.00)
transaction(5, 3, 3, 90000.00)
transaction(6, 7, 4, 60000.00)

