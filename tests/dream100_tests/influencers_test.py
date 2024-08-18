import pytest
from dream100.context.influencers import InfluencerContext
from dream100.models.influencer import Influencer
from dream100.models.project import Project


@pytest.fixture
def influencer_context(db_session):
    return InfluencerContext(db_session)


def test_create_influencer(influencer_context, create_project):
    sample_project = create_project()
    influencer = influencer_context.create_influencer("John Doe", [sample_project.id])
    assert influencer.name == "John Doe"
    assert len(influencer.projects) == 1
    assert influencer.projects[0].name == "Test Project"


def test_get_influencer(influencer_context, create_project):
    sample_project = create_project()
    influencer = influencer_context.create_influencer("Jane Smith", [sample_project.id])
    retrieved_influencer = influencer_context.get_influencer(influencer.id)
    assert retrieved_influencer.name == "Jane Smith"
    assert len(retrieved_influencer.projects) == 1


def test_update_influencer(influencer_context, create_project, db_session):
    sample_project = create_project()
    influencer = influencer_context.create_influencer(
        "Bob Johnson", [sample_project.id]
    )
    new_project = Project(name="New Project", description="A new test project")
    db_session.add(new_project)
    db_session.commit()

    updated_influencer = influencer_context.update_influencer(
        influencer.id, name="Bob Smith", project_ids=[new_project.id]
    )
    assert updated_influencer.name == "Bob Smith"
    assert len(updated_influencer.projects) == 1
    assert updated_influencer.projects[0].name == "New Project"


def test_delete_influencer(influencer_context, create_project):
    sample_project = create_project()
    influencer = influencer_context.create_influencer(
        "Alice Brown", [sample_project.id]
    )
    assert influencer_context.delete_influencer(influencer.id) == True
    assert influencer_context.get_influencer(influencer.id) is None


def test_list_influencers(influencer_context, create_project):
    sample_project = create_project()
    influencer_context.create_influencer("Influencer 1", [sample_project.id])
    influencer_context.create_influencer("Influencer 2", [sample_project.id])
    influencers = influencer_context.list_influencers()
    assert len(influencers) >= 2
    assert any(i.name == "Influencer 1" for i in influencers)
    assert any(i.name == "Influencer 2" for i in influencers)


def test_get_influencer_projects(influencer_context, create_project, db_session):
    sample_project = create_project()
    influencer = influencer_context.create_influencer(
        "Project Test", [sample_project.id]
    )
    new_project = Project(name="Another Project", description="Another test project")
    db_session.add(new_project)
    db_session.commit()
    influencer_context.update_influencer(
        influencer.id, project_ids=[sample_project.id, new_project.id]
    )

    projects = influencer_context.get_influencer_projects(influencer.id)
    assert len(projects) == 2
    assert any(p.name == "Test Project" for p in projects)
    assert any(p.name == "Another Project" for p in projects)

def test_list_influencers_by_project(influencer_context, create_project, db_session):
    project1 = create_project()
    project2 = Project(name="Project 2", description="Another test project")
    db_session.add(project2)
    db_session.commit()

    influencer_context.create_influencer("Influencer 1", [project1.id])
    influencer_context.create_influencer("Influencer 2", [project2.id])
    influencer_context.create_influencer("Influencer 3", [project1.id, project2.id])

    # Filter by project1
    influencers = influencer_context.list_influencers(project_id=project1.id)
    assert len(influencers) == 2
    assert any(i.name == "Influencer 1" for i in influencers)
    assert any(i.name == "Influencer 3" for i in influencers)
    assert all(project1.id in [p.id for p in i.projects] for i in influencers)

    # Filter by project2
    influencers = influencer_context.list_influencers(project_id=project2.id)
    assert len(influencers) == 2
    assert any(i.name == "Influencer 2" for i in influencers)
    assert any(i.name == "Influencer 3" for i in influencers)
    assert all(project2.id in [p.id for p in i.projects] for i in influencers)

    # No filter (should return all influencers)
    influencers = influencer_context.list_influencers()
    assert len(influencers) == 3