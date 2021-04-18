from sqlalchemy import Column, BigInteger, String, sql, Boolean

from ai_ohto.utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'ai_users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    status_news = Column(Boolean)
    query: sql.Select
