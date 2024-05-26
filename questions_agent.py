from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
from pydantic import Field
from typing import Literal
from utils import get_llm_response

# print("[StudyMate Questions Agent] running.")

"""
StudyMate Questions Agent

This agent is designed to assist students by providing practice questions and answers 
for various subjects and topics. Students can specify the topic for which they need 
practice questions, whether they need questions with or without answers, and any 
additional requirements or preferences they may have. The agent will then generate 
appropriate practice questions tailored to the student's needs, helping them to 
prepare effectively for exams and assessments.

Hi, can you provide me with some practice questions on basic algebra?

Could you give me some questions on cell biology along with their answers?

I need practice questions on coding algorithms. Can you help?

Can you provide me with questions on world history for my upcoming exam?

Could you give me some physics questions without answers for quick practice?
"""


class QuestionsAgentModel(Model):
  topic: str = Field(
      'NA',
      title="Topic",
      description=(
          "Please specify the specific topic for which practice questions are requested. This should be a "
          "clear and concise string representing the subject matter. This value must be asked from user."
      ),
      example="Algebra"
  )
  with_answers: Literal['Yes', 'No'] = Field(
      'Yes',
      title="With Answers",
      description=(
          "Please indicate whether the practice questions should include answers. If set to 'Yes', "
          "the agent will provide questions along with their corresponding answers. If set "
          "to 'No', only questions will be provided. This value must be asked from user."
      ),
      example="Yes"
  )
  additional_requirements: str = Field(
      'NA',
      title="Additional Requirements",
      description=(
          "Please specify any additional requirements or preferences for the practice questions. This can include "
          "specifying the difficulty level, the number of questions needed, etc. This value must be asked from user."
      ),
      example="Include questions on advanced topics"
  )


questions_agent_protocol = Protocol("QuestionsAgentProtocol")


@questions_agent_protocol.on_message(model=QuestionsAgentModel, replies={UAgentResponse})
async def get_action(ctx: Context, sender: str, msg: QuestionsAgentModel):
  ctx.logger.info(f"📩 Incoming message from {sender}:")
  ctx.logger.info(f"👉 Data: {msg.json(indent=2)}")

  formatted_prompt = (
      "You are acting as a tool that helps students prepare practice questions and answers for various subjects and topics. "
      "The user specifies the topic for which they need practice questions, whether they require questions with or without answers, "
      "and any additional requirements or preferences they may have. Based on this information, you generate appropriate practice "
      "questions tailored to the student's needs to help them prepare effectively for exams and assessments.\n\n"
      "Given the provided data for the Questions Agent, your task is to prepare practice questions on the following:\n\n"
      f"- Topic: {msg.topic}\n"
      f"- With Answers: {msg.with_answers}\n"
      f"- Additional Requirements: {msg.additional_requirements}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to generate the practice questions accordingly."
  )
  ctx.logger.info(f'{formatted_prompt=}')

  message = (
      "This is a test message. Once the language model (LLM) is integrated, this will be replaced "
      "with the practice questions."
  )
  message = await get_llm_response(formatted_prompt)
  await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))


AGENT_NAME = 'questions_agent'
AGENT_PORT = 8002
AGENT_SEED = AGENT_NAME
AGENT_ENDPOINT = [f'http://localhost:{AGENT_PORT}/submit']
AGENT_MAILBOX_KEY = ""

questions_agent = Agent(name=AGENT_NAME,
                        seed=AGENT_SEED,
                        # port=AGENT_PORT,
                        # endpoint=AGENT_ENDPOINT,
                        # mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai"
                        )
questions_agent.include(questions_agent_protocol, publish_manifest=True)


@questions_agent.on_event("startup")
async def startup(ctx: Context):
  ctx.logger.info(f"🤖 Agent Address: {ctx.address}")

QUESTIONS_AGENT_ADDRESS = questions_agent.address

if __name__ == "__main__":
  questions_agent.run()
