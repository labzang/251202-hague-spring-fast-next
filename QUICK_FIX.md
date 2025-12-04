# Docker Compose 에러 빠른 해결

## ✅ 해결 완료

### 1. version 속성 경고
- `docker-compose.yaml`에서 `version: '3.8'` 제거 완료
- 이제 경고가 나타나지 않습니다

## ⚠️ 해결 필요: Docker Desktop 실행

### 에러 원인
```
unable to get image 'labzangcom-userservice': error during connect: 
Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/images/labzangcom-userservice/json": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**원인**: Docker Desktop이 실행되지 않았습니다.

### 해결 방법

#### 방법 1: 수동 실행 (가장 간단)
1. Windows 시작 메뉴 열기
2. "Docker Desktop" 검색
3. Docker Desktop 실행
4. 시스템 트레이에서 Docker 아이콘이 나타날 때까지 대기 (약 30초~1분)
5. 다시 시도:
   ```powershell
   docker compose up
   ```

#### 방법 2: PowerShell에서 실행
```powershell
# Docker Desktop 실행
& "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

#### 방법 3: 시작 메뉴에서 실행
- Windows 키 누르기
- "Docker Desktop" 입력
- Enter 키

### 실행 확인

Docker Desktop이 실행되면 다음 명령어로 확인:

```powershell
# Docker 연결 확인
docker ps

# 정상이면 빈 목록이 표시됩니다 (에러 없이)
# 에러가 나면 아직 Docker Desktop이 완전히 시작되지 않은 것입니다
```

### Docker Desktop 시작 확인

시스템 트레이(작업 표시줄 오른쪽)에서:
- 🐳 Docker 아이콘이 보이면 실행 중
- 아이콘이 없으면 실행되지 않음

## 🎯 다음 단계

1. ✅ `version` 속성 제거 완료
2. ⚠️ **Docker Desktop 실행 필요** ← 지금 해야 할 일
3. Docker Desktop 실행 후 `docker compose up` 다시 시도

## 💡 팁

Docker Desktop이 시작되는 데 시간이 걸릴 수 있습니다. 시스템 트레이의 Docker 아이콘이 안정화될 때까지 기다리세요.
