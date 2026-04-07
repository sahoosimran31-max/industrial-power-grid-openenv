# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirement files first (for faster building)
COPY pyproject.toml pdm.lock* uv.lock* ./

# 4. Install dependencies 
# We use pip here to keep the container lightweight
RUN pip install --no-cache-dir fastapi uvicorn pydantic openenv-core

# 5. Copy the rest of your project code
COPY . .

# 6. Expose the port your server runs on
EXPOSE 8000

# 7. The command to start your server
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]