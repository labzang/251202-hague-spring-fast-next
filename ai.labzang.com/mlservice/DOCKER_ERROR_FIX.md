# Docker 컨테이너 에러 해결 가이드

## 에러 내용

```
ModuleNotFoundError: No module named 'app.config'
File "/app/app/main.py", line 14, in <module>
    from app.config import TitanicServiceConfig
```

## 에러 원인

1. **Docker 이미지가 오래되어 코드 변경사항이 반영되지 않음**
   - `main.py` 파일을 수정했지만, Docker 이미지가 재빌드되지 않아서 오래된 코드가 실행됨
   - 에러 로그의 라인 번호(14)가 현재 코드의 라인 번호(28)와 다름

2. **경로 설정 문제**
   - Docker 컨테이너 내부에서 Python 모듈 경로(`sys.path`)가 올바르게 설정되지 않음

3. **config.py 파일 복사 확인 필요**
   - Dockerfile에서 `config.py` 파일이 올바르게 복사되었는지 확인 필요

## 해결 방법

### 1단계: 실행 중인 컨테이너 중지 및 제거

```powershell
# 컨테이너 중지
docker compose --profile ai down mlservice

# 또는 강제로 중지
docker stop mlservice
docker rm mlservice
```

### 2단계: Docker 이미지 재빌드 (캐시 없이)

```powershell
# mlservice 이미지만 재빌드 (캐시 사용 안 함)
docker compose --profile ai build --no-cache mlservice

# 또는 전체 재빌드
docker compose --profile ai build --no-cache
```

### 3단계: 컨테이너 시작

```powershell
# 컨테이너 시작
docker compose --profile ai up mlservice

# 또는 백그라운드에서 실행
docker compose --profile ai up -d mlservice
```

### 4단계: 로그 확인

```powershell
# 실시간 로그 확인
docker compose --profile ai logs -f mlservice

# 또는 docker logs 사용
docker logs -f mlservice
```

### 5단계: 컨테이너 내부 확인 (선택사항)

```powershell
# 컨테이너 내부 접속
docker compose --profile ai exec mlservice bash

# 컨테이너 내부에서 파일 확인
docker compose --profile ai exec mlservice ls -la /app/app/

# config.py 파일 확인
docker compose --profile ai exec mlservice cat /app/app/config.py

# sys.path 확인
docker compose --profile ai exec mlservice python -c "import sys; print(sys.path)"
```

## 빠른 해결 (한 번에 실행)

```powershell
# 1. 컨테이너 중지 및 제거
docker compose --profile ai down mlservice

# 2. 이미지 재빌드
docker compose --profile ai build --no-cache mlservice

# 3. 컨테이너 시작 및 로그 확인
docker compose --profile ai up mlservice
```

## 변경사항 확인

현재 `main.py` 파일의 변경사항:

1. **경로 설정 개선** (라인 11-24)
   - Docker 환경과 로컬 환경 모두 지원
   - `/app` 경로를 명시적으로 추가

2. **에러 처리 개선** (라인 26-40)
   - `config.py`를 찾을 수 없어도 기본값으로 작동
   - `try-except` 블록으로 안전하게 처리

3. **모듈 import 안전장치** (라인 42-55)
   - 공통 모듈을 찾을 수 없어도 기본 동작 제공

## 예상 결과

성공적으로 실행되면 다음과 같은 로그가 출력됩니다:

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9010 (Press CTRL+C to quit)
```

## 추가 문제 해결

### 문제 1: 여전히 같은 에러가 발생하는 경우

```powershell
# 모든 mlservice 관련 이미지 및 컨테이너 제거
docker stop mlservice 2>$null
docker rm mlservice 2>$null
docker rmi labzang-com-mlservice 2>$null

# 완전히 새로 빌드
docker compose --profile ai build --no-cache --pull mlservice
docker compose --profile ai up mlservice
```

### 문제 2: config.py 파일이 없다는 에러

```powershell
# config.py 파일이 존재하는지 확인
Test-Path ai.labzang.com\mlservice\app\config.py

# 파일 내용 확인
Get-Content ai.labzang.com\mlservice\app\config.py
```

### 문제 3: 포트가 이미 사용 중인 경우

```powershell
# 포트 9010을 사용하는 프로세스 확인
netstat -ano | findstr :9010

# 프로세스 종료 (PID 확인 후)
taskkill /PID <PID> /F
```

## 참고 사항

- **Docker 이미지는 코드 변경 후 반드시 재빌드해야 합니다**
- `--no-cache` 옵션을 사용하면 완전히 새로 빌드됩니다 (시간이 더 걸림)
- 개발 중에는 `docker compose up --build` 옵션으로 자동 빌드할 수 있습니다
- 프로덕션 환경에서는 변경사항을 적용하기 전에 테스트를 수행하세요

## 성공 확인

브라우저 또는 curl로 확인:

```powershell
# 루트 엔드포인트 확인
curl http://localhost:9010/

# Swagger UI 접속
Start-Process "http://localhost:9010/docs"
```


