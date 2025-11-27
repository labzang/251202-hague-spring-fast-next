'use client';

export default function Home() {
  const handleGoogleLogin = () => {
    // 구글 로그인 로직 추가
    console.log("구글 로그인");
  };

  const handleKakaoLogin = async () => {
    // 카카오 로그인 시작: 인증 URL 가져오기
    try {
      // 프론트엔드 콜백 URL을 파라미터로 전달
      const frontendCallbackUrl = `${window.location.origin}/kakao-callback`;
      const response = await fetch(`http://localhost:8080/oauth2/kakao/auth-url?redirect_uri=${encodeURIComponent(frontendCallbackUrl)}`);

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
        alert('백엔드 서버(localhost:8080)에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.');
      } else {
        alert('카카오 로그인 중 오류가 발생했습니다: ' + (error instanceof Error ? error.message : String(error)));
      }
    }
  };

  const handleNaverLogin = () => {
    // 네이버 로그인 로직 추가
    console.log("네이버 로그인");
  };


  return (
    <div className="flex min-h-screen items-center justify-center bg-white font-sans">
      <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
        <h1 className="text-3xl font-bold text-gray-900">로그인</h1>
        <div className="flex w-full flex-col gap-4">
          <button
            onClick={handleGoogleLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            구글 로그인
          </button>
          <button
            onClick={handleKakaoLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#FEE500] px-6 text-base font-medium text-gray-900 transition-colors hover:bg-[#FDD835] cursor-pointer"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 3C6.48 3 2 6.48 2 11c0 2.4 1.06 4.57 2.75 6.04L3 21l4.28-1.35C8.5 20.5 10.17 21 12 21c5.52 0 10-3.48 10-8s-4.48-10-10-10z"
                fill="#000000"
              />
            </svg>
            카카오 로그인
          </button>
          <button
            onClick={handleNaverLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16.273 12.845L7.376 0H0v24h7.726V11.156L16.624 24H24V0h-7.727v12.845z"
                fill="#FFFFFF"
              />
            </svg>
            네이버 로그인
          </button>
        </div>
      </main>
    </div>
  );
}
