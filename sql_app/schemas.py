from pydantic import BaseModel, Json


class InqusitorBase(BaseModel):
    inqusitor_id: int
    inqusitor_name: str
    inqusitor_pass: str


class RelatumBase(BaseModel):
    table_id: int
    owner_id: int
    sort_flag: bool


class DatumBase(BaseModel):
    table_id: int
    table_datum: Json
