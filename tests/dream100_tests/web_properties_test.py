import pytest
from dream100.context.web_properties import WebPropertyContext
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.influencer import Influencer
from dream100.models.project import Project


@pytest.fixture
def web_property_context(db_session):
    return WebPropertyContext(db_session)


def test_create_web_property(web_property_context, create_influencer):
    sample_influencer = create_influencer()
    web_property = web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.YOUTUBE.value,
        "https://www.youtube.com/testchannel",
        1000,
    )
    assert web_property.influencer_id == sample_influencer.id
    assert web_property.type == WebPropertyType.YOUTUBE
    assert web_property.url == "https://www.youtube.com/testchannel"
    assert web_property.followers == 1000


def test_get_web_property(web_property_context, create_influencer):
    sample_influencer = create_influencer()
    web_property = web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.FACEBOOK.value,
        "https://www.facebook.com/testpage",
    )
    retrieved_web_property = web_property_context.get_web_property(web_property.id)
    assert retrieved_web_property.type == WebPropertyType.FACEBOOK
    assert retrieved_web_property.url == "https://www.facebook.com/testpage"


def test_update_web_property(web_property_context, create_influencer):
    sample_influencer = create_influencer()
    web_property = web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.TWITTER.value,
        "https://www.twitter.com/testaccount",
    )
    updated_web_property = web_property_context.update_web_property(
        web_property.id,
        type=WebPropertyType.LINKEDIN.value,
        url="https://www.linkedin.com/testprofile",
        followers=2000,
    )
    assert updated_web_property.type == WebPropertyType.LINKEDIN
    assert updated_web_property.url == "https://www.linkedin.com/testprofile"
    assert updated_web_property.followers == 2000


def test_delete_web_property(web_property_context, create_influencer):
    sample_influencer = create_influencer()
    web_property = web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.WEBSITE.value,
        "https://www.testwebsite.com",
    )
    assert web_property_context.delete_web_property(web_property.id) == True
    assert web_property_context.get_web_property(web_property.id) is None


def test_list_web_properties(web_property_context, create_influencer):
    sample_influencer = create_influencer()
    web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.YOUTUBE.value,
        "https://www.youtube.com/channel1",
    )
    web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.FACEBOOK.value,
        "https://www.facebook.com/page1",
    )
    web_properties = web_property_context.list_web_properties(sample_influencer.id)
    assert len(web_properties) == 2
    assert any(wp.type == WebPropertyType.YOUTUBE for wp in web_properties)
    assert any(wp.type == WebPropertyType.FACEBOOK for wp in web_properties)


def test_list_all_web_properties(web_property_context, create_influencer, db_session):
    sample_influencer = create_influencer()
    another_influencer = Influencer(name="Another Influencer")
    db_session.add(another_influencer)
    db_session.commit()

    web_property_context.create_web_property(
        sample_influencer.id,
        WebPropertyType.TWITTER.value,
        "https://www.twitter.com/account1",
    )
    web_property_context.create_web_property(
        another_influencer.id,
        WebPropertyType.LINKEDIN.value,
        "https://www.linkedin.com/profile1",
    )
    all_web_properties = web_property_context.list_web_properties()
    assert len(all_web_properties) >= 2
    assert any(wp.type == WebPropertyType.TWITTER for wp in all_web_properties)
    assert any(wp.type == WebPropertyType.LINKEDIN for wp in all_web_properties)

def test_web_property_context(db_session, create_influencer, create_web_property, create_project):
    from dream100.context.web_properties import WebPropertyContext
    
    project1 = create_project("Project 1")
    project2 = create_project("Project 2")
    influencer1 = create_influencer("Influencer 1")
    influencer2 = create_influencer("Influencer 2")
    influencer1.projects.extend([project1, project2])
    influencer2.projects.append(project2)
    db_session.commit()
    
    create_web_property(influencer_id=influencer1.id, type="youtube", url="https://youtube.com/channel1")
    create_web_property(influencer_id=influencer2.id, type="twitter", url="https://twitter.com/user2")
    
    context = WebPropertyContext(db_session)
    
    # Test listing all web properties
    all_properties = context.list_web_properties()
    assert len(all_properties) == 2
    
    # Test filtering by influencer_id
    influencer1_properties = context.list_web_properties(influencer_id=influencer1.id)
    assert len(influencer1_properties) == 1
    assert influencer1_properties[0].url == "https://youtube.com/channel1"
    
    # Test filtering by project_id
    project2_properties = context.list_web_properties(project_id=project2.id)
    assert len(project2_properties) == 2
    
    # Test filtering by both influencer_id and project_id
    filtered_properties = context.list_web_properties(influencer_id=influencer1.id, project_id=project1.id)
    assert len(filtered_properties) == 1
    assert filtered_properties[0].url == "https://youtube.com/channel1"