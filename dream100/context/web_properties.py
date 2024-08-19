from sqlalchemy.exc import SQLAlchemyError
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.project import Project
from dream100.models.influencer import Influencer


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
        return self.session.get(WebProperty, web_property_id)

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

    def list_web_properties_query(self, influencer_id=None, web_property_type=None, project_id=None, page=None, per_page=None):
        query = self.session.query(WebProperty)

        if influencer_id:
            query = query.filter(WebProperty.influencer_id == influencer_id)
            
        if web_property_type:
            query = query.filter(WebProperty.type == WebPropertyType(web_property_type))

        if project_id:
            query = query.join(Influencer, WebProperty.influencer_id == Influencer.id)
            query = query.join(Project, Influencer.projects)
            query = query.filter(Project.id == project_id)

        if page is not None and per_page is not None:
            query = query.offset((page - 1) * per_page).limit(per_page)

        return query

    def list_web_properties(self, influencer_id=None, web_property_type=None, project_id=None, page=None, per_page=None):
        query = self.list_web_properties_query(influencer_id, web_property_type, project_id, page, per_page)
        return query.all()

    def count_web_properties(self, influencer_id=None, web_property_type=None, project_id=None):
        query = self.list_web_properties_query(influencer_id, web_property_type, project_id)
        return query.count()
