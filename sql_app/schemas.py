from typing import List
from pydantic import BaseModel


class DatumBase(BaseModel):
    sort_flag: bool
    table_name: str
    table_datum: dict[str, List[float]]
