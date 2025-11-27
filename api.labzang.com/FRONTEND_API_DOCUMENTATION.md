# 카카오 로그인 API 문서

## 📋 목차
1. [개요](#개요)
2. [환경 설정](#환경-설정)
3. [인증 플로우](#인증-플로우)
4. [API 엔드포인트](#api-엔드포인트)
5. [에러 처리](#에러-처리)
6. [예제 코드](#예제-코드)

---

## 개요

이 문서는 카카오 OAuth 2.0 인증을 통한 로그인 시스템의 프론트엔드 연동 가이드입니다.

### 기본 정보
- **Base URL**: `http://localhost:8080/api/auth/kakao`
- **인증 방식**: OAuth 2.0 (Authorization Code Flow)
- **토큰 형식**: JWT (JSON Web Token)
- **CORS**: `http://localhost:3000`, `http://127.0.0.1:3000` 허용

---

## 환경 설정

### 필수 환경 변수
백엔드 서버의 `.env` 파일에 다음 환경 변수가 설정되어 있어야 합니다:

```env
KAKAO_REST_API_KEY=your-kakao-rest-api-key
KAKAO_REDIRECT_URI=http://localhost:8080/api/auth/kakao/callback
JWT_SECRET=your-secret-key-minimum-32-characters
JWT_EXPIRATION=86400000
```

### 카카오 개발자 콘솔 설정
1. [카카오 개발자 콘솔](https://developers.kakao.com/) 접속
2. 애플리케이션 등록
3. **Redirect URI** 설정: `http://localhost:8080/api/auth/kakao/callback`
4. **REST API 키** 복사하여 `.env` 파일에 설정

---

## 인증 플로우

```
[프론트엔드]                    [백엔드]                    [카카오]
     |                            |                          |
     |  1. GET /auth-url          |                          |
     |--------------------------->|                          |
     |                            |                          |
     |  2. authUrl 반환           |                          |
     |<---------------------------|                          |
     |                            |                          |
     |  3. 카카오 인가 페이지로 리다이렉트 |                          |
     |------------------------------------------------------>|
     |                            |                          |
     |                            |  4. 사용자 로그인 & 동의  |
     |                            |                          |
     |  5. 콜백으로 리다이렉트     |                          |
     |<------------------------------------------------------|
     |  (code 파라미터 포함)       |                          |
     |                            |                          |
     |  6. POST /token            |                          |
     |  { code: "..." }          |                          |
     |--------------------------->|                          |
     |                            |  7. 카카오 Access Token 요청 |
     |                            |------------------------->|
     |                            |                          |
     |                            |  8. 카카오 사용자 정보 요청 |
     |                            |------------------------->|
     |                            |                          |
     |                            |  9. JWT 토큰 생성         |
     |                            |                          |
     |  10. JWT 토큰 반환         |                          |
     |<---------------------------|                          |
     |                            |                          |
     |  11. 토큰 저장 & 인증 완료  |                          |
     |                            |                          |
```

---

## API 엔드포인트

### 1. 카카오 인증 URL 조회

카카오 로그인을 시작하기 위해 인증 URL을 가져옵니다.

**요청**
```http
GET /api/auth/kakao/auth-url
```

**응답 (성공)**
```json
{
  "success": true,
  "auth_url": "https://kauth.kakao.com/oauth/authorize?client_id=...&redirect_uri=...&response_type=code"
}
```

**응답 (실패)**
```json
{
  "success": false,
  "message": "카카오 REST API KEY가 설정되지 않았습니다."
}
```

**예제 코드**
```typescript
const getKakaoAuthUrl = async () => {
  const response = await fetch('http://localhost:8080/api/auth/kakao/auth-url');
  const data = await response.json();
  
  if (data.success) {
    // 카카오 인가 페이지로 리다이렉트
    window.location.href = data.auth_url;
  } else {
    console.error('인증 URL 가져오기 실패:', data.message);
  }
};
```

---

### 2. 카카오 콜백 처리

카카오 인증 후 리다이렉트되는 콜백 엔드포인트입니다.  
**⚠️ 주의**: 이 엔드포인트는 카카오에서 자동으로 호출되므로, 프론트엔드에서 직접 호출하지 않습니다.

**요청**
```http
GET /api/auth/kakao/callback?code={인가코드}
```

**응답 (성공)**
```json
{
  "success": true,
  "message": "카카오 인증이 성공적으로 처리되었습니다.",
  "code": "인가코드"
}
```

---

### 3. 카카오 토큰 교환 및 JWT 발급

인가 코드를 받은 후, 이를 JWT 토큰으로 교환합니다.

**요청**
```http
POST /api/auth/kakao/token
Content-Type: application/json

{
  "code": "인가코드"
}
```

**응답 (성공)**
```json
{
  "success": true,
  "message": "카카오 로그인이 성공적으로 처리되었습니다.",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "kakao_id": "123456789",
    "nickname": "홍길동",
    "email": "user@example.com",
    "email_verified": true,
    "profile_image": "https://k.kakaocdn.net/..."
  }
}
```

**응답 (실패)**
```json
{
  "success": false,
  "message": "Authorization Code가 필요합니다."
}
```

**예제 코드**
```typescript
const exchangeToken = async (code: string) => {
  const response = await fetch('http://localhost:8080/api/auth/kakao/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code }),
  });
  
  const data = await response.json();
  
  if (data.success) {
    // 토큰 저장
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    // 사용자 정보 저장
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  } else {
    throw new Error(data.message);
  }
};
```

---

### 4. 사용자 정보 조회

JWT 토큰을 사용하여 현재 로그인한 사용자 정보를 조회합니다.

**요청**
```http
GET /api/auth/kakao/user
Authorization: Bearer {access_token}
```

**응답 (성공)**
```json
{
  "success": true,
  "message": "카카오 사용자 정보를 성공적으로 조회했습니다.",
  "user": {
    "kakao_id": "123456789",
    "nickname": "홍길동",
    "email": "user@example.com",
    "email_verified": true,
    "profile_image": "https://k.kakaocdn.net/...",
    "provider": "kakao"
  }
}
```

**응답 (실패 - 인증 토큰 없음)**
```json
{
  "success": false,
  "message": "인증 토큰이 필요합니다."
}
```

**응답 (실패 - 유효하지 않은 토큰)**
```json
{
  "success": false,
  "message": "유효하지 않은 토큰입니다."
}
```

**예제 코드**
```typescript
const getUserInfo = async () => {
  const accessToken = localStorage.getItem('access_token');
  
  if (!accessToken) {
    throw new Error('토큰이 없습니다.');
  }
  
  const response = await fetch('http://localhost:8080/api/auth/kakao/user', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
  
  const data = await response.json();
  
  if (data.success) {
    return data.user;
  } else {
    throw new Error(data.message);
  }
};
```

---

### 5. 카카오 로그인 (레거시)

**⚠️ 주의**: 이 엔드포인트는 더미 응답을 반환합니다. 실제 인증을 위해서는 위의 플로우를 사용하세요.

**요청**
```http
POST /api/auth/kakao/login
Content-Type: application/json

{}
```

**응답**
```json
{
  "success": true,
  "message": "카카오 로그인이 성공적으로 처리되었습니다.",
  "token": "mock_token_1234567890"
}
```

---

## 에러 처리

### HTTP 상태 코드

| 상태 코드 | 의미 | 설명 |
|----------|------|------|
| 200 | OK | 요청 성공 |
| 400 | Bad Request | 잘못된 요청 (예: 필수 파라미터 누락) |
| 401 | Unauthorized | 인증 실패 (토큰 없음 또는 유효하지 않음) |
| 500 | Internal Server Error | 서버 내부 오류 |

### 에러 응답 형식

```json
{
  "success": false,
  "message": "에러 메시지",
  "error": "에러 코드 (선택적)",
  "error_description": "상세 에러 설명 (선택적)"
}
```

---

## 예제 코드

### React/Next.js 전체 플로우 예제

```typescript
// hooks/useKakaoAuth.ts
import { useState, useEffect } from 'react';

interface User {
  kakao_id: string;
  nickname: string;
  email: string;
  email_verified: boolean;
  profile_image: string;
  provider: string;
}

interface AuthResponse {
  success: boolean;
  access_token?: string;
  refresh_token?: string;
  user?: User;
  message?: string;
}

export const useKakaoAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 1. 카카오 인증 URL 가져오기
  const getAuthUrl = async (): Promise<string> => {
    try {
      const response = await fetch('http://localhost:8080/api/auth/kakao/auth-url');
      const data = await response.json();
      
      if (data.success) {
        return data.auth_url;
      } else {
        throw new Error(data.message);
      }
    } catch (err) {
      throw new Error('인증 URL을 가져오는데 실패했습니다.');
    }
  };

  // 2. 카카오 로그인 시작
  const startKakaoLogin = async () => {
    try {
      setLoading(true);
      const authUrl = await getAuthUrl();
      window.location.href = authUrl;
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인 실패');
      setLoading(false);
    }
  };

  // 3. 인가 코드로 토큰 교환
  const exchangeToken = async (code: string): Promise<AuthResponse> => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8080/api/auth/kakao/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      const data: AuthResponse = await response.json();

      if (data.success && data.access_token && data.user) {
        // 토큰 저장
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        
        // 사용자 정보 저장
        localStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        
        return data;
      } else {
        throw new Error(data.message || '토큰 교환 실패');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '토큰 교환 실패';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // 4. 사용자 정보 조회
  const fetchUserInfo = async (): Promise<User> => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      if (!accessToken) {
        throw new Error('토큰이 없습니다.');
      }

      const response = await fetch('http://localhost:8080/api/auth/kakao/user', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });

      const data = await response.json();

      if (data.success && data.user) {
        setUser(data.user);
        return data.user;
      } else {
        throw new Error(data.message || '사용자 정보 조회 실패');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '사용자 정보 조회 실패';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  // 5. 로그아웃
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  // 6. 초기 로드 시 사용자 정보 확인
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (err) {
        console.error('사용자 정보 파싱 실패:', err);
      }
    }
  }, []);

  return {
    user,
    loading,
    error,
    startKakaoLogin,
    exchangeToken,
    fetchUserInfo,
    logout,
  };
};
```

```typescript
// pages/kakao-callback.tsx (Next.js)
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useKakaoAuth } from '../hooks/useKakaoAuth';

export default function KakaoCallback() {
  const router = useRouter();
  const { exchangeToken } = useKakaoAuth();

  useEffect(() => {
    const handleCallback = async () => {
      const { code, error } = router.query;

      if (error) {
        console.error('카카오 인증 실패:', error);
        router.push('/login?error=kakao_auth_failed');
        return;
      }

      if (code && typeof code === 'string') {
        try {
          await exchangeToken(code);
          router.push('/dashboard');
        } catch (err) {
          console.error('토큰 교환 실패:', err);
          router.push('/login?error=token_exchange_failed');
        }
      }
    };

    if (router.isReady) {
      handleCallback();
    }
  }, [router.isReady, router.query, exchangeToken]);

  return (
    <div>
      <p>카카오 로그인 처리 중...</p>
    </div>
  );
}
```

```typescript
// components/LoginButton.tsx
import { useKakaoAuth } from '../hooks/useKakaoAuth';

export default function LoginButton() {
  const { startKakaoLogin, loading } = useKakaoAuth();

  return (
    <button
      onClick={startKakaoLogin}
      disabled={loading}
      className="kakao-login-button"
    >
      {loading ? '처리 중...' : '카카오로 로그인'}
    </button>
  );
}
```

---

## 토큰 관리

### Access Token
- **용도**: API 요청 시 인증
- **만료 시간**: 1시간 (3600초)
- **저장 위치**: `localStorage` 또는 `sessionStorage`
- **사용 방법**: `Authorization: Bearer {access_token}` 헤더에 포함

### Refresh Token
- **용도**: Access Token 갱신 (현재 미구현)
- **만료 시간**: 30일 (2592000초)
- **저장 위치**: `localStorage` 또는 `httpOnly` 쿠키 (권장)

### 토큰 저장 권장사항
```typescript
// 보안을 위해 httpOnly 쿠키 사용 권장
// 또는 localStorage 대신 sessionStorage 사용 고려

// localStorage (간단하지만 XSS 취약)
localStorage.setItem('access_token', token);

// sessionStorage (탭 종료 시 자동 삭제)
sessionStorage.setItem('access_token', token);

// httpOnly 쿠키 (가장 안전, 서버에서 설정)
// 프론트엔드에서 직접 설정 불가, 백엔드에서 Set-Cookie 헤더로 설정 필요
```

---

## 주의사항

1. **CORS 설정**: 현재 `http://localhost:3000`과 `http://127.0.0.1:3000`만 허용되어 있습니다. 다른 포트를 사용하는 경우 백엔드 설정을 변경해야 합니다.

2. **환경 변수**: 프로덕션 환경에서는 환경 변수를 안전하게 관리하세요.

3. **토큰 보안**: 
   - Access Token은 클라이언트에 저장되므로 XSS 공격에 취약합니다.
   - 가능하면 `httpOnly` 쿠키를 사용하거나, 최소한 `sessionStorage`를 사용하세요.
   - HTTPS를 사용하여 전송 중 암호화를 보장하세요.

4. **에러 처리**: 모든 API 호출에 대해 적절한 에러 처리를 구현하세요.

5. **로딩 상태**: 사용자 경험을 위해 로딩 상태를 표시하세요.

---

## 문의 및 지원

문제가 발생하거나 질문이 있으시면 백엔드 개발팀에 문의하세요.

---

**문서 버전**: 1.0.0  
**최종 업데이트**: 2025-11-26

