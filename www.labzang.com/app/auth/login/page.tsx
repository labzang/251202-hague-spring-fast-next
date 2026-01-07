"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { handleGoogleLogin, handleKakaoLogin, handleNaverLogin } from "@/service/mainservice";

export default function LoginPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState<{
        google: boolean;
        kakao: boolean;
        naver: boolean;
    }>({
        google: false,
        kakao: false,
        naver: false,
    });

    

    const handleGoogleClick = async () => {
        setIsLoading((prev) => ({ ...prev, google: true }));
        try {
            await handleGoogleLogin();
        } finally {
            setIsLoading((prev) => ({ ...prev, google: false }));
        }
    };

    const handleKakaoClick = async () => {
        setIsLoading((prev) => ({ ...prev, kakao: true }));
        try {
            await handleKakaoLogin();
        } finally {
            setIsLoading((prev) => ({ ...prev, kakao: false }));
        }
    };

    const handleNaverClick = async () => {
        setIsLoading((prev) => ({ ...prev, naver: true }));
        try {
            await handleNaverLogin();
        } finally {
            setIsLoading((prev) => ({ ...prev, naver: false }));
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px] -z-10" />

            <div className="w-full max-w-md px-6 py-12">
                <div className="bg-white rounded-2xl shadow-xl p-8 space-y-8">
                    {/* Header */}
                    <div className="text-center space-y-2">
                        <h1 className="text-3xl font-bold text-gray-900">로그인</h1>
                        <p className="text-gray-600">소셜 계정으로 간편하게 로그인하세요</p>
                    </div>

                    {/* Social Login Buttons */}
                    <div className="space-y-4">
                        {/* Google Login */}
                        <Button
                            onClick={handleGoogleClick}
                            disabled={isLoading.google || isLoading.kakao || isLoading.naver}
                            className="w-full h-12 bg-white border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition-colors flex items-center justify-center gap-3"
                        >
                            {isLoading.google ? (
                                <div className="h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600" />
                            ) : (
                                <>
                                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                                        <path
                                            fill="#4285F4"
                                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                        />
                                        <path
                                            fill="#34A853"
                                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                        />
                                        <path
                                            fill="#FBBC05"
                                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                        />
                                        <path
                                            fill="#EA4335"
                                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                        />
                                    </svg>
                                    <span className="font-medium">구글로 로그인</span>
                                </>
                            )}
                        </Button>

                        {/* Kakao Login */}
                        <Button
                            onClick={handleKakaoClick}
                            disabled={isLoading.google || isLoading.kakao || isLoading.naver}
                            className="w-full h-12 bg-[#FEE500] border-2 border-[#FEE500] text-gray-900 hover:bg-[#FDD835] hover:border-[#FDD835] transition-colors flex items-center justify-center gap-3"
                        >
                            {isLoading.kakao ? (
                                <div className="h-5 w-5 animate-spin rounded-full border-2 border-gray-700 border-t-transparent" />
                            ) : (
                                <>
                                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M12 3c5.799 0 10.5 3.664 10.5 8.185 0 4.52-4.701 8.184-10.5 8.184a13.5 13.5 0 0 1-1.727-.11l-4.408 2.883c-.501.265-.678.236-.472-.413l.892-3.678c-2.88-1.46-4.785-3.99-4.785-6.866C1.5 6.665 6.201 3 12 3z" />
                                    </svg>
                                    <span className="font-medium">카카오로 로그인</span>
                                </>
                            )}
                        </Button>

                        {/* Naver Login */}
                        <Button
                            onClick={handleNaverClick}
                            disabled={isLoading.google || isLoading.kakao || isLoading.naver}
                            className="w-full h-12 bg-[#03C75A] border-2 border-[#03C75A] text-white hover:bg-[#02B350] hover:border-[#02B350] transition-colors flex items-center justify-center gap-3"
                        >
                            {isLoading.naver ? (
                                <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                            ) : (
                                <>
                                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                        <path d="M16.273 12.845L7.376 0H0v24h7.726V11.156L16.624 24H24V0h-7.727v12.845z" />
                                    </svg>
                                    <span className="font-medium">네이버로 로그인</span>
                                </>
                            )}
                        </Button>
                    </div>

                    {/* Footer */}
                    <div className="text-center text-sm text-gray-500 pt-4 border-t border-gray-200">
                        <p>로그인 시 서비스 이용약관 및 개인정보처리방침에 동의하게 됩니다.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

