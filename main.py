from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("Accept")
    api_key = request.headers.get("x-api-key")

    if accept_header not in ["text/html", "text/plain"]:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Type de réponse non supporté. Seuls 'text/html' ou 'text/plain' sont acceptés."
            }
        )

    if api_key != "12345678":
        return JSONResponse(
            status_code=403,
            content={
                "error": "Clé API non reconnue. Accès refusé."
            }
        )

    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=200,
        media_type="text/html"
    )

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=404,
        media_type="text/html"
    )

class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str

events_store: List[EventModel] = []

def serialized_stored_events():
    return [event.model_dump() for event in events_store]

@app.get("/events")
def list_events():
    return {"events": serialized_stored_events()}

@app.post("/events")
def add_events(events: List[EventModel]):
    events_store.extend(events)
    return {"events": serialized_stored_events()}

@app.put("/events")
def update_events(events: List[EventModel]):
    for new_event in events:
        existing = [e for e in events_store if e.name == new_event.name]
        if existing:
            events_store.remove(existing[0])
        events_store.append(new_event)
    return {"events": serialized_stored_events()}


# append(x) : Ajoute un élément à la fin
# extend(iterable) : Ajoute plusieurs éléments
# insert(i, x) : Insère un élément à une position donnée
# remove(x) : Supprime la 1re occurrence de x
# pop(i) : Supprime et retourne l’élément à l’indice i (ou le dernier si omis)
# clear() : Supprime tous les éléments
# index(x) : Donne l’indice de la 1re occurrence de x
# count(x) : Compte le nombre d’occurrences de x
# sort() : Trie la liste (sur place)
# reverse() : Inverse la liste (sur place)
# copy() : Fait une copie superficielle de la liste