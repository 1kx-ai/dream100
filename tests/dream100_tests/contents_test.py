import pytest
from dream100.contents.contents import ContentContext
from dream100.models.content import Content, ContentStatus
from dream100.models.web_property import WebProperty, WebPropertyType


@pytest.fixture
def content_context(db_session):
    return ContentContext(db_session)


def test_create_content(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content = content_context.create_content(
        web_property.id,
        "https://www.youtube.com/watch?v=testVideo",
        "This is a test video",
        1000,
        ContentStatus.NONE,
    )
    assert content.link == "https://www.youtube.com/watch?v=testVideo"
    assert content.scraped_content == "This is a test video"
    assert content.views == 1000
    assert content.status == ContentStatus.NONE


def test_get_content(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content = content_context.create_content(
        web_property.id, "https://www.youtube.com/watch?v=anotherVideo"
    )
    retrieved_content = content_context.get_content(content.id)
    assert retrieved_content.link == "https://www.youtube.com/watch?v=anotherVideo"


def test_update_content(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content = content_context.create_content(
        web_property.id, "https://www.youtube.com/watch?v=updateMe"
    )
    updated_content = content_context.update_content(
        content.id,
        link="https://www.youtube.com/watch?v=updatedVideo",
        scraped_content="Updated content",
        views=2000,
        status=ContentStatus.OK,
    )
    assert updated_content.link == "https://www.youtube.com/watch?v=updatedVideo"
    assert updated_content.scraped_content == "Updated content"
    assert updated_content.views == 2000
    assert updated_content.status == ContentStatus.OK


def test_delete_content(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content = content_context.create_content(
        web_property.id, "https://www.youtube.com/watch?v=deleteMe"
    )
    assert content_context.delete_content(content.id) == True
    assert content_context.get_content(content.id) is None


def test_list_contents(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content_context.create_content(
        web_property.id, "https://www.youtube.com/watch?v=video1"
    )
    content_context.create_content(
        web_property.id, "https://www.youtube.com/watch?v=video2"
    )
    contents = content_context.list_contents(web_property.id)
    assert len(contents) == 2
    assert any(c.link == "https://www.youtube.com/watch?v=video1" for c in contents)
    assert any(c.link == "https://www.youtube.com/watch?v=video2" for c in contents)


def test_list_contents_by_status(content_context, create_web_property):
    web_property = create_web_property(type=WebPropertyType.YOUTUBE)
    content_context.create_content(
        web_property.id,
        "https://www.youtube.com/watch?v=video3",
        status=ContentStatus.OK,
    )
    content_context.create_content(
        web_property.id,
        "https://www.youtube.com/watch?v=video4",
        status=ContentStatus.ERROR,
    )
    ok_contents = content_context.list_contents(status=ContentStatus.OK)
    error_contents = content_context.list_contents(status=ContentStatus.ERROR)
    assert len(ok_contents) == 1
    assert len(error_contents) == 1
    assert ok_contents[0].link == "https://www.youtube.com/watch?v=video3"
    assert error_contents[0].link == "https://www.youtube.com/watch?v=video4"
