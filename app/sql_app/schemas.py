# pydantic model은 "스키마"(유효한 데이터 모양)을 어느 정도 정의한다.
# 데이터 생성(Create) 및 API 요청 처리

from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime


class ItemBase(BaseModel):
    
    name: str

class ItemCreate(ItemBase):

    pass

class Item(ItemBase):
  
    id: int

    class Config:
        orm_mode = True


