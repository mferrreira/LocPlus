from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="LocPlus API")
app.include_router(router, prefix="/api")

@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"service": "locplus-backend"}
