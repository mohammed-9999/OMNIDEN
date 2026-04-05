from fastapi import FastAPI

app = FastAPI(title="Omniden API")

@app.get("/")
def read_root():
    return {"message": "API Omniden en ligne"}
