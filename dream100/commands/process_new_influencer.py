import asyncio
import logging
from dream100.db_config import create_session
from dream100.context.influencers import InfluencerContext
from dream100.services.get_influencer_web_properties import (
    get_influencer_web_properties,
)
from dream100.services.get_influencer_youtube_links import get_influencer_youtube_links
from dream100.services.get_youtube_transcripts import get_youtube_transcripts
from dream100.services.embed_youtube_transcripts import embed_youtube_transcripts

logger = logging.getLogger(__name__)


class ProcessNewInfluencerCommand:
    def __init__(self, session=None):
        if session:
            self.session = session
            self.should_close_session = False
        else:
            self.session, _ = create_session()
            self.should_close_session = True
        self.influencer_context = InfluencerContext(session)

    async def execute(self, influencer_id):
        logger.info(f"Starting processing for new influencer with ID: {influencer_id}")

        try:
            print("STEP1")
            # Step 1: Get web properties
            await self._run_step(
                get_influencer_web_properties, self.session, influencer_id
            )

            print("STEP2")
            # Step 2: Get YouTube links
            await self._run_step(
                get_influencer_youtube_links, self.session, influencer_id
            )

            # Step 3: Get YouTube transcripts
            await self._run_step(get_youtube_transcripts, self.session, influencer_id)

            # Step 4: Embed YouTube transcripts
            await self._run_step(
                embed_youtube_transcripts,
                "Embedding YouTube transcripts",
                influencer_id,
            )

            logger.info(f"Completed processing for influencer with ID: {influencer_id}")
        except Exception as e:
            logger.error(f"Error processing influencer {influencer_id}: {str(e)}")
            # Optionally, update influencer status to indicate error
            # self.influencer_context.update_influencer(influencer_id, status='ERROR')

    async def _run_step(self, func, step_name, influencer_id):
        logger.info(f"Starting step: {step_name} for influencer {influencer_id}")
        try:
            await asyncio.to_thread(func, self.session, influencer_id)
            logger.info(f"Completed step: {step_name} for influencer {influencer_id}")
        except Exception as e:
            logger.error(
                f"Error in {step_name} for influencer {influencer_id}: {str(e)}"
            )
            raise


def process_new_influencer(session, influencer_id):
    command = ProcessNewInfluencerCommand(session)
    asyncio.run(command.execute(influencer_id))
