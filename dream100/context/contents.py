from sqlalchemy.exc import SQLAlchemyError
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
import logging

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
        content_status=None,
        has_scraped_content=None,
        web_property_type=None,
    ):
        query = self.session.query(Content).join(Content.web_property)

        if web_property_id is not None:
            query = query.filter(Content.web_property_id == web_property_id)

        if content_status is not None:
            query = query.filter(Content.status == content_status)

        if web_property_type is not None:
            query = query.filter(WebProperty.type == web_property_type)

        if has_scraped_content is True:
            query = query.filter(Content.scraped_content.isnot(None))
        elif has_scraped_content is False:
            query = query.filter(Content.scraped_content.is_(None))

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
