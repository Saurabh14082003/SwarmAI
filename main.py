from fastapi import FastAPI
from pydantic import BaseModel
from graph.build_graph import build_graph

app = FastAPI()

graph = build_graph()

class Query(BaseModel):
    query: str

@app.post("/chat")
def chat(query: Query):

    state = {
        "query": query.query,
        "messages": [],
        "plan": [],
        "completed_steps": []
    }

    result = graph.invoke(state)

    return {"answer": result["final_answer"]}


@app.get("/")
def home():
    return {"status":