EVAL_DATASET_NAME = "llm_course_qa_pairs"
TEST_EVAL_DATASET_NAME = "llm_course_qa_pairs_test"
SYSTEM_PROMPT = "You are a teacher's assistant who provides answers by referencing video transcripts from recorded lectures. In addition to providing an accurate answer to the question, the response should provide which lecture week (e.g., Week 1, Week 2) this answer can be found and the timestamp of where this relevant information can be found within the recorded lecture (e.g., This was discussed in the recorded lecture from Week 1 at around the 1:09 mark)."
GENERATION_SYSTEM_PROMPT="""
Instructions:

- Generate **25** factual questions, each with a corresponding **expected_output**.
- There should be variations in the questions, based on how much knowledge is known about the lecture:
    LOW: "What topics were talked about during the lecture?", "Was there any assigned homework?"
    MEDIUM: "What LLM topics were discussed during Week 1?"
    HIGH: "What was said about how to deal with slow LLMs?", "What was the thing about Sunday midnight?"
- The expected output should consider this context when providing an answer: {system_prompt}
- Ensure all questions are directly related to the transcript.
- Provide additional information in the answers if you think it would make the answer more helpful.

You only respond in JSON using the following format:

[
  {{
    "question": "<question1>",
    "expected_output": "<answer1>. This was discussed in the recorded Week 1 lecture at around the 1:09 mark."
  }},
  {{
    "question": "<question2>",
    "expected_output": "<answer2>. This information can be found at various points throughout the recorded session from Week 2."
  }}
]
"""
GENERATION_NAME="llm-course-generation"
EVALUATION_PROMPT="""
You are tasked with evaluating the accuracy of a response to the following question:

Question: {input}
Response: {output}

Evaluate the response based on how much the response reflects the grounded truth in the following base answer:

Base Answer: {expected_output}

Provide a score ranging between 0.0 (inaccurate) and 1.0 (accurate) and a brief reason for your evaluation. 

- NEVER nitpick about minor differences in punctuation or formatting and focus on how grounded in truth the response is.
- If the response is generally correct but contains some inaccuracies, you can still assign a partial score.
- If the reference timestamps are off by a few seconds, it should not significantly affect the score.
Return your response in the following JSON format:
{{
    "score": 0.0-1.0,
    "reason": "Your explanation here"
}}
"""