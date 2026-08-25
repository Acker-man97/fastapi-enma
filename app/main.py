from fastapi import FastAPI
from .router import posts, users , auth , likes , comments
from . import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {
        "message": "Hello, World!"
    }

              