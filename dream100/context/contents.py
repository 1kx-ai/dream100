from sqlalchemy.exc import SQLAlchemyError
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty
from dream100.models.content_embedding import ContentEmbedding
from dream100.models.influencer import Influencer
from dream100.models.project import Project
from sqlalchemy import select, func
from sqlalchemy.sql.expression import cast
from sqlalchemy import Float
from pgvector.sqlalchemy import Vector
import logging
from dream100.utilities.embedding_utils import create_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentContext:
    def __init__(self, session):
        self.session = session

    def create_content(
        self,
        web_property_id,
        link,
        scraped_content=None,
        views=0,
        status=ContentStatus.NONE,
    ):
        web_property = self.session.get(WebProperty, web_property_id)
        if web_property:
            content = Content(
                web_property_id=web_property_id,
                link=link,
                scraped_content=scraped_content,
                views=views,
                status=status,
            )
            try:
                self.session.add(content)
                self.session.commit()
                return content
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def get_content(self, content_id):
        return self.session.get(Content, content_id)

    def update_content(
        self, content_id, link=None, scraped_content=None, views=None, status=None
    ):
        content = self.get_content(content_id)
        if content:
            if link:
                content.link = link
            if scraped_content is not None:
                content.scraped_content = scraped_content
            if views is not None:
                content.views = views
            if status is not None:
                content.status = status
            try:
                self.session.commit()
                return content
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def delete_content(self, content_id):
        content = self.get_content(content_id)
        if content:
            try:
                self.session.delete(content)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    def list_contents_query(
        self,
        web_property_id=None,
        content_statuses=None,
        has_scraped_content=None,
        web_property_type=None,
        influencer_id=None,
        batch_size=None,
    ):
        query = (
            self.session.query(Content)
            .join(Content.web_property)
            .join(WebProperty.influencer)
        )

        if influencer_id is not None:
            query = query.join(WebProperty.influencer).filter(
                Influencer.id == influencer_id
            )

        if web_property_id is not None:
            query = query.filter(Content.web_property_id == web_property_id)

        if content_statuses:
            if isinstance(content_statuses, (list, tuple)):
                query = query.filter(Content.status.in_(content_statuses))
            else:
                query = query.filter(Content.status == content_statuses)

        if web_property_type is not None:
            query = query.filter(WebProperty.type == web_property_type)

        if has_scraped_content is True:
            query = query.filter(Content.scraped_content.isnot(None))
        elif has_scraped_content is False:
            query = query.filter(Content.scraped_content.is_(None))

        if batch_size:
            query = query.limit(batch_size)

        logger.debug(f"Generated SQL query: {query}")
        return query

    def list_contents(self, **kwargs):
        query = self.list_contents_query(**kwargs)
        return query.all()

    def count_contents(self, **kwargs):
        stmt = self.list_contents_query(**kwargs)
        return self.session.scalar(select(func.count()).select_from(stmt.subquery()))

    def iter_contents(self, batch_size=100, **kwargs):
        query = self.list_contents_query(**kwargs)
        yield from self.session.execute(query).scalars().yield_per(batch_size)

    def search_contents(self, query_embedding, project_id=None, per_page=10, page=0):
        # Perform the vector similarity search with pagination
        query = (
            self.session.query(
                Content,
                func.min(
                    func.l2_distance(
                        ContentEmbedding.embedding, cast(query_embedding, Vector)
                    )
                ).label("distance"),
            )
            .join(Content.embeddings)
            .join(Content.web_property)
            .join(WebProperty.influencer)
            .join(Influencer.projects)
        )

        if project_id is not None:
            query = query.filter(Project.id == project_id)

        query = (
            query.group_by(Content.id)
            .order_by("distance")
            .offset(page * per_page)
            .limit(per_page)
        )

        results = query.all()

        # Format the results
        contents = [
            {"content": content, "distance": float(distance)}
            for content, distance in results
        ]

        if project_id is not None:
            total_count_query = query.filter(Project.id == project_id)

        total_count = total_count_query.distinct().count()

        return {
            "contents": contents,
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
        }
