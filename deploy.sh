#!/bin/bash

# Labzang API EC2 배포 스크립트

set -e

echo "🚀 Labzang API 배포 시작..."

# 1. 최신 코드 가져오기 (서브모듈 포함)
echo "📥 최신 코드 가져오기..."
git pull origin master
echo "📥 서브모듈 업데이트..."
git submodule update --remote --recursive

# 2. 환경 변수 파일 확인
if [ ! -f ".env" ]; then
    echo "❌ .env 파일이 없습니다. 환경 변수를 설정해주세요."
    exit 1
fi

# 3. Docker 이미지 최신 버전 가져오기
echo "🐳 Docker 이미지 업데이트..."
docker-compose -f api.labzang.com/docker-compose.prod.yml pull

# 4. 기존 컨테이너 중지 및 제거
echo "🛑 기존 서비스 중지..."
docker-compose -f api.labzang.com/docker-compose.prod.yml down

# 5. 새 컨테이너 시작
echo "▶️ 새 서비스 시작..."
docker-compose -f api.labzang.com/docker-compose.prod.yml up -d

# 6. 헬스 체크
echo "🔍 서비스 상태 확인..."
sleep 30

if curl -f http://localhost:8080/docs > /dev/null 2>&1; then
    echo "✅ 배포 성공! API가 정상 동작 중입니다."
    echo "🌐 API 문서: http://your-ec2-ip:8080/docs"
else
    echo "❌ 배포 실패! 로그를 확인해주세요."
    docker-compose -f api.labzang.com/docker-compose.prod.yml logs --tail 50
    exit 1
fi

echo "🎉 배포 완료!"
