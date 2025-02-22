from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.routes.main import api_router
from app.config.config import settings

######################################################## start DB
from app.start.backend_pre_start import main as init_db
from app.start.initial_data import main as initial_data

init_db()
initial_data()
######################################################## end DB

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

print(f"Usando o modelo: {settings.BASE_NAME_CHAT_MODEL}")
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo(a) ao backend do assistente de IA!",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
    }


app.include_router(api_router, prefix=settings.API_V1_STR)
