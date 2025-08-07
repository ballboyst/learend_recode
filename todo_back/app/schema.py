# このファイルはリクエストのデータ構造の定義とシリアライズについて責任を持つ
from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: str

