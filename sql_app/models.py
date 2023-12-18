from sqlalchemy import Boolean, Column, Integer, JSON
from database import Base


class Datum(Base):
    __tablename__ = "datum"

    table_id = Column(Integer, primary_key=True, index=True)
    sort_flag = Column(Boolean, default=False)
    table_datum = Column(JSON)
