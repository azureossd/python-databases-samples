from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# from app import engine

class Base(DeclarativeBase):
     pass

class Task(Base):
     __tablename__ = "task"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(30))
     completed: Mapped[bool] = mapped_column(default=False)


     def __repr__(self) -> str:
         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
     

# Base.metadata.create_all(engine)