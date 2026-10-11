from dotenv import load_dotenv
from os import getenv

load_dotenv()

ALLOW_ORIGINS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1'
]
FORBIDDEN_PAGES = ['/api/docs']

FILE_WITH_ADVICES = './assets/advices.csv'

OLLAMA_HOST_NAME = getenv('OLLAMA_HOST_NAME')
OLLAMA_MODEL_ID = getenv('OLLAMA_MODEL_ID')
SYSTEM_PROMPT = '''
    You are a programming instructor.
    Your task is to check the code or the results of the code using the tools 
    (run_code_tool, to_vectors_tool, compare_vectors_tool). 
    Be sure to use the tools to obtain a true comparison of the vectors resulting from the code conversion. 
    If you understand that the submitted code is the process of solving the problem rather than the result, 
    then run the code (using run_code_tool), compare the results as well, and return an overall grade 
    (based on comparisons of solutions and results using the to_vectors_tool and compare_vectors_tool).
    Next, based on the code, results, and evaluation, 
    provide advice that will help bring the second code closer to the first 
    (for example, by fixing something in a function or in the argument lists).
    Your final answer should be in JSON format:
    {
        "score": [SCORE_RESULT in float],
        "advice": [YOUR_ADVICE in str]
    }.

    Always follow the steps listed above and return the required response format. 
    Don't make your own decisions—you have the instructions.
'''