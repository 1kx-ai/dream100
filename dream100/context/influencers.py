from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from dream100.models.influencer import Influencer
from dream100.models.project import Project


class InfluencerContext:
    def __init__(self, session):
        self.session = session

    def create_influencer(self, name, project_ids):
        influencer = Influencer(name=name)
        try:
            projects = self.session.query(Project).filter(Project.id.in_(project_ids)).all()
            influencer.projects = projects
            self.session.add(influencer)
            self.session.commit()
            self.session.refresh(influencer)
            return influencer
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_influencer(self, influencer_id):
        return (
            self.session.query(Influencer)
            .options(joinedload(Influencer.projects))
            .filter(Influencer.id == influencer_id)
            .first()
        )

    def update_influencer(self, influencer_id, name=None, project_ids=None):
        influencer = self.get_influencer(influencer_id)
        if influencer:
            if name:
                influencer.name = name
            if project_ids is not None:
                projects = (
                    self.session.query(Project)
                    .filter(Project.id.in_(project_ids))
                    .all()
                )
                influencer.projects = projects
            try:
                self.session.commit()
                return influencer
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def delete_influencer(self, influencer_id):
        influencer = self.get_influencer(influencer_id)
        if influencer:
            try:
                self.session.delete(influencer)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    def list_influencers(self, project_id=None):
        query = self.session.query(Influencer).options(joinedload(Influencer.projects))
        
        if project_id is not None:
            query = query.filter(Influencer.projects.any(Project.id == project_id))
        
        return query.all()

    def get_influencer_projects(self, influencer_id):
        influencer = self.get_influencer(influencer_id)
        return influencer.projects if influencer else []
