import pytest
import vcr
from dream100.commands.process_new_influencer import process_new_influencer
from dream100.context.influencers import InfluencerContext
from dream100.context.web_properties import WebPropertyContext
from dream100.context.contents import ContentContext


my_vcr = vcr.VCR(
    record_mode="once",
    match_on=["uri", "method", "query"],
)


@my_vcr.use_cassette("tests/vcr_cassettes/test_process_new_influencer.yaml")
def test_process_new_influencer(db_session, create_influencer):
    influencer = create_influencer(name="Timothy Sykes")
    process_new_influencer(db_session, influencer.id)

    influencer_context = InfluencerContext(db_session)
    web_property_context = WebPropertyContext(db_session)
    content_context = ContentContext(db_session)

    influencer = influencer_context.get_influencer(influencer.id)
    assert influencer is not None

    web_properties = web_property_context.list_web_properties(
        influencer_id=influencer.id
    )
    assert len(web_properties) > 0

    contents = content_context.list_contents(influencer_id=influencer.id)
    assert len(contents) > 0
