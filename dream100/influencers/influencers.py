from sqlalchemy.exc import SQLAlchemyError
from dream100.models.influencer import Influencer
from dream100.models.project import Project


class InfluencerContext:
    def __init__(self, session):
        self.session = session

    def create_influencer(self, name, project_ids):
        influencer = Influencer(name=name)
        try:
            projects = (
                self.session.query(Project).filter(Project.id.in_(project_ids)).all()
            )
            influencer.projects = projects
            self.session.add(influencer)
            self.session.commit()
            return influencer
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_influencer(self, influencer_id):
        return self.session.get(Influencer, influencer_id)

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

    def list_influencers(self):
        return self.session.query(Influencer).all()

    def get_influencer_projects(self, influencer_id):
        influencer = self.get_influencer(influencer_id)
        return influencer.projects if influencer else []
