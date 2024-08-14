from sqlalchemy.exc import SQLAlchemyError
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty


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
        web_property = self.session.query(WebProperty).get(web_property_id)
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
        return self.session.query(Content).get(content_id)

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

    def list_contents(self, web_property_id=None, status=None):
        query = self.session.query(Content)
        if web_property_id:
            query = query.filter(Content.web_property_id == web_property_id)
        if status:
            query = query.filter(Content.status == status)
        return query.all()
