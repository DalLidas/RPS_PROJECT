from sqlalchemy import Boolean, Column, Integer, JSON, String
from database import Base


class Datum(Base):
    __tablename__ = "datum"

    table_id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)
    sort_flag = Column(Boolean, default=False)
    table_datum = Column(JSON)
