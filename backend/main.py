from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import ads_keywords, listings


# створюємо таблиці, якщо ще немає
Base.metadata.create_all(bind=engine)

# app = FastAPI(title='My Etsy helper API')
app = FastAPI(title='My API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # або ["http://localhost:3000"] якщо фронт на React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#todo налаштувати allow_origins більш безпечно (не "*"), щоб у продакшені не було зайвих ризиків


# підключаємо роут
app.include_router(ads_keywords.router)
app.include_router(listings.router)


# @app.get("/")
# def root():
#     return {"message": "Hello from FastAPI backend"}
