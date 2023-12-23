from typing import List
from pydantic import BaseModel


class DatumBase(BaseModel):
    table_name: str
    table_datum: dict[str, List[float]]
