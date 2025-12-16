'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

function KakaoCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('카카오 로그인 처리 중...');

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const error = searchParams.get('error');

      // 에러가 있는 경우
      if (error) {
        console.error('카카오 인증 실패:', error);
        setStatus('error');
        setMessage('카카오 인증에 실패했습니다.');
        setTimeout(() => {
          router.push('/?error=kakao_auth_failed');
        }, 2000);
        return;
      }

      // 인가 코드가 없는 경우
      if (!code) {
        console.error('인가 코드가 없습니다.');
        setStatus('error');
        setMessage('인가 코드를 받지 못했습니다.');
        setTimeout(() => {
          router.push('/?error=no_code');
        }, 2000);
        return;
      }

      // 토큰 교환
      try {
        const response = await fetch('http://localhost:8080/oauth2/kakao/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        });

        // HTTP 응답 상태 확인
        if (!response.ok) {
          const errorText = await response.text().catch(() => '');
          console.error('HTTP 에러:', response.status, response.statusText, errorText);
          throw new Error(`서버 오류 (${response.status}): ${errorText || response.statusText}`);
        }

        const data = await response.json();
        console.log('토큰 교환 응답:', data);

        if (data.success && data.access_token) {
          // 토큰 저장
          localStorage.setItem('access_token', data.access_token);
          if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
          }

          // 사용자 정보 저장
          if (data.user) {
            localStorage.setItem('user', JSON.stringify(data.user));
          }

          setStatus('success');
          setMessage('로그인 성공! 대시보드로 이동합니다...');

          // 대시보드로 리다이렉트
          setTimeout(() => {
            router.push('/dashboard');
          }, 1000);
        } else {
          throw new Error(data.message || '토큰 교환 실패');
        }
      } catch (err) {
        console.error('토큰 교환 실패:', err);
        setStatus('error');
        const errorMessage = err instanceof Error ? err.message : '토큰 교환에 실패했습니다.';
        setMessage(errorMessage);
        setTimeout(() => {
          router.push('/?error=token_exchange_failed');
        }, 2000);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-white font-sans">
      <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
        <div className="flex flex-col items-center gap-4">
          {status === 'loading' && (
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#FEE500] border-t-transparent"></div>
          )}
          {status === 'success' && (
            <div className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          )}
          {status === 'error' && (
            <div className="h-8 w-8 rounded-full bg-red-500 flex items-center justify-center">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          )}
          <p className="text-lg font-medium text-gray-900">{message}</p>
        </div>
      </main>
    </div>
  );
}

export default function KakaoCallback() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center bg-white font-sans">
        <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
          <div className="flex flex-col items-center gap-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#FEE500] border-t-transparent"></div>
            <p className="text-lg font-medium text-gray-900">카카오 로그인 처리 중...</p>
          </div>
        </main>
      </div>
    }>
      <KakaoCallbackContent />
    </Suspense>
  );
}

