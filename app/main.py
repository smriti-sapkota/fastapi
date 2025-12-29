from fastapi import FastAPI
from .router import auth,post,user,vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ['*']

app.add.middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']


)


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
