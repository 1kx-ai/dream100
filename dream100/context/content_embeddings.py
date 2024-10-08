from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from dream100.models.content_embedding import ContentEmbedding
from dream100.models.content import Content


class ContentEmbeddingContext:
    def __init__(self, session):
        self.session = session

    def create_embedding(self, content_id, chunk_text, embedding):
        try:
            content_embedding = ContentEmbedding(
                content_id=content_id, chunk_text=chunk_text, embedding=embedding
            )
            self.session.add(content_embedding)
            self.session.commit()
            return content_embedding
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_embedding(self, embedding_id):
        return self.session.get(ContentEmbedding, embedding_id)

    def delete_embedding(self, embedding_id):
        embedding = self.get_embedding(embedding_id)
        if embedding:
            try:
                self.session.delete(embedding)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    def get_embeddings_for_content(self, content_id):
        stmt = select(ContentEmbedding).filter_by(content_id=content_id)
        return self.session.scalars(stmt).all()

    def update_embedding(self, embedding_id, chunk_text=None, embedding=None):
        content_embedding = self.get_embedding(embedding_id)
        if content_embedding:
            if chunk_text is not None:
                content_embedding.chunk_text = chunk_text
            if embedding is not None:
                content_embedding.embedding = embedding
            try:
                self.session.commit()
                return content_embedding
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def list_embeddings(
        self, content_id=None, query_embedding=None, page=0, per_page=100
    ):
        query = self.session.query(ContentEmbedding)

        if content_id is not None:
            query = query.filter(ContentEmbedding.content_id == content_id)

        if query_embedding is not None:
            query = query.order_by(
                ContentEmbedding.embedding.cosine_distance(query_embedding)
            )

        if page is not None and per_page is not None:
            query = query.offset((page - 1) * per_page).limit(per_page)

        return query.all()

    def get_embedding_count(self, content_id=None):
        stmt = select(func.count()).select_from(ContentEmbedding)
        if content_id is not None:
            stmt = stmt.filter_by(content_id=content_id)
        return self.session.scalar(stmt)
