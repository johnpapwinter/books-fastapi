from sqlalchemy.orm import Session, Query
from math import ceil
from typing import TypeVar, Generic, Type, Any, Callable, Dict

from models import PaginatedResponse

T = TypeVar('T')
M = TypeVar('M')


class GenericService(Generic[T, M]):
    def __init__(self, db: Session, model: Type[T], schema: Type[M]):
        self.db = db
        self.model = model
        self.schema = schema

    def _paginate(self, query: Query, page: int, page_size: int) -> PaginatedResponse[M]:
        total_items = query.count()
        total_pages = ceil(total_items / page_size)

        items = query.offset((page - 1) * page_size).limit(page_size).all()
        schema_items = [self.schema.model_validate(item) for item in items]

        return PaginatedResponse(
            items=schema_items,
            current_page=page,
            total_pages=total_pages,
            total_items=total_items
        )

    def _db_operation(self, operation: Callable[[], Any]) -> Any:
        try:
            result = operation()
            self.db.commit()
            return result
        except Exception as e:
            print(f"Database operation failed: {e}")
            self.db.rollback()
            raise

    def _add_and_refresh(self, item: T) -> M:
        self.db.add(item)
        self.db.flush()
        self.db.refresh(item)
        return self.schema.model_validate(item)

    def _refresh(self, item: T) -> M:
        self.db.refresh(item)
        return self.schema.model_validate(item)

    def create(self, item: M) -> M:
        db_item = self.model(**item.model_dump())
        return self._db_operation(lambda: self._add_and_refresh(db_item))

    def update(self, db_item: T, update_data: Dict[str, Any]) -> M:
        def update_operation():
            for key, value in update_data.items():
                setattr(db_item, key, value)
            self.db.add(db_item)
            self.db.flush()
            self.db.refresh(db_item)
            return self.schema.model_validate(db_item)

        return self._db_operation(update_operation)
