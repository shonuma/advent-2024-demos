FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PROJECT_ID=<%PROJECT_ID%>
ENV REGION=us-central1

ENV GRADIO_SERVER_PORT=8080
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]
