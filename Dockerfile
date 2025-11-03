# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu proyecto al directorio de trabajo
COPY . .

EXPOSE 80

# Comando para ejecutar la aplicación con Uvicorn[citation:2]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]