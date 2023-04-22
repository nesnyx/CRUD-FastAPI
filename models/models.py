from sqlalchemy import Boolean, Column, Integer,String
from config.database import Base

class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True,index=True )
    name = Column(String)
    family_name = Column(String)
    science_name = Column(String)
    