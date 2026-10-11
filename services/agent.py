from strands import Agent, tool
from strands.models.ollama import OllamaModel

from .runCode import runCodeService
from .toVectors import toVectorsService
from .compareVectors import compareVectorsService

from typing import List

@tool
def run_code_tool(
    code: str
) -> dict:
    '''
        Create a file with Python code and run it to see the result of the code execution
        Args:
            code: to receive the result of the execution
    '''

    return runCodeService(code=code)

@tool
def to_vectors_tool(
    code1: str,
    code2: str
) -> List[List[float]]:
    '''
        Converts text into a vector value for further comparison of vectors.
        Args:
            code1: the first version of the code (solution to the problem) or the result of the execution
            code2: the second version of the code (solution to the problem) or the result of the execution
    '''

    return toVectorsService(code1=code1, code2=code2)

@tool
def compare_vectors_tool(
    vectors: List[List[float]]
) -> float:
    '''
        Comparing the similarity of vectors to determine whether the user has completed the task correctly
        Args:
            vectors: a list consisting of two vectors (from code1 and code2)
    '''

    return compareVectorsService(vectors=vectors)
    
class AgentInitService:
    def __init__(
        self,
        ollama_host_name: str,
        ollama_model_id: str,
        system_prompt: str
    ):
        self._ollama_host_name = ollama_host_name
        self._ollama_model_id = ollama_model_id
        self._system_prompt = system_prompt

    def __call__(self) -> Agent:
        return Agent(
            model=OllamaModel(
                host=self._ollama_host_name,
                model_id=self._ollama_model_id
            ),
            tools=[run_code_tool, to_vectors_tool, compare_vectors_tool],
            system_prompt=self._system_prompt
        )