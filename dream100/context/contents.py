from sqlalchemy.exc import SQLAlchemyError
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty
from sqlalchemy.orm import joinedload


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
        self, web_property_id=None, status=None, has_scraped_content=None
    ):
        query = self.session.query(Content).options(joinedload(Content.web_property))
        if web_property_id is not None:
            query = query.filter_by(web_property_id=web_property_id)
        if status is not None:
            query = query.filter_by(status=status)
        if has_scraped_content == True:
            query = query.isnot(False)
        return query

    def list_contents(self, **kwargs):
        query = self.list_contents_query(**kwargs)
        return query.all()
from sqlalchemy import func, select

class ContentContext:
    # existing code...

    def count_contents(self, status=None, type=None, has_scraped_content=None):
        stmt = self.list_contents_query(status=status, type=type, has_scraped_content=has_scraped_content)
        return self.session.scalar(select(func.count()).select_from(stmt.subquery()))
