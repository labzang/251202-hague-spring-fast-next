# .env 파일 플레이스홀더 값 에러

## 🔍 발견된 문제

`.env` 파일에 **실제 값 대신 플레이스홀더 값**이 그대로 사용되고 있습니다.

### 현재 `.env` 파일 상태

```env
GOOGLE_CLIENT_ID=your_google_client_id          ❌ 플레이스홀더
GOOGLE_CLIENT_SECRET=your_google_client_secret  ❌ 플레이스홀더
```

### 컨테이너에서 확인된 값

```bash
$ docker compose exec oauthservice env | findstr GOOGLE
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

### 로그에서 확인된 문제

```
oauthservice  | Writing [{auth_url=https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=your_google_clie (truncated)...]
```

→ **`client_id=your_google_clie`** 라는 잘못된 값이 Google로 전송됨

## 📋 에러 발생 원인

Google OAuth는 `your_google_client_id`라는 클라이언트 ID를 찾을 수 없어서:
```
Error 401: invalid_client
The OAuth client was not found.
```

## ✅ 해결 방법

### 1단계: Google Cloud Console에서 실제 OAuth 클라이언트 ID 가져오기

#### 방법 A: 기존 클라이언트 ID 확인

1. https://console.cloud.google.com/apis/credentials 접속
2. 프로젝트 선택
3. "OAuth 2.0 클라이언트 ID" 섹션에서 기존 클라이언트 확인
4. 클라이언트 이름 클릭 → **클라이언트 ID**와 **클라이언트 보안 비밀번호** 복사

#### 방법 B: 새 클라이언트 ID 생성

1. https://console.cloud.google.com/apis/credentials 접속
2. "+ 사용자 인증 정보 만들기" > "OAuth 클라이언트 ID"
3. 애플리케이션 유형: **웹 애플리케이션**
4. 이름: `Labzang OAuth Client`
5. **승인된 리다이렉트 URI** 추가:
   ```
   http://localhost:8080/auth/google/callback
   http://localhost:4000/login/callback
   ```
6. "만들기" 클릭
7. 표시되는 **클라이언트 ID**와 **클라이언트 보안 비밀번호** 복사

### 2단계: .env 파일 수정

프로젝트 루트의 `.env` 파일을 편집기로 열어서 수정:

#### 수정 전 (현재 - 잘못됨)
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

#### 수정 후 (실제 값으로 교체)
```env
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

**⚠️ 주의:**
- `123456789-abcdefghijklmnop.apps.googleusercontent.com` 부분을 **실제 클라이언트 ID**로 교체
- `GOCSPX-abcdefghijklmnopqrstuvwxyz` 부분을 **실제 클라이언트 시크릿**으로 교체

### 3단계: Docker 컨테이너 재시작

```powershell
# oauthservice 재시작
docker compose restart oauthservice

# 또는 모든 서비스 재시작
docker compose down
docker compose up
```

### 4단계: 확인

#### 환경 변수 확인
```powershell
docker compose exec oauthservice env | findstr GOOGLE
```

**올바른 출력 예시:**
```
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
```

#### 브라우저에서 테스트
1. http://localhost:4000/login 접속
2. "Google로 계속하기" 버튼 클릭
3. Google 로그인 페이지가 정상적으로 표시되는지 확인

## 🔧 실제 클라이언트 ID 형식

### 올바른 형식 예시

**클라이언트 ID:**
```
123456789-abc123def456ghi789jkl012mno345pqr678.apps.googleusercontent.com
```

**클라이언트 시크릿:**
```
GOCSPX-abcdefghijklmnopqrstuvwxyz123456
```

### 잘못된 형식 (플레이스홀더)

```
your_google_client_id          ❌
your_id                        ❌
YOUR_CLIENT_ID_HERE            ❌
```

## 📝 다른 OAuth 제공자도 확인

같은 방식으로 다른 OAuth 설정도 확인하세요:

### Kakao OAuth
```env
KAKAO_REST_API_KEY=실제_카카오_REST_API_키
KAKAO_REDIRECT_URI=http://localhost:8080/auth/kakao/callback
```

### Naver OAuth (추가 시)
```env
NAVER_CLIENT_ID=실제_네이버_클라이언트_ID
NAVER_CLIENT_SECRET=실제_네이버_클라이언트_시크릿
NAVER_REDIRECT_URI=http://localhost:8080/auth/naver/callback
```

## 💡 .env 파일 템플릿 vs 실제 파일

### .env.example (템플릿 - Git에 커밋 가능)
```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### .env (실제 사용 - Git에 커밋 금지)
```env
# Google OAuth
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
```

## ⚠️ 보안 주의사항

1. **.env 파일을 절대 Git에 커밋하지 마세요!**
   - `.gitignore`에 `.env`가 포함되어 있는지 확인
   
2. **실제 클라이언트 ID와 시크릿은 안전하게 보관**
   - 팀원과 공유 시 안전한 방법 사용 (예: 1Password, LastPass)
   
3. **프로덕션 환경에서는 환경 변수를 안전하게 관리**
   - Docker secrets
   - Kubernetes secrets
   - Railway/Vercel 환경 변수

## 🚀 해결 체크리스트

- [ ] Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성 또는 확인
- [ ] 실제 클라이언트 ID 복사 (형식: `xxx.apps.googleusercontent.com`)
- [ ] 실제 클라이언트 시크릿 복사 (형식: `GOCSPX-xxx`)
- [ ] `.env` 파일에서 플레이스홀더 값을 실제 값으로 교체
- [ ] `docker compose restart oauthservice` 실행
- [ ] 환경 변수 확인: `docker compose exec oauthservice env | findstr GOOGLE`
- [ ] 브라우저에서 Google 로그인 테스트

## 📚 관련 문서

- `GOOGLE_OAUTH_ERROR_FIX.md` - Google OAuth 에러 상세 가이드
- `CREATE_ENV_FILE.md` - .env 파일 생성 가이드
- `DOCKER_COMPOSE_GUIDE.md` - Docker Compose 사용 가이드

