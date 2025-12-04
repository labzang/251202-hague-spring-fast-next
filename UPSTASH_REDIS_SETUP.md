# Upstash Redis 연동 가이드

## 📋 개요

이 가이드는 Upstash Redis를 모든 서비스에 연동하는 방법을 설명합니다.

## 🚀 Upstash Redis 설정

### 1. Upstash Redis 인스턴스 정보

이미지에서 확인된 정보:
- **Endpoint**: `summary-polliwog-43960.upstash.io`
- **Port**: `6379`
- **TLS/SSL**: Enabled (필수)
- **Token**: Upstash 대시보드에서 확인

### 2. 연결 URL 형식

Upstash Redis는 TLS가 필수이므로 다음 형식을 사용합니다:

```
redis://default:YOUR_TOKEN@summary-polliwog-43960.upstash.io:6379
```

## 🔧 환경 변수 설정

### .env 파일 설정

```env
# Upstash Redis TCP 연결 (TLS 필수)
REDIS_URL=redis://default:your_upstash_token@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your_upstash_token
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required

# Upstash Redis REST API (선택사항)
UPSTASH_REDIS_REST_URL=https://summary-polliwog-43960.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_upstash_rest_token
```

### Upstash 대시보드에서 Token 확인

1. Upstash 대시보드 로그인
2. `/labzangdb` Redis 인스턴스 선택
3. **Details** 탭에서:
   - **Token** 또는 **Readonly Token** 복사
   - **Endpoint** 확인 (이미 설정됨: `summary-polliwog-43960.upstash.io`)

## 🐳 Docker Compose 설정

### docker-compose.db.yaml

모든 서비스에 Upstash Redis 환경 변수가 자동으로 주입됩니다:

```yaml
environment:
  - REDIS_URL=${REDIS_URL}
  - REDIS_HOST=${REDIS_HOST}
  - REDIS_PORT=${REDIS_PORT}
  - REDIS_PASSWORD=${REDIS_PASSWORD}
  - REDIS_SSL_ENABLED=${REDIS_SSL_ENABLED}
```

### docker-compose.yaml

로컬 개발 시에도 Upstash Redis를 사용할 수 있습니다:

```yaml
environment:
  - REDIS_HOST=${REDIS_HOST:-summary-polliwog-43960.upstash.io}
  - REDIS_PORT=${REDIS_PORT:-6379}
  - REDIS_PASSWORD=${REDIS_PASSWORD:-}
  - REDIS_SSL_ENABLED=${REDIS_SSL_ENABLED:-true}
  - REDIS_URL=${REDIS_URL}
```

## 🔌 서비스별 연결 설정

### Spring Boot 서비스 (Java)

**application-railway.yaml** 파일에서 Upstash Redis 설정:

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST}
      port: ${REDIS_PORT}
      password: ${REDIS_PASSWORD}
      ssl:
        enabled: true
      lettuce:
        ssl:
          enabled: true
          verify-peer: true
```

### FastAPI 서비스 (Python)

**database.py** 파일에서 Upstash Redis 연결:

```python
import ssl
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    ssl=True
)
```

## 🧪 연결 테스트

### Python 서비스 테스트

```bash
# ERP 서비스
cd erp.labzang.com
python common/database.py

# AI 서비스
cd ai.labzang.com
python common/database.py
```

### Spring Boot 서비스 테스트

```bash
# 서비스 실행 후 헬스 체크
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
```

### Redis CLI 테스트

Upstash 대시보드에서 제공하는 명령어:

```bash
redis-cli --tls -u redis://default:YOUR_TOKEN@summary-polliwog-43960.upstash.io:6379
```

## 📊 Upstash 사용량 모니터링

### 무료 티어 제한

- **Commands**: 500k per month
- **Bandwidth**: 50 GB
- **Storage**: 256 MB

### 사용량 확인

1. Upstash 대시보드에서 **Usage** 탭 확인
2. 실시간 메트릭 모니터링
3. 알림 설정 (사용량 임계값 초과 시)

## 🔍 트러블슈팅

### 1. TLS 연결 실패

**문제**: `SSL: CERTIFICATE_VERIFY_FAILED`

**해결**:
- `REDIS_SSL_ENABLED=true` 확인
- `ssl_cert_reqs=ssl.CERT_REQUIRED` 설정 확인
- Python의 경우 `certifi` 패키지 설치 확인

### 2. 인증 실패

**문제**: `NOAUTH Authentication required`

**해결**:
- `REDIS_PASSWORD`에 올바른 Token 입력
- Token이 만료되지 않았는지 확인
- Readonly Token이 아닌 일반 Token 사용 확인

### 3. 연결 타임아웃

**문제**: `Connection timeout`

**해결**:
- 네트워크 연결 확인
- 방화벽 설정 확인
- Upstash 서비스 상태 확인

### 4. Python redis 패키지 버전

**필요한 패키지**:
```bash
pip install redis[hiredis]>=5.0.0
```

## 🔐 보안 주의사항

1. **Token 보안**: `.env` 파일을 Git에 커밋하지 마세요
2. **Readonly Token**: 읽기 전용 작업에는 Readonly Token 사용
3. **환경 변수**: 프로덕션에서는 환경 변수로 관리
4. **SSL/TLS**: 항상 TLS 연결 사용 (Upstash 필수)

## 📝 주요 변경사항

### docker-compose.yaml
- 로컬 Redis 컨테이너 제거
- Upstash Redis 환경 변수 추가
- 모든 서비스에 Redis 설정 주입

### docker-compose.db.yaml
- 모든 서비스에 Upstash Redis 설정 추가
- SSL/TLS 설정 포함

### database.py (Python)
- Upstash Redis TLS 연결 지원
- SSL 인증서 검증 설정

### application-railway.yaml (Spring Boot)
- Upstash Redis SSL 설정
- Lettuce SSL 설정 추가

## 🔗 관련 파일

- `.env.example` - 환경 변수 템플릿
- `database-config.yaml` - 데이터베이스 설정 파일
- `docker-compose.db.yaml` - Railway + Upstash 연동 Docker Compose
- `docker-compose.yaml` - 로컬 개발용 Docker Compose
- `UPSTASH_REDIS_SETUP.md` - 이 가이드 파일

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. Upstash 대시보드에서 서비스 상태
2. 환경 변수 설정 (특히 Token)
3. 네트워크 연결
4. SSL/TLS 설정
5. 애플리케이션 로그
