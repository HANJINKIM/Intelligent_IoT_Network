FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 런타임 최소 의존성만 설치 (torch 제외)
COPY consumer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY consumer/ /app/
CMD ["python", "consumer.py"]