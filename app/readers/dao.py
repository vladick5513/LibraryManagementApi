from app.dao.base import BaseDAO
from app.readers.models import Reader


class ReadersDAO(BaseDAO):
    model = Reader