from fastapi import FastAPI

from api.api import spimex_routers


app = FastAPI()


app.include_router(spimex_routers)
