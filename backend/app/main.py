from fastapi import FastAPI

from app.interfaces.api.routes.auth import router as auth_router

app = FastAPI(title="LocPlus API")
app.include_router(auth_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"service": "locplus-backend"}
