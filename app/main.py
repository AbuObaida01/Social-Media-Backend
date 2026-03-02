from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, SessionLocal, get_db
from .router import user,post,auth,votes

models.Base.metadata.create_all(bind=engine)


app=FastAPI()



origin=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(votes.router)

# @app.get("/")
# def root():
#     return{"Hello":"Hello"}

