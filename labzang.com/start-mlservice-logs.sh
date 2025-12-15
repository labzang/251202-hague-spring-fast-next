#!/bin/bash
# mlservice 로그를 실시간으로 보는 Bash 스크립트
# 사용법: ./start-mlservice-logs.sh

echo "다른 서비스들을 백그라운드로 시작합니다..."
docker compose --profile ai up -d --scale mlservice=0

echo "mlservice를 포그라운드로 시작합니다 (로그 실시간 출력)..."
docker compose --profile ai up mlservice

