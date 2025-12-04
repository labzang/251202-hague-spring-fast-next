# Docker Compose 에러 원인 분석

## 🔍 에러 메시지 분석

```
unable to get image 'labzangcom-gateway': error during connect: 
Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/images/labzangcom-gateway/json": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

## 📋 에러 원인

### 1. **주요 원인: Docker Desktop이 실행되지 않음**

**증거:**
- `docker info` 명령어도 같은 에러 발생
- `dockerDesktopLinuxEngine` 파이프를 찾을 수 없음
- 이 파이프는 Docker Desktop이 실행될 때만 생성됩니다

**파이프 경로:**
```
//./pipe/dockerDesktopLinuxEngine
```
이것은 Windows Named Pipe로, Docker Desktop의 Linux 엔진과 통신하는 데 사용됩니다.

### 2. **이미지 이름 생성 방식**

`labzangcom-gateway` 이미지 이름은 Docker Compose가 자동으로 생성합니다:
- 디렉토리 이름: `labzang.com`
- 점(.) 제거: `labzangcom`
- 서비스 이름 추가: `labzangcom-gateway`

**형식:** `[디렉토리명]_[서비스명]` 또는 `[디렉토리명][서비스명]`

## 🔧 에러 발생 과정

1. `docker compose up` 실행
2. Docker Compose가 기존 이미지 확인 시도
3. Docker 데몬에 연결 시도
4. **Docker Desktop이 실행되지 않아 파이프를 찾을 수 없음**
5. 연결 실패 → 에러 발생

## ✅ 해결 방법

### 즉시 해결
1. **Docker Desktop 실행**
   - Windows 시작 메뉴 → "Docker Desktop" 검색 → 실행
   - 시스템 트레이에 Docker 아이콘이 나타날 때까지 대기

2. **실행 확인**
   ```powershell
   docker ps
   ```
   - 에러 없이 실행되면 정상

3. **다시 시도**
   ```powershell
   docker compose up
   ```

## 🔍 추가 확인 사항

### Docker Desktop 실행 상태 확인
```powershell
# 방법 1: 프로세스 확인
Get-Process -Name "*Docker*" -ErrorAction SilentlyContinue

# 방법 2: Docker 연결 테스트
docker version

# 방법 3: Docker 정보 확인
docker info
```

### 정상적인 경우
```powershell
PS> docker info
Client:
  Version:    28.5.1
  ...
Server:
  Containers: 0
  Running: 0
  ...
  # Server 정보가 정상적으로 표시됨
```

### 비정상적인 경우 (현재 상태)
```powershell
PS> docker info
Client:
  ...
Server:
error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.51/info": 
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

## 📊 에러 원인 요약

| 항목 | 상태 | 설명 |
|------|------|------|
| Docker 설치 | ✅ 정상 | Docker 28.5.1 설치됨 |
| Docker Compose | ✅ 정상 | Docker Compose v2.40.0 설치됨 |
| Docker Desktop 실행 | ❌ **실행 안 됨** | **이것이 문제의 원인** |
| docker-compose.yaml | ✅ 정상 | 파일 구조 정상 |

## 🎯 결론

**에러의 근본 원인:**
- Docker Desktop이 실행되지 않아서 Docker 데몬에 연결할 수 없음
- `dockerDesktopLinuxEngine` 파이프가 생성되지 않음

**해결:**
- Docker Desktop을 실행하면 모든 문제가 해결됩니다
- Docker Desktop 실행 후 `docker compose up`을 다시 시도하세요

## 💡 참고

- Docker Desktop은 Windows에서 Docker를 실행하기 위한 필수 프로그램입니다
- Docker CLI는 설치되어 있지만, 실제 컨테이너를 실행하려면 Docker Desktop이 필요합니다
- Docker Desktop이 실행되면 Linux 가상 머신이 시작되고, 그 안에서 컨테이너가 실행됩니다

