# Railway 데이터베이스 연동 가이드

## 📋 개요

이 가이드는 Railway PostgreSQL과 Redis를 모든 서비스에 연동하는 방법을 설명합니다.

## 🚀 Railway 설정

### 1. PostgreSQL 서비스 생성

1. Railway 프로젝트에서 **Add Service** → **Database** → **PostgreSQL** 선택
2. 생성 후 **Variables** 탭에서 연결 정보 확인:
   ```
   DATABASE_URL=postgresql://postgres:password@junction.proxy.rlwy.net:port/railway
   PGHOST=junction.proxy.rlwy.net
   PGPORT=5432
   PGDATABASE=railway
   PGUSER=postgres
   PGPASSWORD=your_password
   ```

### 2. Redis 서비스 생성 (선택사항)

1. Railway 프로젝트에서 **Add Service** → **Database** → **Redis** 선택
2. 생성 후 연결 정보 확인:
   ```
   REDIS_URL=redis://:password@redis-12345.railway.app:6379
   REDIS_HOST=redis-12345.railway.app
   REDIS_PORT=6379
   REDIS_PASSWORD=your_redis_password
   ```

## 🔧 로컬 개발 설정

### 1. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집하여 Railway 정보 입력
```

### 2. .env 파일 예시

```env
# Railway PostgreSQL
DATABASE_URL=postgresql://postgres:your_password@junction.proxy.rlwy.net:12345/railway
DB_HOST=junction.proxy.rlwy.net
DB_PORT=12345
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=your_password
DB_SSL_MODE=require

# Railway Redis (선택사항)
REDIS_URL=redis://:your_redis_password@redis-12345.railway.app:6379
REDIS_HOST=redis-12345.railway.app
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_SSL_ENABLED=true

# JWT 설정
JWT_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
JWT_ACCESS_TOKEN_EXPIRATION=3600000
JWT_REFRESH_TOKEN_EXPIRATION=2592000000

# OAuth 설정
KAKAO_REST_API_KEY=your_kakao_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 🐳 Docker Compose 실행

### 기본 서비스 (Gateway + Core)
```bash
docker-compose -f docker-compose.db.yaml up
```

### ERP 서비스 포함
```bash
docker-compose -f docker-compose.db.yaml --profile erp up
```

### AI 서비스 포함
```bash
docker-compose -f docker-compose.db.yaml --profile ai up
```

### 모든 서비스
```bash
docker-compose -f docker-compose.db.yaml --profile erp --profile ai up
```

## 📊 데이터베이스 스키마 구조

### 자동 생성되는 스키마

| 서비스 | 스키마명 | 설명 |
|--------|----------|------|
| OAuth Service | `labzang_oauth` | OAuth 인증 데이터 |
| User Service | `labzang_user` | 사용자 관리 데이터 |
| Customer Service | `labzang_customer` | 고객 관리 데이터 |
| Dashboard Service | `labzang_dashboard` | 대시보드 데이터 |
| Order Service | `labzang_order` | 주문 관리 데이터 |
| Report Service | `labzang_report` | 리포트 데이터 |
| Setting Service | `labzang_setting` | 설정 데이터 |
| Stock Service | `labzang_stock` | 재고 관리 데이터 |
| AI Auth Service | `labzang_ai_auth` | AI 인증 데이터 |
| Chatbot Service | `labzang_chatbot` | 챗봇 데이터 |
| Crawler Service | `labzang_crawler` | 크롤링 데이터 |

## 🔌 서비스별 연결 설정

### Spring Boot 서비스 (Java)

**application-railway.yaml** 파일이 각 서비스에 생성됩니다:

- `api.labzang.com/src/main/resources/application-railway.yaml`
- `core.labzang.com/oauthservice/src/main/resources/application-railway.yaml`
- `core.labzang.com/userservice/src/main/resources/application-railway.yaml`

### FastAPI 서비스 (Python)

**database.py** 파일이 각 서비스 그룹에 생성됩니다:

- `erp.labzang.com/common/database.py`
- `ai.labzang.com/common/database.py`

## 🧪 연결 테스트

### PostgreSQL 연결 테스트
```bash
# Python 서비스
cd erp.labzang.com
python common/database.py

# 또는
cd ai.labzang.com
python common/database.py
```

### Spring Boot 서비스 테스트
```bash
# 서비스 실행 후 헬스 체크
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
curl http://localhost:8082/actuator/health
```

## 🔍 모니터링

### 데이터베이스 연결 상태 확인

1. **Railway 대시보드**에서 PostgreSQL 서비스 메트릭 확인
2. **애플리케이션 로그**에서 연결 상태 확인
3. **헬스 체크 엔드포인트** 활용

### 로그 확인
```bash
# 특정 서비스 로그
docker-compose -f docker-compose.db.yaml logs -f gateway
docker-compose -f docker-compose.db.yaml logs -f customerservice

# 모든 서비스 로그
docker-compose -f docker-compose.db.yaml logs -f
```

## 🚨 트러블슈팅

### 1. 연결 실패
- `.env` 파일의 데이터베이스 정보 확인
- Railway 서비스 상태 확인
- 방화벽/네트워크 설정 확인

### 2. 스키마 생성 실패
- 데이터베이스 권한 확인
- 스키마명 중복 확인

### 3. Redis 연결 실패
- Redis 서비스 활성화 상태 확인
- SSL 설정 확인

## 📝 주의사항

1. **보안**: `.env` 파일을 Git에 커밋하지 마세요
2. **백업**: 중요한 데이터는 정기적으로 백업하세요
3. **모니터링**: Railway 사용량을 정기적으로 확인하세요
4. **스키마**: 각 서비스는 독립된 스키마를 사용합니다

## 🔗 관련 파일

- `.env.example` - 환경 변수 템플릿
- `database-config.yaml` - 데이터베이스 설정 파일
- `docker-compose.db.yaml` - Railway 연동 Docker Compose
- `DATABASE_SETUP.md` - 이 가이드 파일

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. Railway 서비스 상태
2. 환경 변수 설정
3. 네트워크 연결
4. 애플리케이션 로그
