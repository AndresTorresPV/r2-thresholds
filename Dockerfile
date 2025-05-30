FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia archivos al contenedor
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa Uvicorn
EXPOSE 8080

# Comando para correr el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
