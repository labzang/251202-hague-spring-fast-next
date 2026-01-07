/**
 * 메인 서비스 - 로그인 핸들러 함수들
 * 클로저 패턴을 사용하여 공통 설정을 외부 스코프에 유지하고 이너 함수로 핸들러를 정의
 */

// ============================================
// Types
// ============================================

interface LoginTokens {
    accessToken: string;
    refreshToken: string;
}

interface LoginSuccessResult {
    success: true;
    accessToken: string;
}

interface LoginErrorResult {
    success: false;
    error: string;
}

type LoginResult = LoginSuccessResult | LoginErrorResult;

const authService = (() => {
    // 외부 스코프 - 공통 설정 및 변수
    const baseUrl = 'api.labzang.com';
    const authPath = '/api/auth';
    const oauth2Path = '/oauth2';

    /**
     * 구글 로그인 핸들러 (이너 함수)
     * 백엔드 GET /api/auth/google/auth-url 엔드포인트로 연결
     * 백엔드 구조: 인증 URL 받기 → 구글 로그인 → 백엔드 콜백 처리 → 프론트엔드로 JWT 토큰 전달
     */
    async function handleGoogleLogin() {
        try {
            const googleLoginUrl = `${baseUrl}${authPath}/google/auth-url`;

            console.log("구글 로그인 요청 시작");
            console.log('구글 로그인 요청 URL:', googleLoginUrl);

            // POST 요청 (백엔드 @PostMapping("/auth-url")에 맞춤)
            const response = await fetch(googleLoginUrl, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });

            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(() => '');
                console.error('HTTP 에러:', response.status, response.statusText, errorText);
                alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
                return;
            }

            const data = await response.json();
            console.log('구글 인증 URL 응답:', data);

            if (data.success && data.auth_url) {
                // 구글 인가 페이지로 리다이렉트
                // 백엔드가 콜백 처리 후 프론트엔드 메인 페이지(/)로 JWT 토큰과 함께 리다이렉트
                window.location.href = data.auth_url;
            } else {
                const errorMessage = data.message || '알 수 없는 오류';
                console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
                alert('구글 로그인을 시작할 수 없습니다: ' + errorMessage);
            }
        } catch (error) {
            console.error("구글 로그인 실패:", error);

            // 네트워크 에러인 경우
            if (error instanceof TypeError && error.message.includes('fetch')) {
                alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
            } else {
                alert('구글 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
            }
        }
    }

    /**
     * 카카오 로그인 핸들러 (이너 함수)
     */
    async function handleKakaoLogin() {
        // 카카오 로그인 시작: 인증 URL 가져오기
        try {
            // 프론트엔드 콜백 URL을 파라미터로 전달
            const frontendCallbackUrl = `${window.location.origin}/kakao-callback`;
            const response = await fetch(`${baseUrl}${oauth2Path}/kakao/auth-url?redirect_uri=${encodeURIComponent(frontendCallbackUrl)}`);

            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(() => '');
                console.error('HTTP 에러:', response.status, response.statusText, errorText);
                alert(`서버 오류가 발생했습니다 (${response.status}). 백엔드 서버가 실행 중인지 확인해주세요.`);
                return;
            }

            const data = await response.json();
            console.log('API 응답:', data);

            if (data.success && data.auth_url) {
                // 카카오 인가 페이지로 리다이렉트
                window.location.href = data.auth_url;
            } else {
                const errorMessage = data.message || '알 수 없는 오류';
                console.error('인증 URL 가져오기 실패:', errorMessage, '전체 응답:', data);
                alert('카카오 로그인을 시작할 수 없습니다: ' + errorMessage);
            }
        } catch (error) {
            console.error("카카오 로그인 실패:", error);

            // 네트워크 에러인 경우
            if (error instanceof TypeError && error.message.includes('fetch')) {
                alert(`백엔드 서버(${baseUrl})에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.`);
            } else {
                alert('카카오 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
            }
        }
    }

    /**
     * 네이버 로그인 핸들러 (이너 함수)
     */
    function handleNaverLogin() {
        // 네이버 로그인 로직 추가
        console.log("네이버 로그인");
    }

    /**
     * Refresh Token을 HttpOnly 쿠키에 저장하는 함수
     * 
     * @param refreshToken - 저장할 refresh token
     * @returns Promise<boolean> - 성공 여부
     */
    async function setRefreshTokenCookie(refreshToken: string): Promise<boolean> {
        try {
            const response = await fetch('/api/auth/set-refresh-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refreshToken }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('[setRefreshTokenCookie] 쿠키 설정 실패:', response.status, errorData);
                return false;
            }

            const data = await response.json();
            console.log('[setRefreshTokenCookie] Refresh token이 HttpOnly 쿠키에 저장되었습니다.');
            return data.success === true;
        } catch (error) {
            console.error('[setRefreshTokenCookie] 에러:', error);
            return false;
        }
    }

    /**
     * Refresh Token 쿠키를 삭제하는 함수
     * 
     * @returns Promise<boolean> - 성공 여부
     */
    async function clearRefreshTokenCookie(): Promise<boolean> {
        try {
            const response = await fetch('/api/auth/set-refresh-token', {
                method: 'DELETE',
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('[clearRefreshTokenCookie] 쿠키 삭제 실패:', response.status, errorData);
                return false;
            }

            const data = await response.json();
            console.log('[clearRefreshTokenCookie] Refresh token 쿠키가 삭제되었습니다.');
            return data.success === true;
        } catch (error) {
            console.error('[clearRefreshTokenCookie] 에러:', error);
            return false;
        }
    }

    /**
     * 로그인 성공 후 토큰 처리 함수
     * - AccessToken: 반환 (호출 측에서 Zustand store에 저장)
     * - RefreshToken: HttpOnly 쿠키에 저장
     * 
     * @param tokens - accessToken과 refreshToken
     * @returns Promise<LoginResult> - 성공 시 accessToken 반환, 실패 시 에러 메시지
     */
    async function handleLoginSuccess(tokens: LoginTokens): Promise<LoginResult> {
        try {
            const { accessToken, refreshToken } = tokens;

            if (!accessToken || !refreshToken) {
                console.error('[handleLoginSuccess] 토큰이 누락되었습니다:', { accessToken: !!accessToken, refreshToken: !!refreshToken });
                return {
                    success: false,
                    error: '토큰이 누락되었습니다.',
                };
            }

            // RefreshToken을 HttpOnly 쿠키에 저장
            const cookieSuccess = await setRefreshTokenCookie(refreshToken);

            if (!cookieSuccess) {
                console.error('[handleLoginSuccess] Refresh token 쿠키 저장 실패');
                return {
                    success: false,
                    error: 'Refresh token 저장에 실패했습니다.',
                };
            }

            console.log('[handleLoginSuccess] 로그인 토큰 처리 완료');

            // AccessToken은 반환 (호출 측에서 Zustand store에 저장)
            return {
                success: true,
                accessToken,
            };
        } catch (error) {
            console.error('[handleLoginSuccess] 토큰 처리 중 에러:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '알 수 없는 오류',
            };
        }
    }

    /**
     * URL에서 토큰을 추출하는 함수 (OAuth 콜백 처리용)
     * 
     * @param url - 토큰이 포함된 URL (쿼리 파라미터 또는 해시)
     * @returns LoginTokens | null - 추출된 토큰 또는 null
     */
    function extractTokensFromUrl(url?: string): LoginTokens | null {
        try {
            const targetUrl = url || window.location.href;
            const urlObj = new URL(targetUrl);

            // 쿼리 파라미터에서 토큰 추출
            const accessToken = urlObj.searchParams.get('access_token') || urlObj.searchParams.get('accessToken');
            const refreshToken = urlObj.searchParams.get('refresh_token') || urlObj.searchParams.get('refreshToken');

            // 해시에서 토큰 추출 (fallback)
            if (!accessToken || !refreshToken) {
                const hash = urlObj.hash.substring(1); // '#' 제거
                const hashParams = new URLSearchParams(hash);
                const hashAccessToken = hashParams.get('access_token') || hashParams.get('accessToken');
                const hashRefreshToken = hashParams.get('refresh_token') || hashParams.get('refreshToken');

                if (hashAccessToken && hashRefreshToken) {
                    return {
                        accessToken: hashAccessToken,
                        refreshToken: hashRefreshToken,
                    };
                }
            }

            if (accessToken && refreshToken) {
                return {
                    accessToken,
                    refreshToken,
                };
            }

            return null;
        } catch (error) {
            console.error('[extractTokensFromUrl] URL 파싱 에러:', error);
            return null;
        }
    }

    /**
     * 로그아웃 처리 함수
     * - AccessToken: Zustand store에서 삭제 (호출 측에서 처리)
     * - RefreshToken: HttpOnly 쿠키에서 삭제
     * 
     * @returns Promise<boolean> - 성공 여부
     */
    async function handleLogout(): Promise<boolean> {
        try {
            // RefreshToken 쿠키 삭제
            const cookieSuccess = await clearRefreshTokenCookie();

            if (!cookieSuccess) {
                console.error('[handleLogout] Refresh token 쿠키 삭제 실패');
                return false;
            }

            // 백엔드 로그아웃 API 호출 (선택사항)
            try {
                await fetch(`${baseUrl}${authPath}/logout`, {
                    method: 'POST',
                    credentials: 'include', // 쿠키 포함
                });
            } catch (error) {
                console.warn('[handleLogout] 백엔드 로그아웃 API 호출 실패 (무시):', error);
            }

            console.log('[handleLogout] 로그아웃 완료');
            return true;
        } catch (error) {
            console.error('[handleLogout] 로그아웃 중 에러:', error);
            return false;
        }
    }

    // 클로저를 통해 이너 함수들을 반환
    return {
        handleGoogleLogin,
        handleKakaoLogin,
        handleNaverLogin,
        setRefreshTokenCookie,
        clearRefreshTokenCookie,
        handleLoginSuccess,
        extractTokensFromUrl,
        handleLogout,
    };
})();

// 개별 함수 export (기존 코드와의 호환성 유지)
export const {
    handleGoogleLogin,
    handleKakaoLogin,
    handleNaverLogin,
    setRefreshTokenCookie,
    clearRefreshTokenCookie,
    handleLoginSuccess,
    extractTokensFromUrl,
    handleLogout,
} = authService;

// 타입 export
export type { LoginTokens, LoginResult, LoginSuccessResult, LoginErrorResult };

