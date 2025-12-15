#!/bin/bash
# mlservice 컨테이너 로그 실시간 보기 Bash 스크립트
# 사용법: ./view-mlservice-logs.sh [lines] [follow]

# 기본값 설정
LINES=${1:-50}  # 기본적으로 최근 50줄 표시
FOLLOW=${2:-true}  # 기본적으로 실시간 팔로우

echo "=== MLService 컨테이너 로그 뷰어 ==="
echo "최근 $LINES 줄부터 실시간 로그를 표시합니다."
echo "종료하려면 Ctrl+C를 누르세요."
echo "=================================================="

# 컨테이너 상태 확인
CONTAINER_STATUS=$(docker ps --filter "name=mlservice" --format "{{.Status}}")

if [ -z "$CONTAINER_STATUS" ]; then
    echo "❌ mlservice 컨테이너가 실행 중이지 않습니다."
    echo "컨테이너를 시작하려면 다음 명령을 실행하세요:"
    echo "docker compose up mlservice -d"
    exit 1
else
    echo "✅ mlservice 컨테이너 상태: $CONTAINER_STATUS"
fi

echo ""

# 실시간 로그 출력
if [ "$FOLLOW" = "true" ]; then
    docker logs mlservice --tail "$LINES" --follow --timestamps
else
    docker logs mlservice --tail "$LINES" --timestamps
fi
