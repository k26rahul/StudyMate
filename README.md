# Project Overview

Welcome to our project! Our goal is to develop a suite of intelligent agents to assist students with various academic tasks and provide career guidance. These agents leverage state-of-the-art language models to understand user queries and generate relevant responses. In this README, we'll provide a detailed overview of the project, including the functionality of each agent, the structure of the project files, and instructions on how to run the application.

## Agents

### 1. Notes Agent

The Notes Agent is designed to help students prepare comprehensive notes on different subjects and topics. It collects specific details from the user, such as the topic for which notes are needed, the preferred style of notes (short, detailed, or last-minute revision), any reference material, and additional requirements or focus areas. Based on this information, the agent generates tailored notes to assist students in studying effectively.

#### Fields:
- **Topic**: Specifies the subject matter for which notes are requested.
- **Notes Style**: Determines the preferred style of the notes (short, detailed, or last-minute revision).
- **Reference Material**: Indicates any reference material or sources to be used for note preparation.
- **Additional Requirements**: Specifies any additional requirements or focus areas for the notes.

### 2. Questions Agent

The Questions Agent provides practice questions and answers to help students prepare for exams and assessments. Users can specify the topic for which they need practice questions, whether they require questions with or without answers, and any additional requirements or preferences they may have. The agent then generates appropriate practice questions tailored to the student's needs.

#### Fields:
- **Topic**: Specifies the subject matter for which practice questions are requested.
- **With Answers**: Indicates whether the practice questions should include answers.
- **Additional Requirements**: Specifies any additional requirements or preferences for the practice questions.

### 3. Career Guidance Agent

The Career Guidance Agent offers personalized career guidance and advice to students based on their educational background, interests, and future goals. Users provide details such as their current education level, degree or class, field of interest, and future aspirations. The agent then provides recommendations tailored to the student's profile.

#### Fields:
- **Education Level**: Indicates whether the student is currently in school or college.
- **Degree/Class**: Specifies the student's degree (if in college) or class (if in school).
- **Field of Interest**: Specifies the student's area of interest (e.g., law, medicine, software engineering).
- **Future Goal**: Indicates whether the student's future goal is further studies or employment.

## File Structure

Our project repository has the following structure:

- **.env**: Environment variables file containing sensitive information (e.g., API keys). This file is not version-controlled.
- **.env.example**: Example environment variables file to guide users in setting up their own environment.
- **.gitignore**: File specifying patterns to be ignored by Git (e.g., `.env` file).
- **career_guidance_agent.py**: Python script defining the Career Guidance Agent model and functionality.
- **main.py**: Main script to run the application.
- **notes_agent.py**: Python script defining the Notes Agent model and functionality.
- **questions_agent.py**: Python script defining the Questions Agent model and functionality.
- **test_agent.py**: Python script containing test code.
- **utils.py**: Python script containing utility functions used in the project.

## How to Run It

To run the application, follow these steps:

1. **Set Up Virtual Environment**: Create a virtual environment to isolate project dependencies.
    ```bash
    python -m venv venv
    ```
2. **Activate Virtual Environment**: Activate the virtual environment.
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```
3. **Install Requirements**: Install the required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Main File**: Execute the `main.py` file to start the application.
    ```bash
    python main.py
    ```
In the `main.py` file, we create a bureau of agents using the `Bureau` class from the `uagents` module. The `Bureau` class manages a collection of agents and orchestrates their execution.

The bureau will handle the coordination and execution of the agents, allowing them to interact with each other and perform their designated tasks. This setup ensures seamless integration and operation of the agents within the system.

That's it! You should now have the project up and running, ready to assist students with their academic needs and career aspirations. Enjoy exploring the functionality of our intelligent agents!