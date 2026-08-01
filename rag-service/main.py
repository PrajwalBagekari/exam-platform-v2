from fastapi import FastAPI

from rag import RAG

app = FastAPI()

rag = RAG()


@app.post("/build")
def build(data: dict):

    print("=" * 60)
    print("RAG INPUT:")
    print(data)
    print("=" * 60)

    count = rag.build(data)

    return {
        "vectors": count
    }