# SweepAI-Python

A service for comparing two Python solutions using an AI agent and calculating their “similarity.” The project combines FastAPI, a local Ollama model, and text/code vector comparison methods to assess how similar two code snippets are and provide recommendations for improvement.

## What kind of project is this

This web application allows you to:

- compare two solutions to the same problem;
- run Python code on the server and get the execution result;
- convert source code or program output into vectors using TF-IDF;
- compare vectors using cosine similarity;
- receive suggestions for improving your solution based on the final score;
- use an Ollama-based AI agent to evaluate code using various tools.

The idea behind the project is not just to check syntax, but to assess the semantic similarity between two solutions and help you understand what needs to be corrected in the second version to bring it closer to the benchmark.

## Main Workflow

The user submits two code snippets:

- `code1` — the reference or correct solution;
- `code2` — the version being tested.

The app can then:

1. execute both code snippets;
2. convert them into vectors;
3. compare the vectors and generate a numerical score;
4. select a piece of advice from `assets/advices.csv` based on the score;
5. or pass the task to an AI agent, which uses the tools `run_code_tool`, `to_vectors_tool`, and `compare_vectors_tool`.

## Technology Stack

- Python 3
- FastAPI
- Jinja2
- Pydantic
- Strands Agents
- Ollama
- scikit-learn
- pandas
- python-dotenv
- loguru

## Project Architecture

### `main.py`
The main entry point for the application. This is where an instance of FastAPI is created, middleware, error handlers, and routers are configured, and the AI agent is initialized when the server starts.

### `config.py`
Contains application settings and environment variables, including:

- `OLLAMA_HOST_NAME`
- `OLLAMA_MODEL_ID`
- `SYSTEM_PROMPT`
- path to CSV-file with advices `FILE_WITH_ADVICES`

### `routers/`
Routers for API:

- `routers/agent.py` — requests to AI-agent;
- `routers/action.py` — actions for code launching, creating vectors, comparing and giving advices.

### `services/`
Business Process Logic:

- `runCode.py` — runs Python code in a temporary file;
- `toVectors.py` — converts text/code into TF-IDF vectors;
- `compareVectors.py` — compares vectors using cosine similarity;
- `getAdvice.py` — selects a random piece of advice based on a score range;
- `agent.py` — registers tools and initializes the agent.

### `validators/`
Pydantic-schemes of requests for validation income data.

### `assets/`

- `advices.csv` — a guide to tips and score ranges;
- `temporary_files/` — temporary files used when the code is run.

### `templates/` и `static/`
Web interface templates and static resources.

## API

The main endpoints are located in the prefix `/api`.

### AI-agent

- `POST /api/agent/evaluate`
  Send `code1` и `code2` to agent, who can use tools for comparing results.

### Actions

- `POST /api/action/run_code`
  Runs the provided Python code and returns stdout, stderr, and the return code.

- `POST /api/action/to_vectors`
  Converts two code snippets into vectors.

- `POST /api/action/compare_vectors`
  Compares two vectors and returns a score.

- `GET /api/action/get_advice?score=...`
  Returns a suggestion based on the rating.

### API docs

- Swagger UI: `/api/docs`

### Main page

- `/` — Application HTML-page

## Settings and start

### 1. Install dependencies

```bash
python -m pip install --no-cache-dir --upgrade -r requirements.txt
```

### 2. Turn on `.env`

Create `.env` file into project root and write in variables:

```env
OLLAMA_HOST_NAME=http://localhost:11434
OLLAMA_MODEL_ID=llama3.2
```

Confirm, that Ollama local launched and model is an avialable.

### 3. Start application

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Open next addresses:

- `http://localhost:8001/`
- Swagger: `http://localhost:8001/api/docs`

## How the Evaluation Works

The project calculates the score as follows:

- The code is converted into vectors using TF-IDF;
- The vectors are compared using cosine similarity;
- The final value falls within the range of 0.0 to 1.0;
- Then, `getAdviceService` is used to select advice based on the score’s percentage range.

The AI agent can also run the code and evaluate its output to take into account not only the text of the solution but also the program’s actual result.

## Example Scenario

1. The user submits two solutions to a problem.
2. The system runs both solutions, if necessary.
3. It compares the texts/outputs using vectors.
4. It calculates the similarity score.
5. It returns:

```json
{
  “score”: 0.87,
  “advice”: “Check your use of variables and improve the function’s logic.”
}
```

## Notes

- Access to Ollama is required for AI evaluation.
- All temporary files used to run the code are stored in `assets/temporary_files/` and are deleted after execution.
- Data containing advice is stored in CSV format and used to generate recommendations.

## License

MIT License
