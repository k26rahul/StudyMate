from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

# from notes_agent import NotesAgentModel
# from questions_agent import QuestionsAgentModel
# from career_guidance_agent import CareerGuidanceAgentModel
from utils import get_llm_response

app = FastAPI()


class NotesRequest(BaseModel):
  topic: str
  notes_style: Literal['Short', 'Detailed', 'Last-minute revision']
  reference_material: str
  additional_requirements: str


class QuestionsRequest(BaseModel):
  topic: str
  with_answers: Literal['Yes', 'No']
  additional_requirements: str


class CareerGuidanceRequest(BaseModel):
  education_level: str
  degree_or_class: str
  field_of_interest: str
  future_goal: str


@app.post("/notes")
async def generate_notes(request: NotesRequest):
  formatted_prompt = (
      "You are acting as a tool that helps students prepare notes for various subjects and topics. "
      "The user supplies specific details such as the topic they need notes on, the preferred style "
      "of the notes (short, detailed, or last-minute revision), any reference material, and additional "
      "requirements or focus areas for the notes. Based on this information, you generate concise and "
      "tailored notes to assist students in studying effectively and efficiently.\n\n"
      "Given the provided data for the Notes Agent, your task is to prepare notes on the following:\n\n"
      f"- Topic: {request.topic}\n"
      f"- Notes Style: {request.notes_style}\n"
      f"- Reference Material: {request.reference_material}\n"
      f"- Additional Requirements: {request.additional_requirements}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to generate the notes accordingly."
  )

  try:
    response = await get_llm_response(formatted_prompt)
    return {"response": response}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/questions")
async def generate_questions(request: QuestionsRequest):
  formatted_prompt = (
      "You are acting as a tool that helps students by providing practice questions and answers. "
      "Users specify the topic for which they need practice questions, whether they require questions "
      "with or without answers, and any additional requirements or preferences they may have. You generate "
      "appropriate practice questions tailored to the student's needs to help them prepare effectively for exams and assessments.\n\n"
      "Given the provided data for the Questions Agent, your task is to prepare questions on the following:\n\n"
      f"- Topic: {request.topic}\n"
      f"- With Answers: {request.with_answers}\n"
      f"- Additional Requirements: {request.additional_requirements}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to generate the questions accordingly."
  )

  try:
    response = await get_llm_response(formatted_prompt)
    return {"response": response}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/career-guidance")
async def generate_career_guidance(request: CareerGuidanceRequest):
  formatted_prompt = (
      "You are acting as a career guidance tool that helps students navigate their education and career paths. "
      "The user supplies specific details such as their current education level, degree or class, field of interest, "
      "and future goals. Based on this information, you provide personalized career guidance and advice to assist them "
      "in making informed decisions about their academic and professional future.\n\n"
      "Given the provided data for the Career Guidance Agent, your task is to provide guidance on the following:\n\n"
      f"- Education Level: {request.education_level}\n"
      f"- Degree or Class: {request.degree_or_class}\n"
      f"- Field of Interest: {request.field_of_interest}\n"
      f"- Future Goal: {request.future_goal}\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to provide the guidance accordingly."
  )

  try:
    response = await get_llm_response(formatted_prompt)
    return {"response": response}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="localhost", port=8000)
