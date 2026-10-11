from typing import Any

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)


class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///test_tasks.db") -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.Session()

    def create_task(self, title: str, body: str, user_id: int) -> Task:
        session = self.get_session()
        task = Task(title=title, body=body, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        session.close()
        return task

    def get_task_by_id(self, task_id: int) -> Any:

        with self.get_session() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            session.close()
            return task

    def get_all_tasks(self) -> Any:

        with self.get_session() as session:
            tasks = session.query(Task).all()
            session.close()
            return tasks

    def delete_task(self, task_id: int) -> bool:

        session = self.get_session()
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    def clear_all_tasks(self) -> None:
        with self.get_session() as session:
            session.query(Task).delete()
            session.commit()
            session.close()
