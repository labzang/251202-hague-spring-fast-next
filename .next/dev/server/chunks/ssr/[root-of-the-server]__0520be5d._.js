module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[project]/service/mainservice.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * 메인 서비스 - 로그인 핸들러 함수들
 * 클로저 패턴을 사용하여 공통 설정을 외부 스코프에 유지하고 이너 함수로 핸들러를 정의
 */ __turbopack_context__.s([
    "handleGoogleLogin",
    ()=>handleGoogleLogin,
    "handleKakaoLogin",
    ()=>handleKakaoLogin,
    "handleNaverLogin",
    ()=>handleNaverLogin
]);
const { handleGoogleLogin, handleKakaoLogin, handleNaverLogin } = (()=>{
    // 외부 스코프 - 공통 설정 및 변수
    const baseUrl = 'http://localhost:8080';
    const authPath = '/api/auth';
    const oauth2Path = '/oauth2';
    /**
     * 구글 로그인 핸들러 (이너 함수)
     * 백엔드 GET /api/auth/google/auth-url 엔드포인트로 연결
     * 백엔드 구조: 인증 URL 받기 → 구글 로그인 → 백엔드 콜백 처리 → 프론트엔드로 JWT 토큰 전달
     */ async function handleGoogleLogin() {
        try {
            const googleLoginUrl = `${baseUrl}${authPath}/google/auth-url`;
            console.log("구글 로그인 요청 시작");
            console.log('구글 로그인 요청 URL:', googleLoginUrl);
            // GET 요청 (백엔드 @GetMapping("/auth-url")에 맞춤)
            const response = await fetch(googleLoginUrl, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });
            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(()=>'');
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
     */ async function handleKakaoLogin() {
        // 카카오 로그인 시작: 인증 URL 가져오기
        try {
            // 프론트엔드 콜백 URL을 파라미터로 전달
            const frontendCallbackUrl = `${window.location.origin}/kakao-callback`;
            const response = await fetch(`${baseUrl}${oauth2Path}/kakao/auth-url?redirect_uri=${encodeURIComponent(frontendCallbackUrl)}`);
            // HTTP 응답 상태 확인
            if (!response.ok) {
                const errorText = await response.text().catch(()=>'');
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
     */ function handleNaverLogin() {
        // 네이버 로그인 로직 추가
        console.log("네이버 로그인");
    }
    // 클로저를 통해 이너 함수들을 반환
    return {
        handleGoogleLogin,
        handleKakaoLogin,
        handleNaverLogin
    };
})();
}),
"[project]/app/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$service$2f$mainservice$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/service/mainservice.ts [app-ssr] (ecmascript)");
'use client';
;
;
function Home() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex min-h-screen items-center justify-center bg-white font-sans",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
            className: "flex w-full max-w-md flex-col items-center gap-8 px-8 py-16",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                    className: "text-3xl font-bold text-gray-900",
                    children: "로그인"
                }, void 0, false, {
                    fileName: "[project]/app/page.tsx",
                    lineNumber: 11,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex w-full flex-col gap-4",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: __TURBOPACK__imported__module__$5b$project$5d2f$service$2f$mainservice$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["handleGoogleLogin"],
                            className: "flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                    className: "h-5 w-5",
                                    viewBox: "0 0 24 24",
                                    fill: "none",
                                    xmlns: "http://www.w3.org/2000/svg",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                            d: "M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z",
                                            fill: "#4285F4"
                                        }, void 0, false, {
                                            fileName: "[project]/app/page.tsx",
                                            lineNumber: 23,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                            d: "M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z",
                                            fill: "#34A853"
                                        }, void 0, false, {
                                            fileName: "[project]/app/page.tsx",
                                            lineNumber: 27,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                            d: "M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z",
                                            fill: "#FBBC05"
                                        }, void 0, false, {
                                            fileName: "[project]/app/page.tsx",
                                            lineNumber: 31,
                                            columnNumber: 15
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                            d: "M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z",
                                            fill: "#EA4335"
                                        }, void 0, false, {
                                            fileName: "[project]/app/page.tsx",
                                            lineNumber: 35,
                                            columnNumber: 15
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/app/page.tsx",
                                    lineNumber: 17,
                                    columnNumber: 13
                                }, this),
                                "구글 로그인"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/app/page.tsx",
                            lineNumber: 13,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: __TURBOPACK__imported__module__$5b$project$5d2f$service$2f$mainservice$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["handleKakaoLogin"],
                            className: "flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#FEE500] px-6 text-base font-medium text-gray-900 transition-colors hover:bg-[#FDD835] cursor-pointer",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                    className: "h-5 w-5",
                                    viewBox: "0 0 24 24",
                                    fill: "none",
                                    xmlns: "http://www.w3.org/2000/svg",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                        d: "M12 3C6.48 3 2 6.48 2 11c0 2.4 1.06 4.57 2.75 6.04L3 21l4.28-1.35C8.5 20.5 10.17 21 12 21c5.52 0 10-3.48 10-8s-4.48-10-10-10z",
                                        fill: "#000000"
                                    }, void 0, false, {
                                        fileName: "[project]/app/page.tsx",
                                        lineNumber: 52,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/app/page.tsx",
                                    lineNumber: 46,
                                    columnNumber: 13
                                }, this),
                                "카카오 로그인"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/app/page.tsx",
                            lineNumber: 42,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: __TURBOPACK__imported__module__$5b$project$5d2f$service$2f$mainservice$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["handleNaverLogin"],
                            className: "flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                    className: "h-5 w-5",
                                    viewBox: "0 0 24 24",
                                    fill: "none",
                                    xmlns: "http://www.w3.org/2000/svg",
                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                        d: "M16.273 12.845L7.376 0H0v24h7.726V11.156L16.624 24H24V0h-7.727v12.845z",
                                        fill: "#FFFFFF"
                                    }, void 0, false, {
                                        fileName: "[project]/app/page.tsx",
                                        lineNumber: 69,
                                        columnNumber: 15
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/app/page.tsx",
                                    lineNumber: 63,
                                    columnNumber: 13
                                }, this),
                                "네이버 로그인"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/app/page.tsx",
                            lineNumber: 59,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/app/page.tsx",
                    lineNumber: 12,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/page.tsx",
            lineNumber: 10,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/page.tsx",
        lineNumber: 9,
        columnNumber: 5
    }, this);
}
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    else {
        if ("TURBOPACK compile-time truthy", 1) {
            if ("TURBOPACK compile-time truthy", 1) {
                module.exports = __turbopack_context__.r("[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)");
            } else //TURBOPACK unreachable
            ;
        } else //TURBOPACK unreachable
        ;
    }
} //# sourceMappingURL=module.compiled.js.map
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].ReactJsxDevRuntime; //# sourceMappingURL=react-jsx-dev-runtime.js.map
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__0520be5d._.js.map