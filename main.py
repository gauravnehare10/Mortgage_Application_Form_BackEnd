from fastapi import FastAPI
from routes import mortgage, user_auth
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(mortgage.router)
app.include_router(user_auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)