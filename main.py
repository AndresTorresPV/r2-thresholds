from fastapi import FastAPI, HTTPException, Request
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


def interpretar_r2(r2: float, tipo_funcion: str) -> str:
    if r2 < 0 or r2 > 1:
        return "El valor de R² debe estar entre 0 y 1."
    
    interpretacion_base = ""
    if r2 >= 0.9:
        interpretacion_base = "excelente ajuste"
    elif r2 >= 0.75:
        interpretacion_base = "muy buen ajuste"
    elif r2 >= 0.5:
        interpretacion_base = "ajuste moderado"
    else:
        interpretacion_base = "pobre ajuste"

    return f"La función {tipo_funcion} tiene un {interpretacion_base} (R² = {r2:.2f})."

@app.post("/")
async def recibir_evento(request: Request):
    evento = await request.json()
    texto = evento.get("message", {}).get("text", "").strip()

    try:
        # Divide por espacios y luego por "="
        partes = {}
        for parte in texto.split():
            if "=" in parte:
                k, v = parte.split("=", 1)
                partes[k.strip().lower()] = v.strip().lower()
        
        r2_str = partes.get("r2")
        tipo = partes.get("tipo")
        
        if r2_str is None or tipo is None:
            raise ValueError("Faltan parámetros")
        
        r2 = float(r2_str)
        if tipo not in ["lineal", "exponencial", "logarítmica", "potencial"]:
            raise ValueError("Tipo inválido")

        respuesta = interpretar_r2(r2, tipo)

    except Exception as e:
        print("❌ Error:", str(e))  # Para ver en consola local
        respuesta = ("Formato incorrecto. Usa:\n"
                     "`R2=0.87 tipo=lineal`\n"
                     "Tipos válidos: lineal, exponencial, logarítmica, potencial.")

    return {"text": respuesta}

# Para pruebas locales
#if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8080)
