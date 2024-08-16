import pytest
from dream100.context.web_properties import WebPropertyContext
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.influencer import Influencer


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
