from __future__ import annotations

import os
from typing import Protocol
from typing import TypeAlias

from slack_bolt.app import App

Block: TypeAlias = dict[str, str | dict[str, str]]
View: TypeAlias = dict[str, str | list[Block]]
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


class BlockBuilder(Protocol):
    """protocol for all slack blocks"""

    def build(self) -> Block:
        """build the slack block"""
        ...


class DividerBlockBuilder(BlockBuilder):
    """class building divider blocks"""

    def build(self) -> Block:
        return {"type": "divider"}


class MarkdownBlockBuilder(BlockBuilder):
    """class building divider blocks"""

    def __init__(self):
        self._text = ""

    def text(self, value: str) -> BlockBuilder:
        """add the text to the builder"""
        self._text = value
        return self

    def build(self) -> Block:
        return {
            "type": "section",
            "text": {"type": "mrkdwn", "text": self._text},
        }


class ViewBuilder:
    """class helping building a slack view"""

    def __init__(self, type_: str, callback_id: str):
        self.type_ = type_
        self.callback_id = callback_id
        self._blocks: list[Block] = []

    def add_block(self, block: Block) -> ViewBuilder:
        """add a block to the view"""
        self._blocks.append(block)
        return self

    def build(self) -> View:
        """build a slack view from aggregated blocks"""
        return {
            "type": self.type_,
            "callback_id": self.callback_id,
            "blocks": self._blocks,
        }


@app.command("/beerbox")
def beerbox_controller(ack, respond, command):
    """command controller"""
    ack()
    respond(f"{command['text']}")


@app.event("app_home_opened")
def home_controller(client, event, logger):
    """home controller"""
    try:
        divider = DividerBlockBuilder().build()
        title = MarkdownBlockBuilder().text("*Welcome to your beerbox's home page*").build()
        content = (
            MarkdownBlockBuilder()
            .text("There is nothing fancy here yet, but much more is coming soon.")
            .build()
        )

        view = ViewBuilder(type_="home", callback_id="home_view")
        view.add_block(title)
        view.add_block(divider)
        view.add_block(content)

        client.views_publish(user_id=event["user"], view=view.build())
    except Exception as error:  # pylint: disable=broad-except
        logger.error(f"Error publishing home tab: {error}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
