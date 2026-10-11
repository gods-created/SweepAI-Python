from fastapi import APIRouter, Request, Query, status
from fastapi.responses import JSONResponse

from services import runCodeService, toVectorsService, compareVectorsService, getAdviceService
from validators import RunCodeActionScheme, ToVectorsActionScheme, CompareVectorsActionScheme
from exceptions import UnicornException

router = APIRouter(
    prefix='/action',
    tags=['ACTION'],
    default_response_class=JSONResponse
)

@router.post('/run_code', response_class=JSONResponse)
async def run_code_action(
    request: Request,
    data: RunCodeActionScheme
) -> JSONResponse:
    try:
        result = runCodeService(code=data.code)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': True,
                'err_descritpion': None,
                'data': {
                    'result': result
                }
            }
        )

    except Exception as e:
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description=str(e)
        )

@router.post('/to_vectors', response_class=JSONResponse)
async def to_vectors_action(
    request: Request,
    data: ToVectorsActionScheme
) -> JSONResponse:
    try:
        vectors = toVectorsService(code1=data.code1, code2=data.code2)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': True,
                'err_descritpion': None,
                'data': {
                    'vectors': vectors
                }
            }
        )

    except Exception as e:
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description=str(e)
        )

@router.post('/compare_vectors', response_class=JSONResponse)
async def compare_vectors_action(
    request: Request,
    data: CompareVectorsActionScheme
) -> JSONResponse:
    try:
        score = compareVectorsService(vectors=[data.vector1, data.vector2])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': True,
                'err_descritpion': None,
                'data': {
                    'score': score
                }
            }
        )

    except Exception as e:
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description=str(e)
        )

@router.get('/get_advice', response_class=JSONResponse)
async def get_advice_action(
    request: Request,
    score: float = Query(default=0.0)
) -> JSONResponse:
    try:
        if score <= 1.0:
            score = score * 100

        advice = getAdviceService(score_in_percent=score)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': True,
                'err_descritpion': None,
                'data': {
                    'advice': advice
                }
            }
        )

    except Exception as e:
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description=str(e)
        )