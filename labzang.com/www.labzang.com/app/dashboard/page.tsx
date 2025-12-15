'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface UserInfo {
    email?: string;
    name?: string;
    provider?: string;
}

export default function Dashboard() {
    const router = useRouter();
    const [user, setUser] = useState<UserInfo | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // 토큰 확인
        const token = localStorage.getItem('access_token');

        if (!token) {
            // 토큰이 없으면 로그인 페이지로 리다이렉트
            router.push('/');
            return;
        }

        // 사용자 정보 가져오기
        const userString = localStorage.getItem('user');
        if (userString) {
            try {
                const userData = JSON.parse(userString);
                setUser(userData);
            } catch (error) {
                console.error('사용자 정보 파싱 실패:', error);
            }
        }

        setIsLoading(false);
    }, [router]);

    const handleLogout = () => {
        // 로컬 스토리지에서 토큰 제거
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');

        // 로그인 페이지로 리다이렉트
        router.push('/');
    };

    if (isLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
                <div className="h-12 w-12 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent"></div>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 font-sans">
            <main className="flex w-full max-w-2xl flex-col items-center gap-8 rounded-2xl bg-white p-12 shadow-2xl">
                {/* 환영 메시지 */}
                <div className="flex flex-col items-center gap-4 text-center">
                    <div className="flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-green-400 to-green-600 shadow-lg">
                        <svg
                            className="h-10 w-10 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M5 13l4 4L19 7"
                            />
                        </svg>
                    </div>

                    <h1 className="text-4xl font-bold text-gray-900">
                        Welcome! 🎉
                    </h1>

                    <p className="text-lg text-gray-600">
                        로그인에 성공했습니다
                    </p>
                </div>

                {/* 사용자 정보 */}
                {user && (
                    <div className="w-full rounded-xl bg-gradient-to-r from-indigo-50 to-blue-50 p-6">
                        <h2 className="mb-4 text-xl font-semibold text-gray-900">
                            사용자 정보
                        </h2>
                        <div className="space-y-3">
                            {user.name && (
                                <div className="flex items-center gap-3">
                                    <span className="text-sm font-medium text-gray-600 w-20">이름:</span>
                                    <span className="text-base text-gray-900">{user.name}</span>
                                </div>
                            )}
                            {user.email && (
                                <div className="flex items-center gap-3">
                                    <span className="text-sm font-medium text-gray-600 w-20">이메일:</span>
                                    <span className="text-base text-gray-900">{user.email}</span>
                                </div>
                            )}
                            {user.provider && (
                                <div className="flex items-center gap-3">
                                    <span className="text-sm font-medium text-gray-600 w-20">제공자:</span>
                                    <span className="text-base capitalize text-gray-900">{user.provider}</span>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* 액션 버튼 */}
                <div className="flex w-full flex-col gap-3 sm:flex-row">
                    <button
                        onClick={() => router.push('/dashboard/profile')}
                        className="flex-1 rounded-lg bg-indigo-600 px-6 py-3 text-base font-medium text-white transition-colors hover:bg-indigo-700"
                    >
                        프로필 보기
                    </button>
                    <button
                        onClick={handleLogout}
                        className="flex-1 rounded-lg border-2 border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
                    >
                        로그아웃
                    </button>
                </div>

                {/* 추가 정보 */}
                <div className="mt-4 text-center text-sm text-gray-500">
                    <p>안전하게 로그인되었습니다</p>
                    <p className="mt-1">JWT 토큰이 저장되어 있습니다</p>
                </div>
            </main>
        </div>
    );
}

