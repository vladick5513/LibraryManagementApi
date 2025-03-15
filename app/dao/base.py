from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete, func
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_factory
from app.logger import logger
from typing import Any, Dict, List, Optional, TypeVar, Union
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_factory() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create (cls, **values):
        async with async_session_factory() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def get(cls, id: int) -> Optional[ModelType]:
        """Получение записи по ID."""
        async with async_session_factory() as session:
            try:
                query = select(cls.model).where(cls.model.id == id)
                result = await session.execute(query)
                return result.scalars().first()
            except SQLAlchemyError as e:
                logger.error(f"Error getting {cls.model.__name__} with id {id}: {e}")
                raise

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """Получение всех записей с пагинацией и фильтрацией."""
        async with async_session_factory() as session:
            try:
                query = select(cls.model)

                if filters:
                    for key, value in filters.items():
                        if hasattr(cls.model, key) and value is not None:
                            query = query.where(getattr(cls.model, key) == value)

                query = query.offset(skip).limit(limit)

                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(f"Error getting all {cls.model.__name__}: {e}")
                raise

    @classmethod
    async def count(cls, filters: Optional[Dict[str, Any]] = None) -> int:
        """Подсчет количества записей с учетом фильтров."""
        async with async_session_factory() as session:
            try:
                query = select(func.count()).select_from(cls.model)

                if filters:
                    for key, value in filters.items():
                        if hasattr(cls.model, key) and value is not None:
                            query = query.where(getattr(cls.model, key) == value)

                result = await session.execute(query)
                return result.scalar()
            except SQLAlchemyError as e:
                logger.error(f"Error counting {cls.model.__name__}: {e}")
                raise

    @classmethod
    async def update(cls, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        """Обновление записи."""
        async with async_session_factory() as session:
            try:
                if isinstance(obj_in, dict):
                    update_data = obj_in
                else:
                    update_data = obj_in.model_dump(exclude_unset=True)

                query = (
                    sqlalchemy_update(cls.model)
                    .where(cls.model.id == id)
                    .values(**update_data)
                    .returning(cls.model)
                )

                result = await session.execute(query)
                await session.commit()

                updated_obj = result.scalars().first()
                if updated_obj:
                    logger.info(f"Updated {cls.model.__name__} with id: {id}")
                return updated_obj
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error updating {cls.model.__name__} with id {id}: {e}")
                raise

    @classmethod
    async def delete(cls, id: int) -> bool:
        """Удаление записи."""
        async with async_session_factory() as session:
            try:
                query = (
                    sqlalchemy_delete(cls.model)
                    .where(cls.model.id == id)
                    .returning(cls.model.id)
                )
                result = await session.execute(query)
                await session.commit()

                deleted_id = result.scalar()
                if deleted_id:
                    logger.info(f"Deleted {cls.model.__name__} with id: {id}")
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error deleting {cls.model.__name__} with id {id}: {e}")
                raise