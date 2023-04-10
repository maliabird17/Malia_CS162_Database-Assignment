# CS162 Database Assignment
**Malia Bird, Spring Semester CS162**

TO DO: 
- Commenting!!!
- Check everything runs correctly
- Indexes


## Getting Started
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
```

## Unit Testing 
``` 
python3 testing.py
```

Additional checks were also performed in the `query_data.py` file to do sanity checks on the query results. 

## Database Design & Data Normalization

Database design visualized in an ER diagram. Blocks correspond to tables, arrows indicate relationships (implemented through foeirgn keys), and bolded attributes of tables are primary keys. The green listings table is distinct because it is a joining/linkage table of all primary keys. 

A joining table was implemented for listings to allow for many-to-many relationships between homes, agents, and sellers. It is plausible that one seller is listing multiple properties, that multiple agents in charge of a single listing, and that a home is listed many times or in different offices. Instead of including entries for the same home, but with different combinations of agents and sellers, in the `Homes` table, most of that redundancy can be moved into the bridging table, where minimal information is stored -- just the specific combination of home, agent, and seller which describes one version of the listing.

![ER image](/ER_database_diagram.jpg)

1. **First Normal Form: Each row should be uniquely identifiable and columns should be of the same datatype.** 
    - This is taken care of using SQLAlchemy's column datatype specifications and by specifying primary keys for the IDs of each table (which are also unique). 

2. **Second Normal Form: All table attributes depend on the key.**
     - This is achieved by splitting up all data types according to their dependencies and what they describe. All major actors (what we would call agents in `#multipleagents`), including actors which encompass many other actors (like how an office includes many agents) form their own table. That way, attributes specific to an actor can be attached to just one appropriate table, and foreign keys can be used to make connections. 
     
     - For example, rather than including an agent's information (name, email) with a listing, an agent's information is included in an agent-specific table and agent's ID are connected to a listing. The same is done with home, office, buyer, and seller's information. 


3. **Third Normal Form: All columns can be determined from the table key, and no other columns.**
    - This was considered when excluding `office_id` from the `Homes` and `Sales` tables. This might have been practical for queries which are interested in office-specific data; however, the `office_id` could always be determined by looking at the `agent_id`, and therefore, the office column would not be solely determined by the table's key. Instead, we can easily join office, agent, and sales/listings tables in queries to indirectly acquire office-specific information and continue to satisfy third normal form. 

## HC Appendix
`#variables`: Variable types and their relationships were fundamental while constructing my database tables in SQLAlchemy. The datatype of each column (integer, text, boolean, date) needed to be specified. More importantly, the relationships between variables needed to be considered while designing the database to satisfy second normal form and when writing foreign key relationships. Primary keys become independent variables to which all variables in their table are dependent upon and foreign keys represent dependency across tables. 
