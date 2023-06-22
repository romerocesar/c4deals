import logging

import discord
import yaml

from slickdeals import SlickDealsFetcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('c4deals')


class C4Deals(discord.Client):

    def __init__(self, *args, config=None, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.reactions = True
        super().__init__(*args, intents=intents, **kwargs)
        self.approvers = config.get('approvers')
        self.token = config.get('token')
        self.deals_fetcher = SlickDealsFetcher(html=open('test.html').read())

    async def on_ready(self):
        deals = self.deals_fetcher.fetch_deals()
        for userid in self.approvers:
            user = await client.fetch_user(userid)
            deal = deals.iloc[0]
            msg = self.deals_fetcher.format_message(deal)
            sent_msg = await user.send(msg)
            await sent_msg.add_reaction("\U0001F44D")
            await sent_msg.add_reaction("\U0001F44E")

    async def on_reaction_add(self, reaction, user):
        logger.debug(f'got {reaction=} from {user=}')
        # TODO: make sure we only process reactions to deals and nothing else
        if user.id in self.approvers:
            if reaction.emoji == '\U0001F44D':  # thumbs up
                logger.info(f'deal {reaction.message} approved by {user.name}')
            elif reaction.emoji == '\U0001F44E':  # thumbs down
                logger.info(f'deal {reaction.message} approved by {user.name}')
            else:
                logger.warning(f'unknown emoji={reaction.emoji} in reaction.')
        else:
            logger.warning(f'ignoring reaction from {user=}')


config = yaml.safe_load(open('config.yaml'))
client = C4Deals(config=config)

client.run(config.get('token'))
