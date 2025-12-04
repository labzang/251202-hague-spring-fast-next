# Docker Compose Profile 사용 가이드

## 🔍 현재 상황

`docker compose up` 명령어를 실행하면 **3개의 기본 서비스**만 실행됩니다:
- gateway (8080)
- oauthservice (8081)
- userservice (8082)

나머지 서비스들은 **profile**로 그룹화되어 있어 명시적으로 지정해야 실행됩니다.

## 📋 서비스 그룹 구조

### 기본 서비스 (profile 없음)
항상 실행되는 Core 서비스:
```
✅ gateway        (8080) - API Gateway
✅ oauthservice   (8081) - OAuth 인증
✅ userservice    (8082) - 사용자 관리
```

### ERP 서비스 (profile: erp)
```
customerservice   (9009) - 고객 관리
dashboardservice  (9008) - 대시보드
orderservice      (9007) - 주문 관리
reportservice     (9006) - 보고서
settingservice    (9005) - 설정
stockservice      (9004) - 재고 관리
```

### AI 서비스 (profile: ai)
```
authservice       (9001) - AI 인증
chatbotservice    (9003) - 챗봇
crawlerservice    (9002) - 크롤러
```

## 🚀 실행 방법

### 1. 기본 서비스만 실행
```powershell
docker compose up
```
→ gateway, oauthservice, userservice만 실행

### 2. ERP 서비스 포함
```powershell
docker compose --profile erp up
```
→ 기본 서비스 + 6개 ERP 서비스 실행

### 3. AI 서비스 포함
```powershell
docker compose --profile ai up
```
→ 기본 서비스 + 3개 AI 서비스 실행

### 4. 모든 서비스 실행
```powershell
docker compose --profile erp --profile ai up
```
→ 총 12개 서비스 모두 실행

### 5. 백그라운드 실행
```powershell
# 기본 서비스만
docker compose up -d

# ERP 포함
docker compose --profile erp up -d

# 모든 서비스
docker compose --profile erp --profile ai up -d
```

## 📊 서비스 확인

### 정의된 모든 서비스 확인
```powershell
docker compose config --services
```

### 실행 중인 컨테이너 확인
```powershell
docker compose ps
```

### 모든 컨테이너 확인 (중지된 것 포함)
```powershell
docker compose ps -a
```

### 사용 가능한 profile 확인
```powershell
docker compose config --profiles
```

## 🔧 특정 서비스만 실행

### 개별 서비스 시작
```powershell
# 특정 서비스만 시작 (의존성 포함)
docker compose up gateway oauthservice

# 특정 서비스만 재시작
docker compose restart oauthservice

# 특정 서비스만 중지
docker compose stop gateway
```

### Profile 서비스 개별 시작
```powershell
# ERP 서비스 중 하나만 시작 (profile 없이는 안됨)
docker compose --profile erp up customerservice

# AI 서비스 중 하나만 시작
docker compose --profile ai up chatbotservice
```

## 📝 실전 예시

### 시나리오 1: 프론트엔드 개발 (OAuth 테스트)
```powershell
# 기본 서비스만 실행
docker compose up -d

# 확인
docker compose ps
# ✅ gateway (8080)
# ✅ oauthservice (8081)
# ✅ userservice (8082)
```

### 시나리오 2: ERP 기능 개발
```powershell
# 기본 + ERP 서비스 실행
docker compose --profile erp up -d

# 확인
docker compose ps
# ✅ 기본 3개 + ERP 6개 = 총 9개
```

### 시나리오 3: AI 챗봇 개발
```powershell
# 기본 + AI 서비스 실행
docker compose --profile ai up -d

# 확인
docker compose ps
# ✅ 기본 3개 + AI 3개 = 총 6개
```

### 시나리오 4: 전체 시스템 테스트
```powershell
# 모든 서비스 실행
docker compose --profile erp --profile ai up -d

# 확인
docker compose ps
# ✅ 기본 3개 + ERP 6개 + AI 3개 = 총 12개
```

## 🛑 서비스 중지

### 실행 중인 서비스 중지
```powershell
# 현재 실행 중인 모든 서비스 중지
docker compose down

# 특정 profile만 중지 (불가능 - down은 모든 서비스 중지)
# 대신 stop 사용
docker compose stop customerservice dashboardservice
```

### 완전히 삭제 (볼륨 포함)
```powershell
docker compose down -v
```

## 📌 포트 맵핑 참고

### Core Services
- 8080: Gateway (API 진입점)
- 8081: OAuth Service
- 8082: User Service

### ERP Services (9000번대)
- 9004: Stock Service
- 9005: Setting Service
- 9006: Report Service
- 9007: Order Service
- 9008: Dashboard Service
- 9009: Customer Service

### AI Services (9000번대)
- 9001: Auth Service
- 9002: Crawler Service
- 9003: Chatbot Service

## 💡 Profile 사용 이유

### 장점
1. **리소스 절약**: 필요한 서비스만 실행
2. **개발 효율**: 작업 중인 모듈만 실행
3. **빠른 시작**: 전체 서비스 대신 필요한 것만
4. **명확한 그룹화**: 서비스를 논리적으로 그룹화

### 예시
```
개발자 A (프론트엔드):     docker compose up
개발자 B (ERP 백엔드):      docker compose --profile erp up
개발자 C (AI 개발):         docker compose --profile ai up
통합 테스트:                docker compose --profile erp --profile ai up
```

## 🔄 Profile 없이 모든 서비스 실행하려면?

docker-compose.yaml에서 각 서비스의 `profiles:` 섹션을 제거하면 됩니다.

### 수정 전
```yaml
customerservice:
  build:
    context: ./erp.labzang.com
  profiles:
    - erp  # 이 줄 제거
```

### 수정 후
```yaml
customerservice:
  build:
    context: ./erp.labzang.com
  # profiles 섹션 제거됨
```

하지만 **권장하지 않습니다**. 12개 서비스를 모두 실행하면:
- 메모리: ~6-8GB 사용
- CPU: 높은 사용률
- 시작 시간: 3-5분

## 📚 관련 명령어 요약

```powershell
# 확인
docker compose config --services    # 모든 서비스 목록
docker compose config --profiles    # 사용 가능한 profile 목록
docker compose ps                   # 실행 중인 컨테이너

# 실행
docker compose up                            # 기본 서비스
docker compose --profile erp up             # 기본 + ERP
docker compose --profile ai up              # 기본 + AI
docker compose --profile erp --profile ai up # 모든 서비스

# 백그라운드
docker compose up -d
docker compose --profile erp up -d

# 중지
docker compose down                 # 모든 서비스 중지 및 제거
docker compose stop                 # 중지 (컨테이너 유지)
docker compose restart SERVICE_NAME # 특정 서비스 재시작

# 로그
docker compose logs SERVICE_NAME    # 특정 서비스 로그
docker compose logs -f              # 실시간 로그
docker compose logs --tail 50       # 최근 50줄
```

## ⚠️ 주의사항

1. **Profile 지정 없이 up 하면**: 기본 3개만 실행됨
2. **down은 profile 무관**: 모든 컨테이너를 중지/제거
3. **Profile은 up/start에서만 필요**: restart, stop, logs는 profile 불필요
4. **여러 profile 동시 사용 가능**: `--profile erp --profile ai`

## 🎯 추천 사용 패턴

### 일상 개발
```powershell
# 아침: 필요한 서비스만 시작
docker compose --profile erp up -d

# 저녁: 모든 서비스 종료
docker compose down
```

### 특정 기능 테스트
```powershell
# 1. 기본 서비스 시작
docker compose up -d

# 2. 필요한 서비스 추가
docker compose --profile erp up -d customerservice

# 3. 테스트 후 정리
docker compose down
```

### CI/CD 환경
```powershell
# 모든 서비스 빌드 및 테스트
docker compose --profile erp --profile ai build
docker compose --profile erp --profile ai up -d
# 테스트 실행...
docker compose down
```

