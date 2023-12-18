from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from database import Base


class Inqusitor(Base):
    __tablename__ = "inqusitor"

    inqusitor_id = Column(Integer, primary_key=True, index=True)
    inqusitor_name = Column(String, unique=True, index=True)
    inqusitor_pass = Column(String)


class Relatum(Base):
    __tablename__ = "relatum"

    table_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("inqusitor.inqusitor_id"), index=True)
    sort_flag = Column(Boolean, default=False, index=True)


class Datum(Base):
    __tablename__ = "datum"

    table_id = Column(Integer, ForeignKey("relatum.table_id"), primary_key=True, index=True)
    table_datum = Column(JSON)
