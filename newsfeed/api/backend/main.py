from fastapi import FastAPI
# Local imports
from popular.routes import router as popular_router

# Instanciate the API controller
app = FastAPI(
    title="NyNews",
    description="API du projet New-York Times du Bootcamp DE de février 2023",
    version="1.0.1",
    openapi_tags=[
        {"name": "Popular"},
    ],
)

# Inject endpoints in the scope of the controller
app.include_router(popular_router, tags=["Popular"], prefix="/popular")


# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the NyNews API!"}


if __name__ == "__main__":
    # DEV MODE: start local server for testing
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
