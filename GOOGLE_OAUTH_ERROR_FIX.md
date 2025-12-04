# Google OAuth 인증 에러 해결 가이드

## 🔍 에러 내용

```
Access blocked: Authorization Error
Error 401: invalid_client
The OAuth client was not found.
```

**URL에서 확인된 문제:**
- `client_id=your_googl` → 플레이스홀더 값이 그대로 사용됨

## 📋 원인 분석

### 1. 환경 변수 미설정
- `.env` 파일에 `GOOGLE_CLIENT_ID`가 설정되지 않았거나
- 플레이스홀더 값(`your_google_client_id`)이 그대로 사용되고 있음

### 2. Google OAuth Client ID 미생성
- Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하지 않았거나
- 생성했지만 프로젝트에 설정하지 않음

### 3. 리다이렉트 URI 불일치
- Google Cloud Console에 등록된 리다이렉트 URI와
- 애플리케이션에서 사용하는 리다이렉트 URI가 일치하지 않음

## ✅ 해결 방법

### 1단계: Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/ 접속
   - 프로젝트 선택 또는 새 프로젝트 생성

2. **API 및 서비스 > 사용자 인증 정보**
   - 좌측 메뉴: "API 및 서비스" > "사용자 인증 정보"
   - 상단 "+ 사용자 인증 정보 만들기" > "OAuth 클라이언트 ID"

3. **OAuth 동의 화면 설정** (처음인 경우)
   - 사용자 유형: 외부 선택
   - 앱 정보 입력:
     - 앱 이름: `Labzang Platform` (또는 원하는 이름)
     - 사용자 지원 이메일: 본인 이메일
     - 개발자 연락처 정보: 본인 이메일
   - 범위: 기본값 유지
   - 테스트 사용자: 본인 이메일 추가

4. **OAuth 클라이언트 ID 생성**
   - 애플리케이션 유형: **웹 애플리케이션**
   - 이름: `Labzang OAuth Client` (또는 원하는 이름)
   - 승인된 리다이렉트 URI 추가:
     ```
     http://localhost:8080/auth/google/callback
     http://localhost:4000/login/callback
     ```
     (프로덕션 환경의 경우 실제 도메인도 추가)

5. **클라이언트 ID 및 시크릿 복사**
   - 생성 후 표시되는 **클라이언트 ID**와 **클라이언트 시크릿** 복사

### 2단계: .env 파일에 설정 추가

프로젝트 루트의 `.env` 파일에 다음 값들을 추가/수정:

```env
# Google OAuth 설정
GOOGLE_CLIENT_ID=여기에_실제_클라이언트_ID_붙여넣기
GOOGLE_CLIENT_SECRET=여기에_실제_클라이언트_시크릿_붙여넣기
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

**예시:**
```env
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

### 3단계: Docker 컨테이너 재시작

환경 변수를 변경했으므로 Docker 컨테이너를 재시작해야 합니다:

```powershell
# 컨테이너 중지
docker compose down

# 컨테이너 재시작
docker compose up
```

또는 특정 서비스만 재시작:

```powershell
# oauthservice만 재시작
docker compose restart oauthservice
```

### 4단계: 확인

1. **환경 변수 확인**
   ```powershell
   # oauthservice 컨테이너에서 환경 변수 확인
   docker compose exec oauthservice env | grep GOOGLE
   ```

2. **로그 확인**
   ```powershell
   # oauthservice 로그 확인
   docker compose logs oauthservice
   ```

3. **브라우저에서 테스트**
   - `http://localhost:4000/login` 접속
   - "Google로 계속하기" 버튼 클릭
   - Google 로그인 페이지가 정상적으로 표시되는지 확인

## 🔧 추가 문제 해결

### 문제 1: "redirect_uri_mismatch" 에러

**원인:** Google Cloud Console에 등록된 리다이렉트 URI와 애플리케이션에서 사용하는 URI가 다름

**해결:**
1. Google Cloud Console > 사용자 인증 정보 > OAuth 클라이언트 ID 편집
2. "승인된 리다이렉트 URI"에 다음 추가:
   - `http://localhost:8080/auth/google/callback`
   - `http://localhost:4000/login/callback`
   - 프로덕션 도메인 (배포 시)

### 문제 2: "access_denied" 에러

**원인:** OAuth 동의 화면에서 테스트 사용자로 등록되지 않음

**해결:**
1. Google Cloud Console > API 및 서비스 > OAuth 동의 화면
2. "테스트 사용자" 섹션에 본인 이메일 추가

### 문제 3: 환경 변수가 적용되지 않음

**원인:** Docker 컨테이너가 환경 변수를 읽지 못함

**해결:**
```powershell
# 1. .env 파일 위치 확인 (프로젝트 루트에 있어야 함)
# 2. docker-compose.yaml에서 env_file 경로 확인
# 3. 컨테이너 완전히 재생성
docker compose down
docker compose up --build
```

## 📝 참고 사항

### 현재 프로젝트 구조

```
프론트엔드 (admin.labzang.com)
  ↓ POST /auth/google/login
Gateway (api.labzang.com:8080)
  ↓ 라우팅
OAuth Service (oauthservice:8081)
  ↓ Google OAuth URL 생성
Google OAuth
  ↓ 콜백
OAuth Service
  ↓ JWT 토큰 생성
프론트엔드 (콜백 페이지)
```

### 관련 파일 위치

- **OAuth 설정**: `core.labzang.com/oauthservice/src/main/resources/application.yaml`
- **Google Controller**: `core.labzang.com/oauthservice/src/main/java/com/labzang/api/google/GoogleController.java`
- **Docker Compose**: `docker-compose.yaml` (oauthservice 섹션)
- **프론트엔드 로그인**: `admin.labzang.com/app/login/page.tsx`

### 환경 변수 체크리스트

- [ ] `GOOGLE_CLIENT_ID` - Google Cloud Console에서 생성한 클라이언트 ID
- [ ] `GOOGLE_CLIENT_SECRET` - Google Cloud Console에서 생성한 클라이언트 시크릿
- [ ] `GOOGLE_REDIRECT_URI` - OAuth 콜백 URI (일반적으로 `http://localhost:8080/auth/google/callback`)

## 🚀 빠른 해결 체크리스트

1. ✅ Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성
2. ✅ `.env` 파일에 `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` 설정
3. ✅ Google Cloud Console에 리다이렉트 URI 등록
4. ✅ Docker 컨테이너 재시작
5. ✅ 브라우저에서 로그인 테스트

## ⚠️ 보안 주의사항

- **절대 `.env` 파일을 Git에 커밋하지 마세요!**
- `.gitignore`에 `.env`가 포함되어 있는지 확인
- 프로덕션 환경에서는 환경 변수를 안전하게 관리 (예: Docker secrets, Kubernetes secrets)

