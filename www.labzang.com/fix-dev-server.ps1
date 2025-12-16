# Next.js 개발 서버 Lock 문제 해결 스크립트
# 전략: lock 파일만 삭제 (일반적인 경우)
# 문제가 지속될 때만 .next 폴더 전체 삭제
# 사용법: .\fix-dev-server.ps1 [--full]

param(
    [switch]$Full = $false  # --full 플래그로 .next 폴더 전체 삭제
)

Write-Host "`n🔧 Next.js 개발 서버 문제 해결 중...`n" -ForegroundColor Cyan

# 1. 포트 3000 확인 및 종료
$port = 3000
Write-Host "📡 포트 $port 확인 중..." -ForegroundColor Yellow
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($connections) {
    $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $pids) {
        try {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Stop-Process -Id $pid -Force
                Write-Host "  ✅ 포트 $port 의 프로세스(PID: $pid, 이름: $($process.ProcessName)) 종료 완료" -ForegroundColor Green
            }
        } catch {
            Write-Host "  ⚠️ 프로세스 $pid 종료 실패: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  ℹ️ 포트 $port 는 사용 중이 아닙니다" -ForegroundColor Gray
}

# 2. 전략 1: Lock 파일만 삭제 (일반적인 경우)
if (-not $Full) {
    Write-Host "`n🗑️ Lock 파일만 삭제 중 (일반 방법)..." -ForegroundColor Yellow
    $lockFile = ".next\dev\lock"
    if (Test-Path $lockFile) {
        Remove-Item $lockFile -Force
        Write-Host "  ✅ Lock 파일 삭제 완료: $lockFile" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️ Lock 파일이 없습니다" -ForegroundColor Gray
    }
}
# 3. 전략 2: .next 폴더 전체 삭제 (문제가 지속될 때만)
else {
    Write-Host "`n🗑️ .next 폴더 전체 삭제 중 (완전 초기화)..." -ForegroundColor Yellow
    if (Test-Path ".next") {
        Remove-Item ".next" -Recurse -Force
        Write-Host "  ✅ .next 폴더 삭제 완료" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️ .next 폴더가 없습니다" -ForegroundColor Gray
    }
}

Write-Host "`n✅ 정리 완료!`n" -ForegroundColor Green

# 4. 개발 서버 자동 시작
Write-Host "🚀 개발 서버 시작 중...`n" -ForegroundColor Cyan
pnpm dev

