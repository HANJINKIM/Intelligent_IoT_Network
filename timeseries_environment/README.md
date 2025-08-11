# timeseries environment configuration

Kafka → InfluxDB → Grafana 파이프라인과 PyTorch 기반의 시계열 데이터 예측 및 분석을 위한 환경 구축
간략한 실습 내용 포함

## 데이터 흐름
Producer → Kafka → Consumer → InfluxDB → Grafana

## 요구사항
- Windows 11, WSL2 권장
- Docker Desktop
- Python 3.10+

## 빠른 시작
```bash
git clone <REPO_URL>
cd timeseries_environment
copy .env.example .env   # (본 레포는 .env가 이미 있음)
docker compose up -d

## 접속
InfluxDB: http://localhost:8086 (초기계정 : admin, 비밀번호: admin123, 토큰 : admintoken )
Grafana:  http://localhost:3000 (초기계정 : admin, 비밀번호: admin)