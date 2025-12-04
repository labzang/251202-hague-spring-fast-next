# .env 파일 설정 가이드

## 📋 개요

이 가이드는 Neon PostgreSQL과 Upstash Redis를 사용하는 `.env` 파일 설정 방법을 설명합니다.

## 🔧 설정 단계

### 1. Neon PostgreSQL 정보 가져오기

1. [Neon Console](https://console.neon.tech)에 로그인
2. 프로젝트 선택
3. **Connection Details** 또는 **Connection String** 확인
4. 다음 정보 복사:
   - Connection String (DATABASE_URL)
   - Host
   - Database name
   - User
   - Password

**Neon Connection String 형식:**
```
postgresql://user:password@ep-xxx-xxx.region.neon.tech/database?sslmode=require
```

### 2. Upstash Redis 정보 가져오기

1. [Upstash Console](https://console.upstash.com)에 로그인
2. `/labzangdb` Redis 인스턴스 선택
3. **Connect** 섹션 → **TCP** 탭 클릭
4. **Read-Only Token** 체크 해제 (쓰기 권한 필요)
5. `REDIS_URL` 복사 또는 Token 복사

**Upstash Redis URL 형식:**
```
rediss://default:TOKEN@summary-polliwog-43960.upstash.io:6379
```

### 3. .env 파일 생성

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집
# Neon과 Upstash 정보 입력
```

## 📝 .env 파일 구조

### Neon PostgreSQL 설정
```env
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.neon.tech/database?sslmode=require
DB_HOST=ep-xxx-xxx.region.neon.tech
DB_PORT=5432
DB_NAME=database
DB_USER=user
DB_PASSWORD=password
DB_SSL_MODE=require
```

### Upstash Redis 설정
```env
REDIS_URL=rediss://default:TOKEN@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=TOKEN
REDIS_SSL_ENABLED=true
REDIS_SSL_CERT_REQS=required
```

## ✅ 설정 확인

### 1. Neon PostgreSQL 연결 테스트
```bash
# psql로 테스트
psql "postgresql://user:password@ep-xxx-xxx.region.neon.tech/database?sslmode=require"

# 또는 Python으로 테스트
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('✅ 연결 성공!' if engine.connect() else '❌ 연결 실패')"
```

### 2. Upstash Redis 연결 테스트
```bash
# redis-cli로 테스트
redis-cli --tls -u "$REDIS_URL"

# 또는 Python으로 테스트
python -c "import redis, ssl, os; client = redis.from_url(os.getenv('REDIS_URL'), ssl_cert_reqs=ssl.CERT_REQUIRED, ssl=True); print('✅ 연결 성공!' if client.ping() else '❌ 연결 실패')"
```

### 3. Docker Compose로 테스트
```bash
# 환경 변수 로드 확인
docker-compose -f docker-compose.db.yaml config

# 서비스 실행
docker-compose -f docker-compose.db.yaml up -d

# 로그 확인
docker-compose -f docker-compose.db.yaml logs | grep -i "database\|redis"
```

## 🔐 보안 주의사항

1. **.gitignore 확인**: `.env` 파일이 Git에 커밋되지 않도록 확인
2. **권한 설정**: `.env` 파일 권한을 `600`으로 설정 (선택사항)
   ```bash
   chmod 600 .env
   ```
3. **환경 변수 분리**: 프로덕션과 개발 환경 분리
4. **Token 보안**: Token을 공유하지 마세요

## 🎯 빠른 설정 체크리스트

- [ ] Neon PostgreSQL Connection String 복사
- [ ] Neon DB_HOST, DB_NAME, DB_USER, DB_PASSWORD 설정
- [ ] Upstash Redis TCP Token 복사
- [ ] REDIS_URL 및 REDIS_PASSWORD 설정
- [ ] JWT_SECRET 설정 (프로덕션용 강력한 키)
- [ ] OAuth 설정 (Kakao, Google)
- [ ] .env 파일이 .gitignore에 포함되어 있는지 확인
- [ ] 연결 테스트 완료

## 📞 문제 해결

### Neon 연결 실패
- SSL 모드 확인 (`sslmode=require`)
- 방화벽 설정 확인
- Connection String 형식 확인

### Upstash 연결 실패
- TLS/SSL 설정 확인 (`rediss://` 사용)
- Token이 올바른지 확인
- Read-Only Token이 아닌 일반 Token 사용 확인

## 🔗 관련 파일

- `.env` - 실제 환경 변수 파일 (Git에 커밋하지 않음)
- `.env.example` - 환경 변수 템플릿
- `ENV_SETUP_GUIDE.md` - 이 가이드 파일
