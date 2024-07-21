import uvicorn
from fastapi import FastAPI

from routes import router as books_router
from routes import user_router
from models import entities
from database import engine

app = FastAPI()

entities.Base.metadata.create_all(bind=engine)

app.include_router(books_router)
app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
