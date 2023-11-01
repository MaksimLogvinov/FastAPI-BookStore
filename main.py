import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import settings
from api.authors import router as author_router
from api.books import router as book_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

load_dotenv()
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )

app.include_router(
    router=book_router,
    prefix='/book'
)

app.include_router(
    router=author_router,
    prefix='/author'
)


@app.get('/')
async def root() -> dict:
    return {'message': 'Hello World'}


@app.post('/test-login')
async def test_login(response: Response) -> None:
    response.set_cookie(
        key='faketoken', value=settings.Token.authjwt_secret_key, httponly=True
    )
    logging.log(51, 'Токен успешно выдан')
    return None


@app.get('/hello/{name}')
async def say_hello(name: str) -> dict:
    return {'message': f'Hello {name}'}


@app.middleware('http')
async def check_token(request: Request, call_next) -> Response:
    if 'faketoken' not in request.cookies:
        logging.log(51, 'Токен отсутсвует')
    response = await call_next(request)
    return response
