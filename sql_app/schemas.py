from typing import List
from pydantic import BaseModel, Json


class DatumBase(BaseModel):
    table_id: int
    sort_flag: bool
    table_datum: dict[str, List]
