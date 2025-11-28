'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  nickname: string;
  email?: string;
  provider: string;
}

export default function Dashboard() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // 저장된 사용자 정보 불러오기
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (err) {
                console.error('사용자 정보 파싱 실패:', err);
            }
        } else {
            // 토큰이 있으면 사용자 정보 조회
            const accessToken = localStorage.getItem('access_token');
            if (accessToken) {
                fetchUserInfo(accessToken);
            } else {
                // 토큰이 없으면 로그인 페이지로 리다이렉트
                router.push('/');
            }
        }
        setLoading(false);
    }, [router]);

    const fetchUserInfo = async (accessToken: string) => {
        try {
            const response = await fetch('http://localhost:8080/api/auth/google/user', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            const data = await response.json();

            if (data.success && data.user) {
                setUser(data.user);
                localStorage.setItem('user', JSON.stringify(data.user));
            } else {
                throw new Error(data.message || '사용자 정보 조회 실패');
            }
        } catch (err) {
            console.error('사용자 정보 조회 실패:', err);
            // 토큰이 유효하지 않으면 로그인 페이지로 리다이렉트
            router.push('/');
        }
    };

    const handleLogout = () => {
        // 토큰 및 사용자 정보 삭제
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        // 로그인 페이지로 리다이렉트
        router.push('/');
    };

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-white font-sans">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-white font-sans">
                <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
                    <p className="text-lg text-gray-600">사용자 정보를 불러올 수 없습니다.</p>
                    <button
                        onClick={handleLogout}
                        className="flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
                    >
                        로그인 페이지로 돌아가기
                    </button>
                </main>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-white font-sans">
            <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
                <h1 className="text-4xl font-bold text-gray-900 text-center">
                    구글 로그인 성공
                </h1>
                
                <div className="flex w-full flex-col gap-2 text-center">
                    <p className="text-xl font-semibold text-gray-900">{user.nickname || user.id}</p>
                    {user.email && (
                        <p className="text-sm text-gray-600">{user.email}</p>
                    )}
                    <p className="text-xs text-gray-500">구글 ID: {user.id}</p>
                </div>

                <button
                    onClick={handleLogout}
                    className="flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
                >
                    로그아웃
                </button>
            </main>
        </div>
    );
}

