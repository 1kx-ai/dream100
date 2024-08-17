import pytest
import vcr
from dream100.services.get_youtube_transcripts import GetYoutubeTranscripts
from dream100.models.content import ContentStatus, Content

my_vcr = vcr.VCR(
    record_mode="once",
    match_on=["uri", "method", "query"],
)


@my_vcr.use_cassette("tests/vcr_cassettes/test_get_youtube_transcripts.yaml")
def test_get_youtube_transcripts(db_session, create_content):
    content = create_content(
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ", status=ContentStatus.NONE
    )
    service = GetYoutubeTranscripts(batch_size=1, delay=1, session=db_session)
    service.get_and_update_transcripts()
    updated_content = db_session.query(Content).filter_by(id=content.id).first()
    assert updated_content.scraped_content is not None
    assert updated_content.status == ContentStatus.OK


@my_vcr.use_cassette(
    "tests/vcr_cassettes/test_get_youtube_transcripts_invalid_url.yaml"
)
def test_get_youtube_transcripts_invalid_url(create_content, db_session):
    content = create_content(
        link="https://www.youtube.com/watch?v=kxieMYNdWeE&t=4s",
        status=ContentStatus.NONE,
    )
    service = GetYoutubeTranscripts(batch_size=1, delay=1, session=db_session)
    service.get_and_update_transcripts()
    updated_content = db_session.query(Content).filter_by(id=content.id).first()
    assert updated_content.status == ContentStatus.ERROR
    assert updated_content.scraped_content is None


@my_vcr.use_cassette(
    "tests/vcr_cassettes/test_get_youtube_transcripts_with_influencer_id.yaml"
)
def test_get_youtube_transcripts_with_influencer_id(
    create_content, db_session, create_influencer
):
    influencer = create_influencer(name="Test Influencer")
    content = create_content(
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        status=ContentStatus.NONE,
        influencer_id=influencer.id,
    )
    service = GetYoutubeTranscripts(
        batch_size=1, delay=1, session=db_session, influencer_id=influencer.id
    )
    service.get_and_update_transcripts()
    updated_content = db_session.query(Content).filter_by(id=content.id).first()
    assert updated_content.scraped_content is not None
    assert updated_content.status == ContentStatus.OK
