from logging import getLogger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config import setting
from src.router import router as rt
from src.database import (
    engine,
    Base,
)
from src.service import (
    load_data, 
    write_data
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[setting.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/image", StaticFiles(directory="image"), name="image")
app.include_router(router=rt)
logger = getLogger("uvicorn.app")


@app.on_event("startup")
def startup():
    migrate()
    try:
        logger.info("start load data")
        data = load_data()
        logger.info("finish load data")
        # logger.info(data)
        logger.info("start write data")
        write_data(data[0], data[1])
        logger.info("finish write data")
    except Exception as e:
        logger.info(e)
        pass

def migrate():
    logger.info("create tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("migrate done.")
    except Exception as e:
        logger.info(e)
        pass
