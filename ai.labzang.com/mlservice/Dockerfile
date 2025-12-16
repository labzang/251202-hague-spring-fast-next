FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 시스템 패키지 업데이트 및 한글 폰트 설치
RUN apt-get update && apt-get install -y \
    fonts-nanum \
    fonts-nanum-coding \
    fonts-nanum-extra \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 폰트 캐시 업데이트
RUN fc-cache -fv

# 공통 모듈 복사 (빌드 컨텍스트가 ai.labzang.com인 경우)
COPY common ./common

# requirements.txt 복사 및 설치
COPY mlservice/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY mlservice/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9010"]

