# Docker 설정 가이드

## Docker Desktop 실행 확인

Docker Compose를 실행하기 전에 Docker Desktop이 실행 중이어야 합니다.

### 확인 방법

```powershell
# Docker 버전 확인 (Docker Desktop이 실행 중이면 정상 출력)
docker version

# Docker 컨테이너 목록 확인
docker ps
```

### Docker Desktop이 실행되지 않는 경우

1. **Windows 시작 메뉴에서 Docker Desktop 실행**
   - 시작 메뉴 → "Docker Desktop" 검색 → 실행

2. **시스템 트레이 확인**
   - 작업 표시줄 오른쪽 하단의 시스템 트레이에서 Docker 아이콘 확인
   - Docker 아이콘이 회색이면 아직 시작 중
   - Docker 아이콘이 초록색이면 실행 중

3. **Docker Desktop 완전 시작 대기**
   - Docker Desktop을 처음 실행하면 1-2분 정도 소요될 수 있습니다
   - "Docker Desktop is starting..." 메시지가 사라질 때까지 대기

4. **Docker Desktop 재시작**
   - 시스템 트레이에서 Docker 아이콘 우클릭 → "Quit Docker Desktop"
   - 몇 초 후 다시 Docker Desktop 실행

### 에러 해결

**에러: `The system cannot find the file specified`**
- Docker Desktop이 실행되지 않았거나 완전히 시작되지 않음
- 위의 단계를 따라 Docker Desktop을 실행하고 완전히 시작될 때까지 대기

## 환경 변수 설정 (선택사항)

개발 환경에서 OAuth 기능을 사용하려면 환경 변수를 설정해야 합니다.

### .env 파일 생성

```powershell
# api.labzang.com/.env 파일 생성
cd api.labzang.com
Copy-Item .env.example .env
# .env 파일을 열어서 실제 값으로 수정
```

### 필수 환경 변수

- `KAKAO_REST_API_KEY`: 카카오 REST API 키
- `KAKAO_REDIRECT_URI`: 카카오 OAuth 리다이렉트 URI
- `GOOGLE_CLIENT_ID`: 구글 OAuth 클라이언트 ID
- `GOOGLE_CLIENT_SECRET`: 구글 OAuth 클라이언트 시크릿
- `GOOGLE_REDIRECT_URI`: 구글 OAuth 리다이렉트 URI
- `JWT_SECRET`: JWT 토큰 서명용 시크릿 키 (최소 32자)

### 기본값

환경 변수가 설정되지 않아도 서비스는 시작되지만, OAuth 기능은 작동하지 않습니다.
기본값이 설정되어 있어 경고만 표시되고 서비스는 정상적으로 시작됩니다.

## Docker Compose 실행

```powershell
# 기본 스택 실행
docker compose up

# 백그라운드 실행
docker compose up -d

# AI 서비스 포함 실행
docker compose --profile ai up

# 중지
docker compose down
```

