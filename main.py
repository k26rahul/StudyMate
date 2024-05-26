from uagents import Bureau
from notes_agent import notes_agent
from questions_agent import questions_agent
from career_guidance_agent import career_guidance_agent
from test_agent import test_agent

bureau = Bureau()
bureau.add(notes_agent)
bureau.add(questions_agent)
bureau.add(career_guidance_agent)
bureau.add(test_agent)
bureau.run()
