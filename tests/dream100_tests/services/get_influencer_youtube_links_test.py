import pytest
import vcr
from dream100.services.get_influencer_youtube_links import GetYouTubeLinksService, get_influencer_youtube_links
from dream100.db_config import create_session
from dream100.models.web_property import WebProperty, WebPropertyType
from dream100.models.influencer import Influencer
from dream100.models.content import Content

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

@pytest.fixture(scope="module")
def db_session():
    session, _ = create_session()
    yield session
    session.close()

@pytest.fixture(scope="module")
def youtube_links_service(db_session):
    return GetYouTubeLinksService()

@pytest.fixture(scope="module")
def sample_influencer(db_session):
    influencer = Influencer(name="Test Influencer")
    db_session.add(influencer)
    db_session.commit()
    
    web_property = WebProperty(
        influencer_id=influencer.id,
        type=WebPropertyType.YOUTUBE,
        url="https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ"  # Example: Computerphile channel
    )
    db_session.add(web_property)
    db_session.commit()
    
    yield influencer
    
    # Cleanup
    db_session.query(Content).filter(Content.web_property_id == web_property.id).delete()
    db_session.delete(web_property)
    db_session.delete(influencer)
    db_session.commit()

@my_vcr.use_cassette()
def test_get_channel_id_from_url(youtube_links_service):
    channel_id = youtube_links_service.get_channel_id_from_url("https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ")
    assert channel_id == "UCa-vrCLQHviTOVnEKDOdetQ"

    user_channel_id = youtube_links_service.get_channel_id_from_url("https://www.youtube.com/user/Computerphile")
    assert user_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"

    custom_channel_id = youtube_links_service.get_channel_id_from_url("https://www.youtube.com/c/Computerphile")
    assert custom_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"

    # New test case for @ tag URL
    at_tag_channel_id = youtube_links_service.get_channel_id_from_url("https://www.youtube.com/@Computerphile")
    assert at_tag_channel_id == "UC9-y-6csu5WGm29I7JiwpnA"

@my_vcr.use_cassette()
def test_get_channel_videos(youtube_links_service):
    videos = youtube_links_service.get_channel_videos("https://www.youtube.com/channel/UCa-vrCLQHviTOVnEKDOdetQ")
    assert len(videos) > 0
    assert all(v.startswith("https://www.youtube.com/watch?v=") for v in videos)

@my_vcr.use_cassette()
def test_process_youtube_links(youtube_links_service, sample_influencer, db_session):
    youtube_links_service.process_youtube_links()
    
    web_property = db_session.query(WebProperty).filter_by(influencer_id=sample_influencer.id).first()
    contents = db_session.query(Content).filter_by(web_property_id=web_property.id).all()
    
    assert len(contents) > 0
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents)

@my_vcr.use_cassette()
def test_get_influencer_youtube_links(sample_influencer, db_session):
    get_influencer_youtube_links()
    
    web_property = db_session.query(WebProperty).filter_by(influencer_id=sample_influencer.id).first()
    contents = db_session.query(Content).filter_by(web_property_id=web_property.id).all()
    
    assert len(contents) > 0
    assert all(c.link.startswith("https://www.youtube.com/watch?v=") for c in contents)