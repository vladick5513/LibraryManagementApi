from app.authors.models import Author
from app.dao.base import BaseDAO


class AuthorsDAO(BaseDAO):
    model = Author
