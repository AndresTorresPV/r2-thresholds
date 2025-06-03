from fastapi import FastAPI, HTTPException, Request
from Process.Hero import Hero, heroes
import pandas as pd

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

# Traducción de los niveles de R² al español

# Escala de clasificación de R²
r2_classification_scale = ["Muy débil", "Débil", "Moderada", "Fuerte", "Muy fuerte"]

levels_dictionary = {
    "Muy fuerte": "Very Strong",
    "Fuerte": "Strong",
    "Moderada": "Moderate",
    "Débil": "Weak",
    "Muy débil": "Very Weak"
}

# Cargar los archivos una sola vez
r2_thresholds = {
    "idt_idc": pd.read_csv("Thresholds/idt_idc.csv", index_col="f"),
    "idl_ial": pd.read_csv("Thresholds/idl_ial.csv", index_col="f")
}

x_strings = {
    "idt_idc": "Índice de la Transacción",
    "idl_ial": "Índice del Liderazgo"
}

y_strings = {
    "idt_idc": "Índice del Compromiso",
    "idl_ial": "Índice del Ambiente Laboral"
}

# Define los tipos de funciones válidos
f_types = ["lin", "exp", "log", "pot"]
f_strings = ["lineal", "exponencial", "logarítmico", "potencial"]

def classify_r2(x: str, y: str, f: str, r2: float) -> str:
    print("🔍 Parámetros recibidos:")
    print(f"x = {x}, y = {y}, f = {f}, r2 = {r2}")

    if r2 < 0 or r2 > 1:
        print("❌ R2 fuera de rango.")
        return "El valor de R² debe estar entre 0 y 1"
    
    x = x.lower()
    y = y.lower()
    f = f.lower()
    thresholds_key = f"{x}_{y}".lower()

    print(f"📊 Llave thresholds: {thresholds_key}")

    if thresholds_key not in r2_thresholds:
        print(f"⚠️ Umbrales no encontrados para {thresholds_key}")
        return f"No se encontraron umbrales para x={x}, y={y}."
    
    selected_thresholds = r2_thresholds[thresholds_key]
    x_string = x_strings[thresholds_key]
    y_string = y_strings[thresholds_key]

    try:
        f_index = f_types.index(f)
        f_string = f_strings[f_index]
    except ValueError as e:
        print("❌ Tipo de función inválido:", f)
        return "Tipo de función inválido. Usa lin, exp, log o pot."

    print("🧠 Procesando niveles...")

    for level in list(levels_dictionary.keys()):  # reversed con print
        valor_umbral = selected_thresholds[levels_dictionary[level]]
        print(f"Comparando R²={r2:.2f} con umbral para {level}: {valor_umbral.values[0]}")
        if r2 >= valor_umbral.values[0]:
            print(f"✅ Clasificado como: {level}")
            return f"Un R² = {r2:.2f} proveniente de un ajuste {f_string} entre el {x_string} *_(x)_* y el {y_string} *_(y)_* comunica una correlación *{level}*"

    print("⬇️ Clasificación más baja usada.")
    return f"Un R² = {r2:.2f} proveniente de un ajuste {f_string} entre el {x_string} *_(x)_* y el {y_string} *_(y)_* comunica una correlación *{r2_classification_scale[0]}*"


@app.post("/")
async def recibir_evento(request: Request):
    evento = await request.json()
    texto = evento.get("message", {}).get("text", "").strip()

    try:
        partes = {}
        for parte in texto.split():
            if "=" in parte:
                k, v = parte.split("=", 1)
                partes[k.strip().lower()] = v.strip().lower()

        x = partes["x"]
        y = partes["y"]
        f = partes["f"]
        r2 = float(partes["r2"])

        #respuesta = f"x={x}, y={y}, f={f}, r2={r2}"

        respuesta = classify_r2(x, y, f, r2)

    except Exception as e:
        respuesta = (
            "Formato incorrecto. Usa por ejemplo:`x=idt y=idc f=lin r2=0.65`. Tipos de función válidos: lin, exp, log, pot"
        )
        print("Error:", str(e))

    return {"text": respuesta}

if __name__ == "__main__":
    print("🧪 Ejecutando prueba local de classify_r2...\n")
    prueba = classify_r2("idt", "idc", "exp", 1)
    print("\n🧾 Resultado:", prueba)
