# Upstash Redis Token 찾기 및 설정 가이드

## 🔑 Redis Password = Token

Upstash Redis에서는 **전통적인 password 대신 Token을 사용**합니다. 
`REDIS_PASSWORD` 환경 변수에는 **Upstash Token**을 입력하면 됩니다.

## 📍 Token 위치 찾기

### 1. Upstash 대시보드 접속
1. [Upstash Console](https://console.upstash.com)에 로그인
2. `/labzangdb` Redis 인스턴스 선택

### 2. Details 탭에서 Token 확인
1. **Details** 탭 클릭 (기본적으로 선택되어 있음)
2. **"Token / Readonly Token"** 섹션 확인
3. 두 가지 Token이 있습니다:
   - **Token**: 읽기/쓰기 권한 (일반적으로 이것 사용)
   - **Readonly Token**: 읽기 전용 권한

### 3. Token 복사 방법
- **눈 아이콘** 클릭 → Token 표시
- **복사 아이콘** 클릭 → Token 복사
- 또는 직접 입력

## 🔧 .env 파일 설정

### 올바른 설정 예시

```env
# Upstash Redis TCP 연결 (TLS 필수)
# REDIS_URL 형식: redis://default:TOKEN@host:port
REDIS_URL=redis://default:YOUR_UPSTASH_TOKEN@summary-polliwog-43960.upstash.io:6379

# 개별 설정
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=YOUR_UPSTASH_TOKEN  # ← 여기에 Token 입력!
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required

# REST API (선택사항)
UPSTASH_REDIS_REST_URL=https://summary-polliwog-43960.upstash.io
UPSTASH_REDIS_REST_TOKEN=YOUR_REST_TOKEN
```

### ❌ 잘못된 설정 예시

```env
# 잘못됨: redis-cli 명령어가 포함되어 있음
REDIS_URL=redis://redis-cli --tls -u redis://default

# 올바름: 순수한 Redis URL만 사용
REDIS_URL=redis://default:YOUR_TOKEN@summary-polliwog-43960.upstash.io:6379
```

## 📝 실제 설정 단계

### Step 1: Token 복사
1. Upstash 대시보드 → `/labzangdb` 선택
2. **Details** 탭에서 **Token** 옆 **눈 아이콘** 클릭
3. Token 표시되면 **복사 아이콘** 클릭

### Step 2: .env 파일 수정
```env
# 예시 (실제 Token으로 교체하세요)
REDIS_PASSWORD=Aau4AAIncDJlYTkwN2M5ZjNkZj...  # 복사한 Token 붙여넣기
REDIS_URL=redis://default:Aau4AAIncDJlYTkwN2M5ZjNkZj...@summary-polliwog-43960.upstash.io:6379
```

### Step 3: REST Token (선택사항)
REST API를 사용하는 경우:
1. **Connect** 섹션 → **REST** 탭
2. `UPSTASH_REDIS_REST_TOKEN` 복사
3. `.env` 파일에 추가

## 🔍 Token 확인 방법

### 방법 1: redis-cli로 테스트
Upstash 대시보드에서 제공하는 명령어 사용:
```bash
redis-cli --tls -u redis://default:YOUR_TOKEN@summary-polliwog-43960.upstash.io:6379
```

### 방법 2: Python으로 테스트
```python
import redis
import ssl

REDIS_URL = "redis://default:YOUR_TOKEN@summary-polliwog-43960.upstash.io:6379"

client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    ssl=True
)

# 연결 테스트
try:
    client.ping()
    print("✅ Redis 연결 성공!")
except Exception as e:
    print(f"❌ Redis 연결 실패: {e}")
```

### 방법 3: Docker Compose로 테스트
```bash
# .env 파일 설정 후
docker-compose -f docker-compose.db.yaml up -d customerservice

# 로그 확인
docker-compose -f docker-compose.db.yaml logs customerservice | grep -i redis
```

## ⚠️ 주의사항

### 1. Token 보안
- ✅ `.env` 파일을 Git에 커밋하지 마세요
- ✅ `.gitignore`에 `.env` 추가 확인
- ✅ 프로덕션에서는 환경 변수로 관리

### 2. Token vs Readonly Token
- **Token**: 모든 작업 가능 (읽기/쓰기)
- **Readonly Token**: 읽기 전용 (보안상 더 안전)

### 3. Token 형식
- Token은 긴 문자열입니다 (예: `Aau4AAIncDJlYTkwN2M5ZjNkZj...`)
- 공백이나 줄바꿈 없이 전체를 복사하세요
- 따옴표 없이 입력하세요 (환경 변수는 자동으로 처리)

## 🔄 Token 재생성

Token을 잃어버렸거나 재생성이 필요한 경우:
1. Upstash 대시보드 → `/labzangdb` 선택
2. **RBAC** 탭 이동
3. **Token** 섹션에서 **Regenerate** 클릭
4. 새 Token 복사 후 `.env` 파일 업데이트

## 📊 현재 설정 확인

현재 `.env` 파일에서 Token이 제대로 설정되었는지 확인:

```bash
# .env 파일 확인 (비밀번호는 마스킹)
grep REDIS_PASSWORD .env

# 또는
cat .env | grep REDIS
```

## 🎯 요약

1. **REDIS_PASSWORD = Upstash Token**
2. **위치**: Upstash 대시보드 → Details 탭 → Token
3. **형식**: 긴 문자열 (예: `Aau4AAIncDJlYTkwN2M5ZjNkZj...`)
4. **설정**: `.env` 파일의 `REDIS_PASSWORD`에 Token 입력
5. **REDIS_URL**: `redis://default:TOKEN@host:port` 형식

## 🔗 관련 파일

- `.env` - 환경 변수 설정 파일
- `UPSTASH_REDIS_SETUP.md` - 전체 Upstash Redis 가이드
- `docker-compose.db.yaml` - Docker Compose 설정
