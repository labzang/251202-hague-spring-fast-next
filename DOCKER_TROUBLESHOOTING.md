# Docker Compose 에러 해결 가이드

## 🔧 해결된 문제

### 1. ✅ version 속성 경고 해결
- `docker-compose.yaml`에서 `version: '3.8'` 제거 완료
- 최신 Docker Compose는 version 속성이 필요 없습니다

### 2. ⚠️ Docker Desktop 연결 에러

**에러 메시지:**
```
unable to get image 'labzangcom-userservice': error during connect: 
Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/images/labzangcom-userservice/json": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**원인:** Docker Desktop이 실행되지 않았습니다.

## 🚀 해결 방법

### 방법 1: Docker Desktop 수동 실행
1. Windows 시작 메뉴에서 **Docker Desktop** 검색
2. **Docker Desktop** 실행
3. Docker Desktop이 완전히 시작될 때까지 대기 (시스템 트레이 아이콘 확인)
4. 다시 시도:
   ```bash
   docker compose up
   ```

### 방법 2: PowerShell에서 Docker Desktop 시작
```powershell
# Docker Desktop 실행
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# 또는
& "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### 방법 3: Docker Desktop 자동 시작 설정
1. Docker Desktop 실행
2. **Settings** → **General**
3. **Start Docker Desktop when you log in** 체크

## ✅ Docker Desktop 실행 확인

### 명령어로 확인
```powershell
# Docker 데몬 연결 확인
docker ps

# 정상적인 경우 컨테이너 목록이 표시됩니다
# 에러가 나면 Docker Desktop이 실행되지 않은 것입니다
```

### 시스템 트레이 확인
- Windows 시스템 트레이에서 Docker 아이콘 확인
- 아이콘이 보이면 Docker Desktop이 실행 중입니다

## 🔍 추가 문제 해결

### Docker Desktop이 시작되지 않을 때
1. **작업 관리자**에서 Docker 프로세스 확인
2. Docker Desktop 완전 종료 후 재시작
3. Windows 재부팅

### 포트 충돌
```powershell
# 사용 중인 포트 확인
netstat -ano | findstr :8080
netstat -ano | findstr :8081
netstat -ano | findstr :8082

# 프로세스 종료 (필요시)
taskkill /PID [PID번호] /F
```

### 권한 문제
- PowerShell을 **관리자 권한**으로 실행
- Docker Desktop이 관리자 권한으로 실행 중인지 확인

## 📝 정상 실행 확인

Docker Desktop이 실행되면 다음 명령어가 정상 작동합니다:

```powershell
# Docker 버전 확인
docker --version

# Docker Compose 버전 확인
docker compose version

# 실행 중인 컨테이너 확인
docker ps

# Docker Compose 실행
docker compose up
```

## 🎯 요약

1. ✅ **version 속성 제거 완료** - 경고 해결
2. ⚠️ **Docker Desktop 실행 필요** - 수동으로 실행하세요
3. ✅ **실행 확인** - `docker ps` 명령어로 확인

Docker Desktop을 실행한 후 다시 `docker compose up`을 시도하세요!
