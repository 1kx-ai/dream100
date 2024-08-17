import pytest
import vcr
from dream100.models.web_property import WebPropertyType
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
    influencer = create_influencer(name="Timothy Sykes")
    get_influencer_web_properties(db_session)
    web_properties = web_property_context.list_web_properties()

    # Print web properties for debugging
    print(f"Web properties for {influencer.name}:")
    for wp in web_properties:
        print(f"Type: {wp.type}, URL: {wp.url}")


@my_vcr.use_cassette(
    "tests/vcr_cassettes/test_get_influencer_web_properties_specific_influencer.yaml"
)
def test_get_influencer_web_properties_specific_influencer(
    db_session,
    web_property_context,
    create_influencer,
):
    # Create a specific influencer
    influencer = create_influencer(name="Timothy Sykes")

    # Get web properties for the specific influencer
    get_influencer_web_properties(db_session, influencer.id)

    # Check if web properties were created for the influencer
    web_properties = web_property_context.list_web_properties(
        influencer_id=influencer.id
    )

    # Assert that web properties were found
    assert (
        len(web_properties) > 0
    ), f"No web properties found for influencer {influencer.name}"

    # Check if the correct types of web properties were created
    property_types = [wp.type for wp in web_properties]
    expected_types = [
        WebPropertyType.WEBSITE,
        WebPropertyType.FACEBOOK,
        WebPropertyType.TWITTER,
        WebPropertyType.YOUTUBE,
        WebPropertyType.LINKEDIN,
    ]

    for expected_type in expected_types:
        assert (
            expected_type in property_types
        ), f"Expected web property type {expected_type} not found for influencer {influencer.name}"

    # Print web properties for debugging
    print(f"Web properties for {influencer.name}:")
    for wp in web_properties:
        print(f"Type: {wp.type}, URL: {wp.url}")
