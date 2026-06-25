FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]