from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
from pydantic import Field
from typing import Literal
from utils import get_llm_response

# print("[StudyMate Notes Agent] running.")

"""
StudyMate Notes Agent

This agent is designed to assist students in preparing notes on various topics. 
Students can specify the topic they need notes on, the preferred style of the notes 
(short, detailed, or last-minute revision), and any reference material to be used. 
Additionally, students can provide any specific requirements or focus areas they 
would like the notes to cover. The agent uses this information to generate concise 
and useful notes tailored to the student's needs, helping them to study more effectively 
and efficiently.

Hi, can you help me prepare detailed notes on the topic of the French Revolution?

I need some quick revision notes for my upcoming exam on chemical bonding. Can you assist?

Can you create some concise notes on the basics of Python programming for me?

I'm looking for detailed notes on quantum mechanics using 'Introduction to Quantum Mechanics' by David J. Griffiths. Can you help?

Could you help me prepare last-minute revision notes on the major themes in Shakespeare's plays?
"""


class NotesAgentModel(Model):
  topic: str = Field(
      'NA',
      title="Topic",
      description=(
          "Please specify the specific topic on which notes are to be prepared. This should be a "
          "clear and concise string representing the subject matter. This value must be asked from user."
      ),
      example="Quantum Mechanics"
  )
  notes_style: Literal['Short', 'Detailed', 'Last Minute Revision'] = Field(
      'Detailed',
      title="Notes Style",
      description=(
          "Please specify the style of the notes. Options are 'Short' for brief summaries, 'Detailed' "
          "for comprehensive coverage, and 'Last Minute Revision' for key points and quick review. This value must be asked from user."
      ),
      example="Detailed"
  )
  reference_material: str = Field(
      'NA',
      title="Reference Material",
      description=(
          "Please specify any reference material or source from which the notes are to be prepared. "
          "This can include textbooks, articles, lecture notes, etc. This value must be asked from user."
      ),
      example="Introduction to Quantum Mechanics by David J. Griffiths"
  )
  additional_requirements: str = Field(
      'NA',
      title="Additional Requirements",
      description=(
          "Please specify any additional requirements or specific focus areas for the notes. This can include "
          "focusing on certain subtopics, including specific examples, etc. This value must be asked from user."
      ),
      example="Include examples of wave function normalization"
  )


notes_agent_protocol = Protocol("NotesAgentProtocol")


@notes_agent_protocol.on_message(model=NotesAgentModel, replies={UAgentResponse})
async def get_action(ctx: Context, sender: str, msg: NotesAgentModel):
  ctx.logger.info(f"📩 Incoming message from {sender}:")
  ctx.logger.info(f"👉 Data: {msg.json(indent=2)}")

  formatted_prompt = (
      "You are acting as a tool that helps students prepare notes for various subjects and topics. "
      "The user supplies specific details such as the topic they need notes on, the preferred style "
      "of the notes (short, detailed, or last-minute revision), any reference material, and additional "
      "requirements or focus areas for the notes. Based on this information, you generate concise and "
      "tailored notes to assist students in studying effectively and efficiently.\n\n"
      "Given the provided data for the Notes Agent, your task is to prepare notes on the following:\n\n"
      f"- Topic: {msg.topic}\n"
      f"- Notes Style: {msg.notes_style}\n"
      f"- Reference Material: {msg.reference_material}\n"
      f"- Additional Requirements: {msg.additional_requirements}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to generate the notes accordingly."
  )
  ctx.logger.info(f'{formatted_prompt=}')

  #   message = (
  #       "This is a test message. Once the language model (LLM) is integrated, this will be replaced "
  #       "with the final notes."
  #   )
  message = await get_llm_response(formatted_prompt)
  await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))


AGENT_NAME = 'notes_agent'
AGENT_PORT = 8001
AGENT_SEED = AGENT_NAME
AGENT_ENDPOINT = [f'http://localhost:{AGENT_PORT}/submit']
AGENT_MAILBOX_KEY = ""

notes_agent = Agent(name=AGENT_NAME,
                    seed=AGENT_SEED,
                    # port=AGENT_PORT,
                    # endpoint=AGENT_ENDPOINT,
                    # mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai"
                    )
notes_agent.include(notes_agent_protocol, publish_manifest=True)


@notes_agent.on_event("startup")
async def startup(ctx: Context):
  ctx.logger.info(f"🤖 Agent Address: {ctx.address}")

NOTES_AGENT_ADDRESS = notes_agent.address

if __name__ == "__main__":
  notes_agent.run()
