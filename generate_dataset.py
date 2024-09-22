# Import necessary libraries
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI
import json

client = OpenAI()

# Function to generate questions and answers
def generate_qa(prompt, text, temperature=0.2):    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}],
        temperature=temperature,
    )
    
    print(response.choices[0].message.content)

    # Strip extraneous symbols from the response content
    content = response.choices[0].message.content.strip()
    
    # Remove potential JSON code block markers
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[-1]
    if content.endswith('```'):
        content = content.rsplit('\n', 1)[0]
    content = content.strip()
    
    # Attempt to parse the cleaned content as JSON
    try:
        parsed_content = json.loads(content.strip())
        return parsed_content
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON. Raw content:")
        print(content)
        return []

factual_prompt = """
You are tasked with generating questions and answers using class notes, video transcripts, etc. as reference. These questions should focus on retrieving specific details that were discussed during the class. In addition to providing an accurate answer to the question, the response should provide a timestamp of where in the video recording this relevant information can be found. These should reflect the type of questions a student might ask after attending the class and they want to review the material or re-watch a specific part of the recorded lecture.

Instructions:

- Generate **10** factual questions, each with a corresponding **expected_output**.
- Ensure all questions are directly related to the transcript.
- Present the output in the following structured JSON format:

[
  {
    "question": "<question1>",
    "expected_output": "<answer1>. This was discussed in the recorded lecture at around the 1:09 mark."
  },
  {
    "question": "<question2>",
    "expected_output": "<answer2>. You can listen to this discussion at 3:05 in the lecture video."
  }
]
"""

# Generate dataset
import os
import json

# Retrieve context
with open('data/llm_bootcamp_week1_transcript.txt', 'r') as file:
    text = file.read()

# Generate dataset if local file doesn't exist
dataset = generate_qa(factual_prompt, text, temperature=0.2)
        
# Note: we're choosing to create the dataset in Langfuse below, but it's equally easy to create it in another platform.

from langfuse import Langfuse
langfuse = Langfuse()

dataset_name = "llm_course_qa_pairs"
langfuse.create_dataset(
    name=dataset_name, 
    );

for item in dataset:
  langfuse.create_dataset_item(
      dataset_name=dataset_name,
      input=item["question"],
      expected_output=item["expected_output"],
      metadata={
        "date": "2024-09-10",
        "tags": "lecture,week1"
        }
)