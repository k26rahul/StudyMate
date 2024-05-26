from uagents import Agent, Context
from ai_engine import UAgentResponse

from notes_agent import NotesAgentModel, NOTES_AGENT_ADDRESS
from questions_agent import QuestionsAgentModel, QUESTIONS_AGENT_ADDRESS
from career_guidance_agent import CareerGuidanceAgentModel, CAREER_GUIDANCE_AGENT_ADDRESS

notes_request_data = NotesAgentModel(
    topic="Photosynthesis",
    notes_style="Detailed",
    reference_material="NCERT Textbook of Class Twelve",
    additional_requirements="Include detailed explanations of the Calvin cycle and the light-dependent reactions"
)

questions_request_data = QuestionsAgentModel(
    topic="Data Analysis",
    with_answers="Yes",
    additional_requirements="Include questions on statistical analysis and machine learning algorithms"
)

career_guidance_request_data = CareerGuidanceAgentModel(
    education_level="College",
    degree_or_class="Computer Science",
    field_of_interest="Data Analysis",
    future_goal="Employment"
)


AGENT_NAME = 'test_agent'
AGENT_PORT = 8000
AGENT_SEED = AGENT_NAME
AGENT_ENDPOINT = [f'http://localhost:{AGENT_PORT}/submit']
AGENT_MAILBOX_KEY = ""

test_agent = Agent(name=AGENT_NAME,
                   seed=AGENT_SEED,
                   # port=AGENT_PORT,
                   # endpoint=AGENT_ENDPOINT,
                   # mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai"
                   )


@test_agent.on_event("startup")
async def startup(ctx: Context):
  ctx.logger.info(f"🤖 Agent Address: {ctx.address}")
  # await ctx.send(NOTES_AGENT_ADDRESS, notes_request_data)
  # await ctx.send(QUESTIONS_AGENT_ADDRESS, questions_request_data)
  # await ctx.send(CAREER_GUIDANCE_AGENT_ADDRESS, career_guidance_request_data)


# Define a list containing dictionaries for each agent
agent_requests = [
    {"name": "Notes Agent", "address": NOTES_AGENT_ADDRESS, "data": notes_request_data},
    {"name": "Questions Agent", "address": QUESTIONS_AGENT_ADDRESS, "data": questions_request_data},
    {"name": "Career Guidance Agent", "address": CAREER_GUIDANCE_AGENT_ADDRESS, "data": career_guidance_request_data}
]

# Initialize a pointer to keep track of the current request
current_request_index = 0


@test_agent.on_interval(period=0.5)
async def interval(ctx: Context):
  global current_request_index

  if current_request_index >= len(agent_requests):
    return

  current_request = agent_requests[current_request_index]
  await ctx.send(current_request["address"], current_request["data"])

  current_request_index += 1
  ctx.logger.info(f"📩 Sent request to {current_request['name']}")


@test_agent.on_message(model=UAgentResponse, replies=set())
async def receive_response(ctx: Context, sender: str, msg: UAgentResponse):
  agent_name = None
  if sender == NOTES_AGENT_ADDRESS:
    agent_name = "Notes Agent"
  elif sender == QUESTIONS_AGENT_ADDRESS:
    agent_name = "Questions Agent"
  elif sender == CAREER_GUIDANCE_AGENT_ADDRESS:
    agent_name = "Career Guidance Agent"

  ctx.logger.info(f"📩 Received response from {agent_name}:")
  ctx.logger.info(f"👉 Message: {msg.message}")


if __name__ == "__main__":
  test_agent.run()
