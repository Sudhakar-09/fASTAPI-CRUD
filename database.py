from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE='mysql+pymysql://root:root@localhost:3306/Blog_Application'
engine=create_engine(URL_DATABASE)
sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()
