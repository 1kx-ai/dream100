import pytest
import vcr
from dream100.context.web_properties import WebPropertyContext
from dream100.services.get_influencer_web_properties import (
    get_influencer_web_properties,
)

my_vcr = vcr.VCR(
    record_mode="once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="function")
def influencer_web_properties_service(db_session):
    return get_influencer_web_properties(db_session)


@pytest.fixture
def web_property_context(db_session):
    return WebPropertyContext(db_session)


@my_vcr.use_cassette(
    "tests/vcr_cassettes/test_get_influencer_web_properties_no_existing_properties.yaml"
)
def test_get_influencer_web_properties_no_existing_properties(
    db_session,
    web_property_context,
    influencer_web_properties_service,
    create_influencer,
):
    create_influencer(name="Timothy Sykes")
    get_influencer_web_properties(db_session)
    web_properties = web_property_context.list_web_properties()
    print(web_properties)
