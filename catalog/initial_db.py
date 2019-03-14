from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from db_structure import *

engine = create_engine('sqlite:///cars.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete CarBrandName if exisitng.
session.query(CarBrandName).delete()
# Delete CarName if exisitng.
session.query(CarName).delete()
# Delete User if exisitng.
session.query(SUser).delete()

# Create sample users data
User1 = SUser(name="Sruthi Kotha",
              email="sruthi.kotha1999@gmail.com"
              )
session.add(User1)
session.commit()
print ("Successfully Add First SUser")
# Create sample  car brands
Brand1 = CarBrandName(name="Mercedes Benz",
                      user_id=1)
session.add(Brand1)
session.commit()

Brand2 = CarBrandName(name="Audi",
                      user_id=1)
session.add(Brand2)
session.commit

Brand3 = CarBrandName(name="Hyundai",
                      user_id=1)
session.add(Brand3)
session.commit()

Brand4 = CarBrandName(name="BMW",
                      user_id=1)
session.add(Brand4)
session.commit()

Brand5 = CarBrandName(name="JAGUAR",
                      user_id=1)
session.add(Brand5)
session.commit()


# Populare a cars with models for testing
# Using different users for cars names year also
Name1 = CarName(name="Mercedes Benz GLS",
                year="2019",
                color="Black",
                engines="5461 cc,Petrol,577bhp@6000rpm",
                price="Rs. 85.67 Lakhs onwards",
                gearboxes="9-speed, Automatic, AWD",
                seeting="7 seater",
                steering="Power steering",
                date=datetime.datetime.now(),
                carbrandnameid=1,
                suser_id=1)
session.add(Name1)
session.commit()

Name2 = CarName(name="Audi A8",
                year="2013",
                color="Silver",
                engines="6299 cc,Petrol,493.5bhp@6200rpm",
                price="RS. 10.5 Crores",
                gearboxes="Automatic",
                seeting="4 seater",
                steering="Power,Adjustable",
                date=datetime.datetime.now(),
                carbrandnameid=2,
                suser_id=1)
session.add(Name2)
session.commit()

Name3 = CarName(name="Creta",
                year="2017",
                color="White",
                engines="1396 to 1591 cc,Petrol/Diesel",
                price="Rs. 9.6 Lakhs onwards",
                gearboxes="Automatic,Manual",
                seeting="5 seater",
                steering="Power steering",
                date=datetime.datetime.now(),
                carbrandnameid=3,
                suser_id=1)
session.add(Name3)
session.commit()

Name4 = CarName(name="BMW-M5",
                year="2015",
                color="Black",
                engines="4395cc,Petrol,575bhp@6000-6500rpm power",
                price="RS. 2.03 Crores",
                gearboxes="Automatic",
                seeting="5 seater",
                steering="Power steering,Adjustable",
                date=datetime.datetime.now(),
                carbrandnameid=4,
                suser_id=1)
session.add(Name4)
session.commit()

Name5 = CarName(name="JAGUAR XJ",
                year="2012",
                color="royal blue",
                engines="2993 cc, Diesel, 296 bhp @ 4000 rpm power",
                price="Rs. 1.1 Crores onwards",
                gearboxes="8-speed, Automatic, RWD",
                seeting="5 seater",
                steering="Power steering,Electrically Adjustable",
                date=datetime.datetime.now(),
                carbrandnameid=5,
                suser_id=1)
session.add(Name5)
session.commit()


print("Your cars database has been inserted!")
