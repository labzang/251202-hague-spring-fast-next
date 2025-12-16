# mlservice 컨테이너 로그 실시간 보기 PowerShell 스크립트
# 사용법: .\view-mlservice-logs.ps1

param(
    [string]$Lines = "50",  # 기본적으로 최근 50줄 표시
    [switch]$Follow = $true  # 기본적으로 실시간 팔로우
)

Write-Host "=== MLService 컨테이너 로그 뷰어 ===" -ForegroundColor Cyan
Write-Host "최근 $Lines 줄부터 실시간 로그를 표시합니다." -ForegroundColor Yellow
Write-Host "종료하려면 Ctrl+C를 누르세요." -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Gray

# 컨테이너 상태 확인
$containerStatus = docker ps --filter "name=mlservice" --format "{{.Status}}"

if ([string]::IsNullOrEmpty($containerStatus)) {
    Write-Host "❌ mlservice 컨테이너가 실행 중이지 않습니다." -ForegroundColor Red
    Write-Host "컨테이너를 시작하려면 다음 명령을 실행하세요:" -ForegroundColor Yellow
    Write-Host "docker compose up mlservice -d" -ForegroundColor Green
    exit 1
} else {
    Write-Host "✅ mlservice 컨테이너 상태: $containerStatus" -ForegroundColor Green
}

Write-Host ""

# 실시간 로그 출력
if ($Follow) {
    docker logs mlservice --tail $Lines --follow --timestamps
} else {
    docker logs mlservice --tail $Lines --timestamps
}
