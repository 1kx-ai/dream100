from sqlalchemy.exc import SQLAlchemyError
from dream100.models.project import Project


class ProjectContext:
    def __init__(self, session):
        self.session = session

    def create_project(self, name, description):
        project = Project(name=name, description=description)
        try:
            self.session.add(project)
            self.session.commit()
            return project
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_project(self, project_id):
        return self.session.get(Project, project_id)

    def update_project(self, project_id, name=None, description=None):
        project = self.get_project(project_id)
        if project:
            if name:
                project.name = name
            if description:
                project.description = description
            try:
                self.session.commit()
                return project
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return None

    def delete_project(self, project_id):
        project = self.get_project(project_id)
        if project:
            try:
                self.session.delete(project)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise e
        return False

    def list_projects(self):
        return self.session.query(Project).all()
