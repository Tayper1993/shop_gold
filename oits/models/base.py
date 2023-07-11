from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


Base = declarative_base()
engine = create_engine('postgresql+psycopg2://scot:tiger@localhost:5432/mydatabase')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(engine)
