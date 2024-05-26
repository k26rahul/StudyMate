import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-pro")


async def get_llm_response(prompt: str) -> str:
  """
  Function to make a request to LLM and return the response.

  Args:
      prompt (str): The prompt for LLM.

  Returns:
      str: The response from LLM.
  """
  print("Starting LLM request...")

  # Make a request to LLM
  response = llm.invoke(prompt)

  print("LLM request finished.")

  # Return the LLM response
  return response.content


async def test_llm_response():
  # Sample prompt
  prompt = (
      "You are acting as a tool that helps students prepare notes for various subjects and topics. "
      "The user supplies specific details such as the topic they need notes on, the preferred style "
      "of the notes (short, detailed, or last-minute revision), any reference material, and additional "
      "requirements or focus areas for the notes. Based on this information, you generate concise and "
      "tailored notes to assist students in studying effectively and efficiently.\n\n"
      "Given the provided data for the Notes Agent, your task is to prepare notes on the following:\n\n"
      "- Topic: Photosynthesis\n"
      "- Notes Style: Detailed\n"
      "- Reference Material: NCERT Textbook of Class Twelve\n"
      "- Additional Requirements: Include detailed explanations of the Calvin cycle and the light-dependent reactions\n\n"
      "Note: If any information is missing (marked as 'NA'), please use intelligent reasoning to generate the notes accordingly."
  )

  # Get LLM response
  response = await get_llm_response(prompt)

  # Print LLM response
  print(response)


# Check if the file is executed directly
if __name__ == "__main__":
  # Run the test function
  asyncio.run(test_llm_response())
