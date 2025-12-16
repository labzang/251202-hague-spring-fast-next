# mlservice 로그를 실시간으로 보는 PowerShell 스크립트
# 사용법: .\start-mlservice-logs.ps1

Write-Host "다른 서비스들을 백그라운드로 시작합니다..." -ForegroundColor Yellow
docker compose --profile ai up -d --scale mlservice=0

Write-Host "mlservice를 포그라운드로 시작합니다 (로그 실시간 출력)..." -ForegroundColor Green
docker compose --profile ai up mlservice



docker compose down
docker compose up gateway mlservice -d
