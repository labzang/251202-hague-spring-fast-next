# .env 파일 생성 가이드

## 📋 개요

Neon PostgreSQL과 Upstash Redis 정보를 사용하여 `.env` 파일을 생성하는 방법입니다.

## 🚀 빠른 시작

### 1. 템플릿 복사
```bash
cp .env.template .env
```

### 2. Neon PostgreSQL 정보 입력

1. [Neon Console](https://console.neon.tech) 접속
2. 프로젝트 선택 → **Connection Details** 확인
3. Connection String 복사
4. `.env` 파일에서 다음 값 수정:

```env
# Neon Connection String 예시
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.neon.tech/database?sslmode=require
DB_HOST=ep-xxx-xxx.region.neon.tech
DB_PORT=5432
DB_NAME=database
DB_USER=user
DB_PASSWORD=password
```

### 3. Upstash Redis 정보 확인

이미 `.env.template`에 설정되어 있습니다:
- ✅ `REDIS_URL`: 이미 설정됨
- ✅ `REDIS_PASSWORD`: 이미 설정됨
- ✅ `UPSTASH_REDIS_REST_TOKEN`: 이미 설정됨

필요시 Upstash 대시보드에서 확인:
- [Upstash Console](https://console.upstash.com) → `/labzangdb` → TCP 탭

## 📝 완성된 .env 파일 예시

```env
# ========================================================================
# Neon PostgreSQL
# ========================================================================
DATABASE_URL=postgresql://neondb_owner:your_password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
DB_HOST=ep-cool-darkness-123456.us-east-2.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your_neon_password
DB_SSL_MODE=require

# ========================================================================
# Upstash Redis (이미 설정됨)
# ========================================================================
REDIS_URL=rediss://default:Aau4AAIncDJ1YTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=Aau4AAIncDJ1YTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required

UPSTASH_REDIS_REST_URL=https://summary-polliwog-43960.upstash.io
UPSTASH_REDIS_REST_TOKEN=Aau4AAIncDJlYTkwN2M5ZjNkZjQ0ZWRlOGIyMzZjNTc1YmI4YTcxMnAyNDM5NjA

# ========================================================================
# JWT 설정
# ========================================================================
JWT_SECRET=your-super-secret-jwt-key-change-in-production-minimum-32-characters-long
JWT_ACCESS_TOKEN_EXPIRATION=3600000
JWT_REFRESH_TOKEN_EXPIRATION=2592000000

# ========================================================================
# OAuth 설정
# ========================================================================
KAKAO_REST_API_KEY=your_kakao_rest_api_key
KAKAO_REDIRECT_URI=http://localhost:8080/auth/kakao/callback
GOOGLE_CLIENT_ID= 

GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

## ✅ 설정 확인

### 1. Neon 연결 테스트
```bash
# .env 파일 로드 후
source .env  # 또는 export $(cat .env | xargs)

# psql로 테스트
psql "$DATABASE_URL"
```

### 2. Upstash 연결 테스트
```bash
# redis-cli로 테스트
redis-cli --tls -u "$REDIS_URL"

# 또는 Python으로 테스트
python -c "import redis, ssl, os; from dotenv import load_dotenv; load_dotenv(); client = redis.from_url(os.getenv('REDIS_URL'), ssl_cert_reqs=ssl.CERT_REQUIRED, ssl=True); print('✅ 연결 성공!' if client.ping() else '❌ 연결 실패')"
```

### 3. Docker Compose 테스트
```bash
# 환경 변수 확인
docker-compose -f docker-compose.db.yaml config

# 서비스 실행
docker-compose -f docker-compose.db.yaml up -d
```

## 🔐 보안 주의사항

1. ✅ `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
2. ✅ `.env` 파일을 Git에 커밋하지 마세요
3. ✅ 프로덕션에서는 환경 변수로 관리
4. ✅ Token과 Password를 공유하지 마세요

## 📞 문제 해결

### Neon 연결 실패
- Connection String 형식 확인
- SSL 모드 확인 (`sslmode=require`)
- 방화벽 설정 확인

### Upstash 연결 실패
- TLS/SSL 설정 확인 (`rediss://` 사용)
- Token이 올바른지 확인
- Read-Only Token이 아닌 일반 Token 사용 확인

## 🔗 관련 파일

- `.env.template` - 환경 변수 템플릿
- `CREATE_ENV_FILE.md` - 이 가이드 파일
- `ENV_SETUP_GUIDE.md` - 상세 설정 가이드
