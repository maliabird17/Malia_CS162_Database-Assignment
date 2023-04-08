import sqlalchemy
import datetime
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Connect to database, with echo=True to follow requests
engine = create_engine('sqlite:///real_estate.db', echo=True)
engine.connect()

# provide the base for declarative method to create tables
Base = declarative_base()

### Offices table, this is mostly to help query office-specific information, which is commonly done
class Offices(Base):
    __tablename__ = 'offices'
    office_id = Column(Integer, primary_key = True)
    name = Column(Text)
    agents = relationship("Agents")

    def __repr__(self):
        return "<Offices(ID={}, Name={})>".format(self.office_id, self.name)


### Information dependent on the home listed
class Homes(Base):
    __tablename__ = 'homes'
    home_id = Column(Integer, primary_key=True)
    beds = Column(Integer)
    baths = Column(Float) # We can have half baths so allow for 1 decimal place
    address = Column(Text)
    zipcode = Column(Text)
    price_listed = Column(Float)
    date_listed = Column(DateTime)
    month_listed = Column(Integer)
    sold = Column(Boolean, default=False)
    listings = relationship("Listings")
    sales = relationship("Sales")
    
    def __repr__(self):
        return "<Home(ID={}, Address={}, Date Listed={}, Sold={})>".format(self.home_id, self.address, self.date_listed, self.sold)

### Agent table
class Agents(Base):
    __tablename__ = 'agents'
    agent_id = Column(Integer, primary_key = True)
    office_id = Column(Integer, ForeignKey('offices.office_id'))
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    listings = relationship("Listings")
    sales = relationship("Sales")

    def __repr__(self):
        return "<Agents(ID ={}, Office = {}, First Name ={}, Last Name ={})".format(self.agent_id, self.office_id, self.first_name, self.last_name)
    

### Sellers (individuals selling a property) table
class Sellers(Base):
    __tablename__ = 'sellers'
    seller_id = Column(Integer, primary_key = True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    listing = relationship("Listings")

    def __repr__(self):
        return "<Sellers(ID ={}, First Name ={}, Last Name ={})".format(self.seller_id, self.first_name, self.last_name)


### LINK TABLE ##
### Inspired by e-commerce anecdote from session 15 @ 25:00 
### Connecting Homes to their listing agent and seller
class Listings(Base):
    __tablename__ = 'listings'
    listing_id = Column(Integer, primary_key = True)
    home_id = Column(Integer, ForeignKey('homes.home_id'))
    agent_id = Column(Integer, ForeignKey('agents.agent_id'))
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'))

    
    
### Buyers (individuals purchasing property) table
class Buyers(Base):
    __tablename__ = 'buyers'
    buyer_id = Column(Integer, primary_key = True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    sales = relationship("Sales")

    def __repr__(self):
        return "<Buyers(ID ={}, First Name ={}, Last Name ={})".format(self.buyer_id, self.first_name, self.last_name)


# Function used to calculate the commission, based off the price a property is sold for
def calculate_commission(context):
    price_sold = context.get_current_parameters()["price_sold"]

    if price_sold < 100000.00:
        return price_sold*0.1
    if price_sold <= 200000.00:
        return price_sold*0.075
    if price_sold <= 500000.00:
        return price_sold*0.06
    if price_sold <= 1000000.00:
        return price_sold*0.05
    else:
        return price_sold*0.04

### Sales information recording sale information and linking to the property, buyer & agent involved
class Sales(Base):
    __tablename__ = 'sales'
    sale_id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey('homes.home_id'))
    agent_id = Column(Integer, ForeignKey('agents.agent_id'))
    buyer_id = Column(Integer, ForeignKey('buyers.buyer_id'))
    price_sold = Column(Float)
    date_sold = Column(DateTime, default=datetime.date.today())
    month_sold = Column(Integer, default=int(str(datetime.date.today().year) + str(datetime.date.today().month)))
    commission = Column(Float, default=calculate_commission)

    def __repr__(self):
        return "<Sales(ID ={}, Price Sold ={}, Commission ={})".format(self.sale_id, self.price_sold, self.commission)

# To handle question 4 
class Commission(Base):
    __tablename__ = 'commission'
    commission_id = Column(Integer, primary_key = True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    commission_amount = Column(Float)

# create all the tables defined above 
Base.metadata.create_all(bind=engine)