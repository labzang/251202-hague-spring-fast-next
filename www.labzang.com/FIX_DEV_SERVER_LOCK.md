# Next.js 개발 서버 Lock 파일 문제 해결 가이드

## 🔍 문제 원인

Next.js 개발 서버가 비정상 종료되거나 여러 인스턴스가 실행될 때:
- `.next/dev/lock` 파일이 남아있어 새 서버 실행 차단
- 포트 3000이 이미 사용 중이어서 충돌 발생
- 프로세스가 백그라운드에서 계속 실행 중

## ✅ 해결 방법 (권장 순서)

### 방법 1: 빠른 해결 (권장)

```powershell
# 1. 포트 3000 사용 중인 프로세스 확인 및 종료
$port = 3000
$process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($process) {
    $pid = $process.OwningProcess
    Stop-Process -Id $pid -Force
    Write-Host "포트 $port 의 프로세스(PID: $pid) 종료 완료"
}

# 2. 모든 Node.js 프로세스 확인 (선택사항 - 필요한 경우만)
# Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. .next/dev/lock 파일만 삭제 (빌드 결과물은 유지)
if (Test-Path "www.labzang.com\.next\dev\lock") {
    Remove-Item "www.labzang.com\.next\dev\lock" -Force
    Write-Host ".next/dev/lock 파일 삭제 완료"
}

# 4. 개발 서버 실행
cd www.labzang.com
pnpm dev
```

### 방법 2: 완전 초기화 (문제가 지속될 때)

```powershell
# 1. 포트 3000 프로세스 종료
$port = 3000
$process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
}

# 2. 모든 Node.js 프로세스 종료 (주의: 다른 Node 프로젝트도 종료됨)
Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. .next 폴더 전체 삭제 (빌드 캐시 초기화)
if (Test-Path "www.labzang.com\.next") {
    Remove-Item "www.labzang.com\.next" -Recurse -Force
    Write-Host ".next 폴더 삭제 완료"
}

# 4. 개발 서버 실행
cd www.labzang.com
pnpm dev
```

### 방법 3: 원클릭 스크립트

`fix-dev-server.ps1` 파일 생성:

```powershell
# fix-dev-server.ps1
Write-Host "🔧 Next.js 개발 서버 문제 해결 중..." -ForegroundColor Cyan

# 포트 3000 확인 및 종료
$port = 3000
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connections) {
    $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $pids) {
        Stop-Process -Id $pid -Force
        Write-Host "✅ 포트 $port 의 프로세스(PID: $pid) 종료" -ForegroundColor Green
    }
} else {
    Write-Host "ℹ️ 포트 $port 는 사용 중이 아닙니다" -ForegroundColor Yellow
}

# .next/dev/lock 파일 삭제
$lockFile = ".next\dev\lock"
if (Test-Path $lockFile) {
    Remove-Item $lockFile -Force
    Write-Host "✅ Lock 파일 삭제 완료" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Lock 파일이 없습니다" -ForegroundColor Yellow
}

Write-Host "`n🚀 개발 서버를 시작합니다..." -ForegroundColor Cyan
pnpm dev
```

사용법:
```powershell
cd www.labzang.com
.\fix-dev-server.ps1
```

## 📋 체크리스트

해결 전 확인사항:
- [ ] 포트 3000이 사용 중인가? (`netstat -ano | findstr :3000`)
- [ ] Node.js 프로세스가 실행 중인가? (`Get-Process -Name node`)
- [ ] `.next/dev/lock` 파일이 존재하는가?
- [ ] 올바른 디렉토리(`www.labzang.com`)에서 실행하는가?

## ⚠️ 주의사항

1. **.next 폴더 삭제 시**: 
   - 빌드 캐시가 삭제되어 첫 실행 시 시간이 걸릴 수 있음
   - 개발 환경에서는 문제 없음 (프로덕션 빌드는 영향 없음)

2. **모든 Node 프로세스 종료 시**:
   - 다른 프로젝트의 Node 서버도 종료될 수 있음
   - 필요한 경우 특정 PID만 종료하는 것이 안전함

3. **포트 확인**:
   - 포트가 실제로 사용 중인지 먼저 확인
   - 필요없는 프로세스 종료 방지

## 💡 예방 방법

1. **정상 종료**: 개발 서버를 중지할 때 `Ctrl+C` 사용
2. **단일 인스턴스**: 동시에 여러 `pnpm dev` 실행 금지
3. **자동 정리 스크립트**: IDE 종료 시 자동 실행 설정 (선택사항)

## 🎯 권장 순서 (요약)

**일반적인 경우:**
```powershell
# 1단계: 포트 확인 및 프로세스 종료
netstat -ano | findstr :3000
# PID 확인 후
taskkill /PID [PID번호] /F

# 2단계: Lock 파일 삭제만
Remove-Item www.labzang.com\.next\dev\lock -Force -ErrorAction SilentlyContinue

# 3단계: 개발 서버 실행
cd www.labzang.com
pnpm dev
```

**문제가 지속될 때만 전체 초기화:**
```powershell
# .next 폴더 전체 삭제
Remove-Item www.labzang.com\.next -Recurse -Force -ErrorAction SilentlyContinue
```

