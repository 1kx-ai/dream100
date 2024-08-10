from sqlalchemy.exc import SQLAlchemyError
from dream100.models.web_property import WebProperty, WebPropertyType


class WebPropertyContext:
    def __init__(self, session):
        self.session = session

    def create_web_property(self, influencer_id, type, url, followers=None):
        web_property = WebProperty(
            influencer_id=influencer_id,
            type=WebPropertyType(type),
            url=url,
            followers=followers,
        )
        try:
            self.session.add(web_property)
            self.session.commit()
            return web_property
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_web_property(self, web_property_id):
        return self.session.query(WebProperty).get(web_property_id)

    def update_web_property(self, web_property_id, type=None, url=None, followers=None):
        web_property = self.get_web_property(web_property_id)
        if web_property:
            if type:
                web_property.type = WebPropertyType(type)
            if url:
                web_property.url = url
            if followers is not None:
                web_property.followers = followers
            try:
                self.session.commit()
                return web_property
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def delete_web_property(self, web_property_id):
        web_property = self.get_web_property(web_property_id)
        if web_property:
            try:
                self.session.delete(web_property)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    def list_web_properties(self, influencer_id=None):
        query = self.session.query(WebProperty)
        if influencer_id:
            query = query.filter(WebProperty.influencer_id == influencer_id)
        return query.all()
