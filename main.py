from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from contextlib import asynccontextmanager

from middlewares import ForbiddenPagesMiddleware
from exceptions import UnicornException
from routers import agent_router, action_router
from services import AgentInitService
from config import *

from loguru import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not all((
            OLLAMA_HOST_NAME,
            OLLAMA_MODEL_ID,
            SYSTEM_PROMPT
        )):
            raise ValueError('One of the required parameters for agent initializing is not specified')

        agent_service = AgentInitService(
            ollama_host_name=OLLAMA_HOST_NAME,
            ollama_model_id=OLLAMA_MODEL_ID,
            system_prompt=SYSTEM_PROMPT
        )

        agent = agent_service()

        app.state.agent = agent

    except ValueError as e:
        logger.error(str(e))

    except Exception as e:
        logger.error(f'Unexpected error during launching server: {str(e)}')

    yield

app = FastAPI(
    title='SweepAI-Python',
    description='Compare Python code using an AI Agent or other quick code-checking tools',
    version='0.0.1',
    lifespan=lifespan,
    redoc_url=None,
    docs_url='/api/docs'
)

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=['Content-Type'],
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE']
)

app.add_middleware(
    ForbiddenPagesMiddleware
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'status': False,
            'err_description': str(exc.detail) if exc.status_code != 404 else 'Path doesn\'t exist'
        }
    )

@app.exception_handler(RequestValidationError)
async def validate_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    err_description = exc.errors()[0].get('msg')

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'status': False,
            'err_description': err_description
        }
    )

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'status': False,
            'err_description': exc.err_description
        }
    )

app.include_router(router=agent_router, prefix='/api', tags=['API'])
app.include_router(router=action_router, prefix='/api', tags=['API'])

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def main_page(request: Request):
    return templates.TemplateResponse(request, name='pages/main.html', context={})

# python -m uvicorn main:app --host=0.0.0.0 --port=8001 --reload --proxy-headers