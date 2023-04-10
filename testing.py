import unittest
from create import Offices, Homes, Agents, Listings, Buyers, Sellers, Sales, Commission, engine, Base
from sqlalchemy import create_engine, func, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import date
from insert_data import transaction

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.engine.connect()
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_database(self):
        '''
        Pseudo-Integration testing: testing high level interactions with the database 
        that are not bite-sized unit tests (those follow) or edge-cases. These would be
        true integration tests if we imagined the database was connected to an app, and 
        we test their interaction, but still these are more high-level than unit-tests. 
        
        Testing interactions with the database, specifically: 
            - Tables are initialized to be empty
            - Information is stored when added to the database
            - The correct information is returned from the database
            - Deletions are reflected in the database
            - Data remains consistent between queries (number of data rows is as expected)
        '''
        # Tables are initialized to be empty
        rows = self.session.query(func.count(Homes.home_id)).scalar()
        self.assertEqual(rows, 0, "Table is not emoty at initialization")

        home = Homes(beds=1, baths=1, address='22 Nathaniel', zipcode='94103', price_listed= 800000.00, date_listed=date(2021,9,21), month_listed=20219)
        self.session.add(home)
        self.session.commit()

        # Information is stored when added to the database
        rows = self.session.query(func.count(Homes.home_id)).scalar()
        self.assertEqual(rows, 1, "Information is not all stored to the database")

        # The correct information is returned from the database
        self.assertEqual(home.beds, 1, "Incorrect information is stored to the database")

        # Deletions are reflected in the database
        self.session.query(Homes).delete()
        self.session.commit()
        rows_after_delete = self.session.query(func.count(Homes.home_id)).scalar()
        self.assertEqual(rows_after_delete, 0, "Information is not correctly cleared from the database")

        # Data remains consistent between queries (number of data rows is as expected)
        home = Homes(beds=1, baths=1, address='22 Nathaniel', zipcode='94103', price_listed= 800000.00, date_listed=date(2021,9,21), month_listed=20219)
        self.session.add(home)
        self.session.commit()
        rows_later = self.session.query(func.count(Homes.home_id)).scalar()
        self.assertEqual(rows, rows_later, "Inconsistent amount of data between queries")
    
    def test_homes(self):
        """
        Test home information is accurately stored to database, with the right data type. 
        """
        home = Homes(beds=1, baths=1.5, address='22 Nathaniel', zipcode='94103', price_listed= 800000.00, date_listed=date(2021,9,21), month_listed=20219)
        self.session.add(home)
        self.session.commit()

        self.assertEqual(home.home_id, int(1))
        self.assertEqual(home.beds, int(1))
        self.assertEqual(home.baths, float(1.5))
        self.assertEqual(home.address, '22 Nathaniel')
        self.assertEqual(home.zipcode, '94103')
        self.assertEqual(home.price_listed,float(800000.00))
        self.assertEqual(home.date_listed, datetime.datetime(2021,9,21,0,0))
        self.assertEqual(home.month_listed, int(20219))
        self.assertEqual(home.sold, False)

    def test_agents(self):
        """
        Testing the agent table is populated correctly. 
        """
        agent = Agents(office_id=1, first_name = 'Dwight', last_name='Schrute', email='dwight@estates.com')
        self.session.add(agent)
        self.session.commit()

        self.assertEqual(agent.agent_id, 1)
        self.assertEqual(agent.office_id, 1)
        self.assertEqual(agent.first_name, 'Dwight')
        self.assertEqual(agent.last_name, 'Schrute')
        self.assertEqual(agent.email, 'dwight@estates.com')

    def test_sellers(self):
        """
        Testing the sellers table is populated correctly. 
        """
        seller = Sellers(first_name = 'Malia', last_name='Bird', email='mbird@gmail.com')
        self.session.add(seller)
        self.session.commit()

        self.assertEqual(seller.seller_id, 1)
        self.assertEqual(seller.first_name, 'Malia')
        self.assertEqual(seller.last_name, 'Bird')
        self.assertEqual(seller.email, 'mbird@gmail.com')

    def test_listings(self):
        """
        Testing the listings table is populated correctly. 
        """
        listing = Listings(home_id=1, agent_id=1, seller_id=1)
        self.session.add(listing)
        self.session.commit()

        self.assertEqual(listing.listing_id, 1)
        self.assertEqual(listing.home_id, 1)
        self.assertEqual(listing.agent_id, 1)
        self.assertEqual(listing.seller_id, 1)

    def test_buyers(self):
        """
        Testing the buyers table is populated correctly. 
        """
        buyer = Buyers(first_name = 'Toph', last_name='Beifong', email='metal_bender@gmail.com')
        self.session.add(buyer)
        self.session.commit()

        self.assertEqual(buyer.buyer_id, 1)
        self.assertEqual(buyer.first_name, 'Toph')
        self.assertEqual(buyer.last_name, 'Beifong')
        self.assertEqual(buyer.email, 'metal_bender@gmail.com')

    def test_transactions(self):
        """
        Test transactions do not commit when an exception is raised
        (in this case by a bad input).
        """

        transaction(1, 'WRONG INPUT', 1, 80000.00)
        rows = self.session.query(func.count(Sales.sale_id)).scalar()
        self.assertEqual(rows, 0)

if __name__ == '__main__':
    unittest.main()




