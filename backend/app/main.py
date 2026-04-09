from fastapi import FastAPI

app = FastAPI(
    title="Digital You API",
    description="Autonomous AI agent that acts as your digital representative",
    version="0.1.0"
)

@app.get("/ping")
async def ping():
    return {
        "status": "ok", 
        "message": "Digital You API is alive!"
    }