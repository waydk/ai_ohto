from typing import List

import sqlalchemy as sa
from environs import Env
from gino import Gino
from sqlalchemy import Column, DateTime

env = Env()
env.read_env()

PG_HOST = env.str("PG_HOST")
PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
DATABASE = env.str("DATABASE")

POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{DATABASE}"

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())
