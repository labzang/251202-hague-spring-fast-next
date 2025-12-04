# Docker Compose 통합 가이드

## 📋 파일 구조 변경 사항

### 이전 구조 (분리)
- `docker-compose.yaml` - 로컬 개발용 (기본 서비스만)
- `docker-compose.db.yaml` - Railway/Neon DB 연동용 (모든 서비스)
- `database-config.yaml` - 설정 참조용

### 현재 구조 (통합)
- `docker-compose.yaml` - **통합 파일** (모든 서비스, profiles로 구분)
- `database-config.yaml` - 설정 참조용 (유지)

## ✅ 통합의 장점

1. **단일 파일 관리**: 하나의 파일로 모든 서비스 관리
2. **Profiles 활용**: 서비스 그룹을 선택적으로 실행
3. **환경 변수 통일**: `.env` 파일 하나로 모든 설정 관리
4. **유지보수 용이**: 중복 제거, 일관성 향상

## 🚀 사용 방법

### 1. 기본 서비스만 실행
```bash
docker compose up
```
실행되는 서비스:
- gateway (8080)
- oauthservice (8081)
- userservice (8082)

### 2. ERP 서비스 포함
```bash
docker compose --profile erp up
```
추가 실행되는 서비스:
- customerservice (9009)
- dashboardservice (9008)
- orderservice (9007)
- reportservice (9006)
- settingservice (9005)
- stockservice (9004)

### 3. AI 서비스 포함
```bash
docker compose --profile ai up
```
추가 실행되는 서비스:
- ai-authservice (9002)
- crawlerservice (9001)
- chatbotservice (9003)

### 4. 모든 서비스 실행
```bash
docker compose --profile erp --profile ai up
```

### 5. 백그라운드 실행
```bash
docker compose --profile erp --profile ai up -d
```

## 🔧 환경 변수 설정

### .env 파일 구조
```env
# Neon PostgreSQL
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.neon.tech/database?sslmode=require
DB_HOST=ep-xxx-xxx.region.neon.tech
DB_PORT=5432
DB_NAME=database
DB_USER=user
DB_PASSWORD=password

# Upstash Redis
REDIS_URL=rediss://default:token@summary-polliwog-43960.upstash.io:6379
REDIS_HOST=summary-polliwog-43960.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=token
REDIS_SSL_ENABLED=true

# JWT & OAuth
JWT_SECRET=your-secret-key
KAKAO_REST_API_KEY=your_key
GOOGLE_CLIENT_ID=your_id
# ... 기타 설정
```

## 📊 서비스 포트 매핑

| 서비스 | 포트 | Profile | 설명 |
|--------|------|---------|------|
| gateway | 8080 | 기본 | API Gateway |
| oauthservice | 8081 | 기본 | OAuth 인증 |
| userservice | 8082 | 기본 | 사용자 관리 |
| customerservice | 9009 | erp | 고객 관리 |
| dashboardservice | 9008 | erp | 대시보드 |
| orderservice | 9007 | erp | 주문 관리 |
| reportservice | 9006 | erp | 리포트 |
| settingservice | 9005 | erp | 설정 |
| stockservice | 9004 | erp | 재고 관리 |
| ai-authservice | 9002 | ai | AI 인증 |
| crawlerservice | 9001 | ai | 크롤링 |
| chatbotservice | 9003 | ai | 챗봇 |

## 🔄 마이그레이션 가이드

### 이전 사용법
```bash
# 기본 서비스
docker compose up

# DB 연동 서비스
docker compose -f docker-compose.db.yaml up
docker compose -f docker-compose.db.yaml --profile erp up
```

### 현재 사용법
```bash
# 기본 서비스 (동일)
docker compose up

# DB 연동 서비스 (통합됨)
docker compose up  # .env 파일만 설정하면 자동으로 DB 연동
docker compose --profile erp up
```

## ⚙️ 환경별 설정

### 로컬 개발
`.env` 파일에서:
```env
SPRING_PROFILES_ACTIVE=default
SPRING_JPA_SHOW_SQL=true
DEBUG=true
```

### 프로덕션
`.env` 파일에서:
```env
SPRING_PROFILES_ACTIVE=production
SPRING_JPA_SHOW_SQL=false
DEBUG=false
```

## 🗑️ 제거된 파일

다음 파일은 더 이상 필요하지 않습니다:
- ~~`docker-compose.db.yaml`~~ → `docker-compose.yaml`에 통합됨

**주의**: 기존에 `docker-compose.db.yaml`을 사용하던 경우, 이제 `docker-compose.yaml`을 사용하세요.

## 📝 database-config.yaml

`database-config.yaml`은 **참고용 설정 파일**입니다:
- 실제 연결은 `.env` 파일의 환경 변수 사용
- 설정 구조와 스키마 정보 참고용
- 코드에서 직접 읽지 않음

## 🔍 문제 해결

### 환경 변수가 적용되지 않을 때
```bash
# .env 파일 위치 확인
ls -la .env

# 환경 변수 확인
docker compose config | grep DATABASE_URL
```

### 서비스가 시작되지 않을 때
```bash
# 로그 확인
docker compose logs [service-name]

# 전체 로그
docker compose logs
```

## 🎯 요약

1. ✅ **통합 완료**: `docker-compose.yaml` 하나로 모든 서비스 관리
2. ✅ **Profiles 활용**: `--profile erp`, `--profile ai`로 선택적 실행
3. ✅ **환경 변수 통일**: `.env` 파일 하나로 모든 설정
4. ✅ **database-config.yaml 유지**: 참고용 설정 파일

