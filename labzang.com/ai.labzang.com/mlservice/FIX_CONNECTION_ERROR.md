# 연결 에러 해결 가이드

## 에러 원인

**ERR_CONNECTION_REFUSED** 에러가 발생하는 이유:

1. **컨테이너가 정상 시작되지 않음**
   - Docker 컨테이너가 계속 재시작 중 (Restarting 상태)
   - 포트 9010이 리스닝되지 않음

2. **애플리케이션 시작 실패**
   - `ModuleNotFoundError: No module named 'app.config'` 에러 발생
   - 코드 변경사항이 Docker 이미지에 반영되지 않음

## 해결 방법

### 1. 컨테이너 중지 및 이미지 재빌드

```bash
# 루트 디렉토리에서
cd C:\Users\hi\Documents\250930-hague-spring-fast-next\labzang.com

# 컨테이너 중지 및 제거
docker compose --profile ai stop mlservice
docker compose --profile ai rm -f mlservice

# 이미지 재빌드 (캐시 없이)
docker compose --profile ai build --no-cache mlservice

# 컨테이너 다시 시작
docker compose --profile ai up -d mlservice
```

### 2. 로그 확인

```bash
# 실시간 로그 확인
docker logs -f mlservice

# 또는 최근 50줄
docker logs mlservice --tail 50
```

### 3. 포트 확인

정상 실행되면:
- **포트**: `9010`
- **URL**: `http://localhost:9010`
- **Swagger UI**: `http://localhost:9010/docs`

### 4. 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker ps

# 모든 컨테이너 확인 (중지된 것 포함)
docker ps -a
```

정상 상태라면:
```
STATUS: Up X minutes
PORTS: 0.0.0.0:9010->9010/tcp
```

## 현재 상태 확인

```bash
# 컨테이너 상태
docker ps -a --filter "name=mlservice"

# 포트 매핑 확인
docker port mlservice

# 로그 확인
docker logs mlservice --tail 20
```

## 예상 결과

성공 시:
- 컨테이너 상태: `Up X minutes` (재시작 없음)
- 포트: `0.0.0.0:9010->9010/tcp`
- 브라우저: `http://localhost:9010/docs` 접속 가능

