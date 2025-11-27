# 프론트엔드 에러 가이드 - 화이트라벨 오류 (404 Not Found)

## 🔴 문제 상황

로그인 후 **Whitelabel Error Page (404 Not Found)** 오류가 발생하는 경우

---

## 📋 원인 분석

### 1. **잘못된 API 경로 호출**

가장 흔한 원인입니다. Gateway를 통해 요청할 때는 **반드시 `/api/auth/kakao/...` 경로**를 사용해야 합니다.

#### ❌ 잘못된 예시
```typescript
// 직접 authservice로 요청 (잘못됨)
fetch('http://localhost:8081/kakao/token', ...)

// Gateway 경로 없이 요청 (잘못됨)
fetch('http://localhost:8080/kakao/token', ...)
```

#### ✅ 올바른 예시
```typescript
// Gateway를 통한 올바른 경로
fetch('http://localhost:8080/api/auth/kakao/token', ...)
```

---

### 2. **카카오 콜백 처리 문제**

카카오 인증 후 콜백 URL이 잘못 설정되어 있거나, 프론트엔드에서 콜백을 제대로 처리하지 못하는 경우

#### 확인 사항
- 카카오 개발자 콘솔의 **Redirect URI**가 정확한가?
  - 올바른 URI: `http://localhost:8080/api/auth/kakao/callback`
  - ❌ 잘못된 URI: `http://localhost:8080/kakao/callback` (Gateway 경로 누락)

---

### 3. **Gateway 라우팅 문제**

Gateway가 요청을 올바르게 라우팅하지 못하는 경우

#### Gateway 라우팅 규칙
```
요청: /api/auth/kakao/token
  ↓ Gateway RewritePath 필터
실제: /kakao/token (authservice로 전달)
```

---

## ✅ 해결 방법

### 1. **API 엔드포인트 경로 확인**

모든 카카오 관련 API 호출은 다음 형식을 따라야 합니다:

```typescript
// ✅ 올바른 Base URL
const BASE_URL = 'http://localhost:8080/api/auth/kakao';

// 엔드포인트 목록
const ENDPOINTS = {
  authUrl: `${BASE_URL}/auth-url`,      // GET
  callback: `${BASE_URL}/callback`,     // GET (카카오에서 자동 호출)
  token: `${BASE_URL}/token`,           // POST
  user: `${BASE_URL}/user`,             // GET
  login: `${BASE_URL}/login`            // POST (레거시)
};
```

---

### 2. **카카오 로그인 플로우 수정**

#### 올바른 로그인 플로우

```typescript
// 1. 카카오 인증 URL 가져오기
const getAuthUrl = async () => {
  const response = await fetch('http://localhost:8080/api/auth/kakao/auth-url');
  const data = await response.json();
  
  if (data.success) {
    // 카카오 인가 페이지로 리다이렉트
    window.location.href = data.auth_url;
  } else {
    console.error('인증 URL 가져오기 실패:', data.message);
  }
};

// 2. 카카오 콜백 처리 (Next.js 예시)
// pages/kakao-callback.tsx 또는 pages/api/auth/kakao/callback.ts
useEffect(() => {
  const { code, error } = router.query;
  
  if (error) {
    console.error('카카오 인증 실패:', error);
    router.push('/login?error=kakao_auth_failed');
    return;
  }
  
  if (code && typeof code === 'string') {
    // 3. 인가 코드로 토큰 교환
    exchangeToken(code);
  }
}, [router.query]);

// 3. 토큰 교환
const exchangeToken = async (code: string) => {
  try {
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
      localStorage.setItem('user', JSON.stringify(data.user));
      
      // 대시보드로 이동
      router.push('/dashboard');
    } else {
      throw new Error(data.message);
    }
  } catch (err) {
    console.error('토큰 교환 실패:', err);
    router.push('/login?error=token_exchange_failed');
  }
};
```

---

### 3. **에러 처리 개선**

#### 404 에러 처리

```typescript
const handleApiError = (response: Response) => {
  if (response.status === 404) {
    console.error('404 Not Found - API 경로를 확인하세요');
    console.error('요청 URL:', response.url);
    throw new Error('API 엔드포인트를 찾을 수 없습니다. 경로를 확인하세요.');
  }
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
};

// 사용 예시
const fetchData = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/auth/kakao/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });
    
    handleApiError(response);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API 호출 실패:', error);
    // 사용자에게 친화적인 에러 메시지 표시
    alert('로그인 처리 중 오류가 발생했습니다. 다시 시도해주세요.');
  }
};
```

---

### 4. **디버깅 체크리스트**

문제가 발생하면 다음을 확인하세요:

- [ ] **API 경로 확인**: `/api/auth/kakao/...` 형식인가?
- [ ] **Gateway 실행 확인**: `docker ps | grep gateway`로 컨테이너 상태 확인
- [ ] **authservice 실행 확인**: `docker ps | grep authservice`로 컨테이너 상태 확인
- [ ] **브라우저 네트워크 탭**: 실제 요청 URL과 응답 상태 코드 확인
- [ ] **카카오 Redirect URI**: 개발자 콘솔에서 정확히 설정되었는지 확인
- [ ] **CORS 설정**: `http://localhost:3000` 또는 `http://127.0.0.1:3000`에서 요청하는가?

---

## 🔍 디버깅 방법

### 1. 브라우저 개발자 도구 확인

**Network 탭에서 확인:**
- 요청 URL이 정확한가? (`http://localhost:8080/api/auth/kakao/...`)
- 응답 상태 코드는 무엇인가? (404, 500, 등)
- 응답 본문에 에러 메시지가 있는가?

**Console 탭에서 확인:**
- JavaScript 에러가 있는가?
- API 호출 전후의 로그 메시지

### 2. Gateway 로그 확인

```bash
docker logs gateway -f
```

요청이 Gateway에 도달하는지 확인

### 3. authservice 로그 확인

```bash
docker logs authservice -f
```

요청이 authservice에 도달하는지 확인

---

## 📝 올바른 API 호출 예시

### 전체 로그인 플로우

```typescript
// hooks/useKakaoAuth.ts
import { useState } from 'react';
import { useRouter } from 'next/router';

const BASE_URL = 'http://localhost:8080/api/auth/kakao';

export const useKakaoAuth = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 1. 카카오 로그인 시작
  const startLogin = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${BASE_URL}/auth-url`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success && data.auth_url) {
        // 카카오 인가 페이지로 리다이렉트
        window.location.href = data.auth_url;
      } else {
        throw new Error(data.message || '인증 URL을 가져올 수 없습니다.');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '로그인 시작 실패';
      setError(errorMessage);
      console.error('카카오 로그인 시작 실패:', err);
    } finally {
      setLoading(false);
    }
  };

  // 2. 토큰 교환
  const exchangeToken = async (code: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${BASE_URL}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('API 엔드포인트를 찾을 수 없습니다. 경로를 확인하세요.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.success && data.access_token) {
        // 토큰 저장
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        if (data.user) {
          localStorage.setItem('user', JSON.stringify(data.user));
        }
        
        return data;
      } else {
        throw new Error(data.message || '토큰 교환 실패');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '토큰 교환 실패';
      setError(errorMessage);
      console.error('토큰 교환 실패:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    startLogin,
    exchangeToken,
    loading,
    error,
  };
};
```

---

## ⚠️ 주의사항

1. **절대 직접 authservice로 요청하지 마세요**
   - ❌ `http://localhost:8081/kakao/...`
   - ✅ `http://localhost:8080/api/auth/kakao/...`

2. **Gateway 경로를 반드시 포함하세요**
   - 모든 요청은 `/api/auth/kakao/...` 형식이어야 합니다.

3. **CORS 설정 확인**
   - 현재 허용된 Origin: `http://localhost:3000`, `http://127.0.0.1:3000`
   - 다른 포트를 사용하는 경우 백엔드에 요청 필요

4. **에러 처리 필수**
   - 모든 API 호출에 try-catch 추가
   - 사용자에게 친화적인 에러 메시지 표시

---

## 🆘 문제가 계속되면

1. **백엔드 개발자에게 문의**
   - Gateway 로그 공유
   - authservice 로그 공유
   - 요청 URL과 응답 상태 코드 공유

2. **체크리스트 확인**
   - 위의 디버깅 체크리스트 모두 확인

3. **환경 확인**
   - Docker 컨테이너가 모두 실행 중인지 확인
   - 네트워크 연결 확인

---

**문서 버전**: 1.0.0  
**최종 업데이트**: 2025-11-26

