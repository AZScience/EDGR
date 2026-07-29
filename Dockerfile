# EDGR FastAPI + built React SPA (/ui/)
# Deploy this image to Railway / Render / Fly — then point Streamlit
# Secrets EDGR_PUBLIC_UI_URL = https://<your-host>/ui/

FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend-requirements.txt
RUN pip install --no-cache-dir -r /app/backend-requirements.txt

COPY backend /app/backend
# Pre-built SPA (run: cd frontend && npm run build) — tracked in git for Cloud embeds
COPY frontend/dist /app/frontend/dist

WORKDIR /app/backend
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
