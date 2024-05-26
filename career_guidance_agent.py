from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
from pydantic import Field
from typing import Literal
from utils import get_llm_response

# print("[StudyMate Career Guidance Agent] running.")

"""
StudyMate Career Guidance Agent

This agent is designed to provide career guidance and advice to students based on their 
educational background, interests, and future goals. Students can specify whether they are 
currently in school or college, their degree or class, their field of interest, and their 
goal for the future (e.g., further studies or employment). The agent will then offer tailored 
recommendations and advice to help students make informed decisions about their career path.

Hi, I'm currently in college studying computer science. Can you provide some career guidance 
in this field?

I'm in high school and interested in pursuing a career in medicine. Can you offer some advice 
on how to prepare for medical school?

I have completed my graduation in business administration and I'm confused about whether to 
pursue further studies or start working. Can you provide some guidance?

I'm passionate about environmental science and want to explore career opportunities in this 
field. Can you suggest some career paths and the required qualifications?

I'm a recent engineering graduate and looking for job opportunities in the field of renewable 
energy. Can you help me with some career advice and job search tips?
"""


class CareerGuidanceAgentModel(Model):
  education_level: Literal['School', 'College'] = Field(
      'School',
      title="Education Level",
      description=(
          "Please specify whether the student is currently in school or college. This value must be asked from user."
      ),
      example="College"
  )
  degree_or_class: str = Field(
      'NA',
      title="Degree/Class",
      description=(
          "Please specify the student's degree (if in college) or class (if in school). This value must be asked from user."
      ),
      example="Computer Science"
  )
  field_of_interest: str = Field(
      'NA',
      title="Field of Interest",
      description=(
          "Please specify the student's field of interest, such as law, medicine, software engineering, etc. "
          "This value must be asked from user."
      ),
      example="Data analysis"
  )
  future_goal: Literal['Further Studies', 'Employment'] = Field(
      'Employment',
      title="Future Goal",
      description=(
          "Please indicate whether the student's goal for the future is to pursue further studies "
          "or seek employment. This value must be asked from user."
      ),
      example="Further Studies"
  )


career_guidance_protocol = Protocol("CareerGuidanceAgentProtocol")


@career_guidance_protocol.on_message(model=CareerGuidanceAgentModel, replies={UAgentResponse})
async def get_action(ctx: Context, sender: str, msg: CareerGuidanceAgentModel):
  ctx.logger.info(f"📩 Incoming message from {sender}:")
  ctx.logger.info(f"👉 Data: {msg.json(indent=2)}")

  formatted_prompt = (
      "You are acting as a career guidance tool that assists students in making informed decisions "
      "about their education and future career paths. The user provides information about their current "
      "education level, degree or class, field of interest, and future goals. Based on this information, "
      "you provide personalized career guidance and advice to help students plan for their future.\n\n"
      "Given the provided data for the Career Guidance Agent, your task is to provide guidance based on the following:\n\n"
      f"- Education Level: {msg.education_level}\n"
      f"- Degree/Class: {msg.degree_or_class}\n"
      f"- Field of Interest: {msg.field_of_interest}\n"
      f"- Future Goal: {msg.future_goal}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to provide career guidance accordingly."
  )
  ctx.logger.info(f'{formatted_prompt=}')

  message = (
      "This is a test message. Once the language model (LLM) is integrated, this will be replaced "
      "with personalized career guidance and advice."
  )
  message = await get_llm_response(formatted_prompt)
  await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))


AGENT_NAME = 'career_guidance_agent'
AGENT_PORT = 8003
AGENT_SEED = AGENT_NAME
AGENT_ENDPOINT = [f'http://localhost:{AGENT_PORT}/submit']
AGENT_MAILBOX_KEY = ""

career_guidance_agent = Agent(name=AGENT_NAME,
                              seed=AGENT_SEED,
                              # port=AGENT_PORT,
                              # endpoint=AGENT_ENDPOINT,
                              # mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai"
                              )
career_guidance_agent.include(career_guidance_protocol, publish_manifest=True)


@career_guidance_agent.on_event("startup")
async def startup(ctx: Context):
  ctx.logger.info(f"🤖 Agent Address: {ctx.address}")

CAREER_GUIDANCE_AGENT_ADDRESS = career_guidance_agent.address

if __name__ == "__main__":
  career_guidance_agent.run()
