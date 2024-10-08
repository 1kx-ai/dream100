import pytest
import vcr
from dream100.services.get_influencer_youtube_links import (
    GetYouTubeLinksService,
    get_influencer_youtube_links,
)
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.influencer import Influencer
from dream100.models.content import Content

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir="tests/fixtures/vcr_cassettes",
    record_mode="once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="function")
def youtube_links_service(db_session):
    return GetYouTubeLinksService()


@my_vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/test_get_channel_id_from_channel_url.yaml"
)
def test_get_channel_id_from_channel_url(youtube_links_service):
    channel_id = youtube_links_service.get_channel_id_from_url(
        "https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ"
    )
    assert channel_id == "UCa-vrCLQHviTOVnEKDOdetQ"


@my_vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/test_get_channel_id_from_user_url.yaml"
)
def test_get_channel_id_from_user_url(youtube_links_service):
    user_channel_id = youtube_links_service.get_channel_id_from_url(
        "https://www.youtube.com/user/Computerphile"
    )
    assert user_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"


@my_vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_channel_id_from_c_url.yaml")
def test_get_channel_id_from_c_url(youtube_links_service):
    custom_channel_id = youtube_links_service.get_channel_id_from_url(
        "https://www.youtube.com/c/Computerphile"
    )
    assert custom_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"


@my_vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/test_get_channel_id_from_tag_url.yaml"
)
def test_get_channel_id_from_tag_url(youtube_links_service):
    at_tag_channel_id = youtube_links_service.get_channel_id_from_url(
        "https://www.youtube.com/@Computerphile"
    )
    assert at_tag_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"


@my_vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_channel_videos.yaml")
def test_get_channel_videos(youtube_links_service):
    videos = youtube_links_service.get_channel_videos(
        "https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ"
    )
    assert len(videos) > 0
    assert all(v.startswith("https://www.youtube.com/watch?v=") for v in videos)


@my_vcr.use_cassette("test_process_youtube_links.yaml")
def test_process_youtube_links(db_session, create_influencer, create_web_property):
    # Create a test influencer and web property
    influencer = create_influencer("Test Influencer")
    web_property = create_web_property(
        influencer_id=influencer.id,
        type="youtube",
        url="https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ",
    )

    db_session.add(web_property)
    db_session.commit()

    # Use the get_influencer_youtube_links function with the test session
    get_influencer_youtube_links(db_session)

    contents = (
        db_session.query(Content).filter_by(web_property_id=web_property.id).all()
    )

    assert len(contents) > 0
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents)


@my_vcr.use_cassette("test_process_youtube_links_filtered.yaml")
def test_process_youtube_links_filtered(
    db_session, create_influencer, create_web_property
):
    # Create multiple test influencers and web properties
    influencer1 = create_influencer("Test Influencer 1")
    influencer2 = create_influencer("Test Influencer 2")

    web_property1 = create_web_property(
        influencer_id=influencer1.id,
        type="youtube",
        url="https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ",
    )
    web_property2 = create_web_property(
        influencer_id=influencer2.id,
        type="youtube",
        url="https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA",
    )

    db_session.add_all([web_property1, web_property2])
    db_session.commit()

    # Use the get_influencer_youtube_links function with the test session and filter for influencer1
    get_influencer_youtube_links(db_session, influencer_id=influencer1.id)

    # Check contents for influencer1
    contents1 = (
        db_session.query(Content).filter_by(web_property_id=web_property1.id).all()
    )
    assert len(contents1) > 0
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents1)

    # Check contents for influencer2 (should be empty)
    contents2 = (
        db_session.query(Content).filter_by(web_property_id=web_property2.id).all()
    )
    assert len(contents2) == 0

    # Now process for all influencers
    get_influencer_youtube_links(db_session)

    # Check contents for both influencers
    contents1 = (
        db_session.query(Content).filter_by(web_property_id=web_property1.id).all()
    )
    contents2 = (
        db_session.query(Content).filter_by(web_property_id=web_property2.id).all()
    )

    assert len(contents1) > 0
    assert len(contents2) > 0
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents1)
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents2)
