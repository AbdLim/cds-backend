from typing import Generic, Optional, Type, TypeVar, List
from uuid import UUID

from sqlmodel import Session, SQLModel, select
from sqlalchemy import func

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_count(self) -> int:
        statement = select(func.count()).select_from(self.model)
        return self.session.exec(statement).first()

    def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        self.session.commit()
        self.session.refresh(obj_in)
        return obj_in

    def create_many(self, objects: List[ModelType]) -> List[ModelType]:
        self.session.add_all(objects)
        self.session.commit()
        for obj in objects:
            self.session.refresh(obj)
        return objects

    def update(self, id: UUID, obj_in: dict) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        obj = self.session.exec(statement).first()
        if not obj:
            return None

        for field, value in obj_in.items():
            if hasattr(obj, field):
                setattr(obj, field, value)

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: UUID) -> bool:
        statement = select(self.model).where(self.model.id == id)
        obj = self.session.exec(statement).first()
        if not obj:
            return False

        self.session.delete(obj)
        self.session.commit()
        return True

    def exists(self, id: UUID) -> bool:
        statement = select(func.count()).select_from(self.model).where(self.model.id == id)
        return self.session.exec(statement).first() > 0 