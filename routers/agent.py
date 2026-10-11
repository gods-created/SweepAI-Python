from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse

from exceptions import UnicornException
from validators import ToVectorsActionScheme

from strands import Agent
from strands.types.exceptions import ConcurrencyException

from json import loads, JSONDecodeError
from asyncio import sleep

async def if_agent_exists(request: Request):
    if not hasattr(request.app.state, 'agent'):
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description='AI Agent is not initialized'
        )

async def evaluate_action_response(agent: Agent, prompt: str) -> JSONResponse:
    agent.state.set('status', 'running')

    result = await agent.invoke_async(prompt=prompt)
    agent_response = result.message.get('content', [{}])[0].get('text', str(result))

    try:
        agent_response = loads(agent_response)
    
    except JSONDecodeError:
        pass

    agent.state.set('status', 'ready')
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': True,
            'err_description': None,
            'data': agent_response
        }
    )

router = APIRouter(
    prefix='/agent',
    tags=['AGENT'],
    default_response_class=JSONResponse,
    dependencies=[Depends(if_agent_exists)]
)

@router.post('/evaluate', response_class=JSONResponse)
async def evaluate_action(
    request: Request,
    data: ToVectorsActionScheme,
) -> JSONResponse:
    agent: Agent = request.app.state.agent 

    while agent.state.get('status') == 'running':
        await sleep(10)

    prompt = f'''
        code1: {data.code1},
        code2: {data.code2}
    '''

    return await evaluate_action_response(agent, prompt)