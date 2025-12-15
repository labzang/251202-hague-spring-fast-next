# mlservice 재빌드 및 실행 가이드

## 빠른 해결 방법

```bash
# 1. 루트 디렉토리로 이동
cd C:\Users\hi\Documents\250930-hague-spring-fast-next\labzang.com

# 2. 기존 컨테이너 중지 및 제거
docker compose --profile ai stop mlservice
docker compose --profile ai rm -f mlservice

# 3. 이미지 재빌드 (캐시 없이)
docker compose --profile ai build --no-cache mlservice

# 4. 컨테이너 실행 (백그라운드)
docker compose --profile ai up -d mlservice

# 5. 로그 확인
docker logs -f mlservice
```

## 단계별 설명

### 1단계: 기존 컨테이너 정리

```bash
docker compose --profile ai stop mlservice
docker compose --profile ai rm -f mlservice
```

### 2단계: 이미지 재빌드

```bash
docker compose --profile ai build --no-cache mlservice
```

`--no-cache` 옵션으로 캐시 없이 완전히 새로 빌드합니다.

### 3단계: 컨테이너 실행

```bash
docker compose --profile ai up -d mlservice
```

`-d` 옵션으로 백그라운드에서 실행합니다.

### 4단계: 상태 확인

```bash
# 컨테이너 상태 확인
docker ps --filter "name=mlservice"

# 로그 확인
docker logs mlservice --tail 50
```

## 성공 확인

### 정상 실행 시

```bash
$ docker ps
CONTAINER ID   IMAGE                  STATUS         PORTS
xxxxx          labzangcom-mlservice  Up X minutes   0.0.0.0:9010->9010/tcp
```

### 브라우저에서 접속

- `http://localhost:9010` - 서비스 정보
- `http://localhost:9010/docs` - Swagger UI
- `http://localhost:9010/titanic/` - 타이타닉 서비스

## 문제가 계속되면

1. **이미지 완전 삭제 후 재빌드**
   ```bash
   docker rmi labzangcom-mlservice
   docker compose --profile ai build mlservice
   ```

2. **컨테이너 내부 확인**
   ```bash
   docker compose --profile ai run mlservice ls -la /app/app/
   ```

3. **로그 상세 확인**
   ```bash
   docker logs mlservice 2>&1 | more
   ```

