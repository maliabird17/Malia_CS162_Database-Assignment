import unittest
from create import Offices, Homes, Agents, Listings, Buyers, Sellers, Sales, Commission, engine, Base
from sqlalchemy import create_engine, func, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import date
import query_data
import insert_data


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
    
    def test_update_consistency_across_tables(self):
        """
        If we update a row which is connecting to other tables via foreign keys, those rows should also be updated.
        """
        all_data = [
            Homes(beds=1, baths=1, address='22 Nathaniel', zipcode='94103', price_listed= 800000.00, date_listed=date(2021,9,21), month_listed=20219),
            Agents(office_id=1, first_name = 'Dwight', last_name='Schrute', email='dwight@estates.com'),
            Sellers(first_name = 'Malia', last_name='Bird', email='mbird@gmail.com'),
            Listings(home_id=1, agent_id=1, seller_id=1)
        ]

        self.session.add_all(all_data)
        self.session.commit()
        id_before = self.session.query(Listings.listing_id).all()
        
        self.session.query(Homes).filter(Homes.home_id == 1).update({'home_id': 2})
        self.session.commit()
        id_after = self.session.query(Listings.home_id).all()

        self.assertNotEqual(id_before, id_after)


if __name__ == '__main__':
    unittest.main()




