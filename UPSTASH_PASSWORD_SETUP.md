# Upstash Redis Password (Token) 설정 가이드

## 🔑 Password = Token

Upstash Redis에서 **password는 Token**입니다. TCP 연결을 위해서는 **TCP Token**이 필요합니다.

## 📍 TCP Token 찾기 (REDIS_PASSWORD 설정용)

### Step 1: TCP 탭으로 이동
1. Upstash 대시보드 → `/labzangdb` 선택
2. **Connect** 섹션으로 스크롤
3. **TCP** 탭 클릭 (현재 REST 탭이 선택되어 있음)

### Step 2: TCP Token 확인
TCP 탭에서 다음 정보를 확인할 수 있습니다:

```
redis-cli --tls -u redis://default:TOKEN@summary-polliwog-43960.upstash.io:6379
```

여기서 `TOKEN` 부분이 바로 **REDIS_PASSWORD**에 입력할 값입니다.

### Step 3: Token 복사
1. TCP 탭에서 **Token** 옆 **눈 아이콘** 클릭 → Token 표시
2. **복사 아이콘** 클릭 → Token 복사
3. 또는 `redis-cli` 명령어에서 Token 부분만 추출

## 🔧 .env 파일 설정

### 현재 상태 확인
현재 `.env` 파일에는 REST Token만 설정되어 있습니다:
```env
UPSTASH_REDIS_REST_TOKEN="Aau4AAIncDJlYTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA"
```

### TCP Token 추가 필요
TCP 연결을 위해서는 다음을 추가해야 합니다:

```env
# ========================================================================
# Upstash Redis TCP 연결 (TLS 필수) - REDIS_PASSWORD 설정
# ========================================================================
# TCP 탭에서 Token 복사 후 아래에 붙여넣기
REDIS_URL=redis://default:YOUR_TCP_TOKEN@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=YOUR_TCP_TOKEN  # ← TCP 탭에서 복사한 Token
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required

# ========================================================================
# Upstash Redis REST API (선택사항) - 이미 설정됨
# ========================================================================
UPSTASH_REDIS_REST_URL="https://summary-polliwog-43960.upstash.io"
UPSTASH_REDIS_REST_TOKEN="Aau4AAIncDJlYTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA"
```

## 🔍 REST Token vs TCP Token 차이

| 구분 | REST Token | TCP Token |
|------|-----------|-----------|
| **용도** | REST API 호출 | TCP/TLS 직접 연결 |
| **위치** | REST 탭 | TCP 탭 |
| **환경 변수** | `UPSTASH_REDIS_REST_TOKEN` | `REDIS_PASSWORD` |
| **사용 서비스** | HTTP 기반 클라이언트 | Redis 클라이언트 (redis-py, ioredis 등) |

## 📝 완전한 .env 설정 예시

```env
# ========================================================================
# Upstash Redis TCP 연결 (모든 컨테이너에서 사용)
# ========================================================================
# TCP 탭 → Token 복사 → 아래에 붙여넣기
REDIS_URL=redis://default:YOUR_TCP_TOKEN_HERE@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=YOUR_TCP_TOKEN_HERE  # TCP 탭의 Token
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required

# ========================================================================
# Upstash Redis REST API (선택사항)
# ========================================================================
UPSTASH_REDIS_REST_URL="https://summary-polliwog-43960.upstash.io"
UPSTASH_REDIS_REST_TOKEN="Aau4AAIncDJlYTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA"
```

## ✅ 설정 확인 방법

### 1. TCP Token이 올바른지 확인
```bash
# .env 파일에서 확인
grep REDIS_PASSWORD .env

# 출력 예시:
# REDIS_PASSWORD=your_tcp_token_here
```

### 2. 연결 테스트 (Python)
```python
import redis
import ssl
import os

# .env에서 로드
REDIS_URL = os.getenv("REDIS_URL")

client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    ssl=True
)

try:
    client.ping()
    print("✅ TCP 연결 성공!")
except Exception as e:
    print(f"❌ TCP 연결 실패: {e}")
```

### 3. Docker Compose로 테스트
```bash
# .env 파일 설정 후
docker-compose -f docker-compose.db.yaml up -d customerservice

# 로그에서 Redis 연결 확인
docker-compose -f docker-compose.db.yaml logs customerservice | grep -i redis
```

## 🎯 요약

1. **TCP 탭으로 이동**: Connect 섹션 → TCP 탭 클릭
2. **Token 복사**: 눈 아이콘 클릭 → Token 표시 → 복사
3. **.env 파일 설정**: 
   - `REDIS_PASSWORD=복사한_TCP_Token`
   - `REDIS_URL=redis://default:복사한_TCP_Token@summary-polliwog-43960.upstash.io:6379`
4. **REST Token은 이미 설정됨**: `UPSTASH_REDIS_REST_TOKEN`은 이미 있음

## ⚠️ 주의사항

- **REST Token ≠ TCP Token**: 서로 다른 Token입니다
- **TCP Token 필수**: Spring Boot와 FastAPI 서비스는 TCP Token 필요
- **REST Token 선택사항**: HTTP 기반 클라이언트만 필요
- **보안**: Token을 Git에 커밋하지 마세요
