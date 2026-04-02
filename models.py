from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    income = Column(Integer)
    expenses = Column(Integer)

    goal = Column(String)
    target_amount = Column(Integer)

    savings = Column(Integer)

    investment_type = Column(String)   # e.g. "SIP, Stocks"
    investment_amount = Column(Integer)