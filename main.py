from fastapi import FastAPI, HTTPException
from Process.Hero import Hero, heroes

app = FastAPI()

@app.get("/")
def root():
    return {"API Name": "R2 API", 
            "Version": "1.0", 
            "Description": "This API provides the R2 value."}

@app.get("/heroes", response_model=Hero)
def list_heroes(limit: int = 10, offset: int = 0):
    """
    Returns a list of heroes.
    """
    return heroes[offset:offset + limit]

@app.get("/heroes/{hero_id}", response_model=Hero)
def get_hero(hero_id: int):
    """
    Returns a hero by its ID.
    """
    if 0 <= hero_id < len(heroes):
        return heroes[hero_id]
    else:
        http_error = 404
        raise HTTPException(status_code=http_error, detail=f"{http_error}: Hero {hero_id} not found")
    
@app.post("/new_hero")
def create_item(hero: Hero):
    """
    Creates a Hero with the given payload.
    """
    heroes.append(hero)
    return {"message": "Hero created successfully", "hero": hero}