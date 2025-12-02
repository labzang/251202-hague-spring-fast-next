module.exports = [
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/@opentelemetry/api [external] (next/dist/compiled/@opentelemetry/api, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/@opentelemetry/api", () => require("next/dist/compiled/@opentelemetry/api"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/after-task-async-storage.external.js [external] (next/dist/server/app-render/after-task-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/after-task-async-storage.external.js", () => require("next/dist/server/app-render/after-task-async-storage.external.js"));

module.exports = mod;
}),
"[project]/app/api/auth/kakao/login/route.ts [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "POST",
    ()=>POST
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/server.js [app-route] (ecmascript)");
;
async function POST(request) {
    // 가능한 백엔드 경로들 (우선순위 순)
    // 백엔드 컨트롤러의 @RequestMapping과 @PostMapping 조합에 따라 경로가 달라집니다
    const possiblePaths = [
        '/api/auth/kakao/login',
        '/auth/kakao/login',
        '/api/kakao/login',
        '/kakao/login',
        '/login'
    ];
    const baseUrl = 'http://localhost:8080';
    try {
        // 요청 본문 가져오기
        const body = await request.json().catch(()=>({}));
        let lastError = null;
        // 여러 경로를 시도
        for (const path of possiblePaths){
            const backendUrl = `${baseUrl}${path}`;
            try {
                console.log(`[API 프록시] 시도 중: ${backendUrl}`);
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(body)
                });
                console.log(`[API 프록시] 응답 상태: ${response.status} ${response.statusText} (${backendUrl})`);
                if (response.ok) {
                    const data = await response.json();
                    console.log(`[API 프록시] 성공: ${backendUrl}`);
                    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json(data);
                } else if (response.status !== 404) {
                    // 404가 아닌 다른 에러는 즉시 반환
                    const errorText = await response.text().catch(()=>'');
                    console.error(`[API 프록시] 에러 (${response.status}): ${errorText}`);
                    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
                        error: `HTTP ${response.status}: ${errorText || response.statusText}`,
                        path: backendUrl
                    }, {
                        status: response.status
                    });
                }
                // 404인 경우 다음 경로 시도
                lastError = new Error(`404 Not Found: ${backendUrl}`);
            } catch (fetchError) {
                console.error(`[API 프록시] fetch 에러 (${backendUrl}):`, fetchError);
                lastError = fetchError instanceof Error ? fetchError : new Error(String(fetchError));
                // 네트워크 에러가 아닌 경우 계속 시도
                if (fetchError instanceof TypeError && fetchError.message.includes('fetch')) {
                    // 네트워크 에러는 모든 경로에서 실패할 것이므로 즉시 반환
                    return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
                        error: '서버에 연결할 수 없습니다. 백엔드 서버(localhost:8080)가 실행 중인지 확인해주세요.',
                        attemptedPath: backendUrl
                    }, {
                        status: 500
                    });
                }
            }
        }
        // 모든 경로가 실패한 경우
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
            error: '엔드포인트를 찾을 수 없습니다. 다음 경로들을 시도했습니다:',
            attemptedPaths: possiblePaths.map((p)=>`${baseUrl}${p}`),
            suggestion: '백엔드 서버의 실제 엔드포인트 경로를 확인해주세요.'
        }, {
            status: 404
        });
    } catch (error) {
        console.error('[API 프록시] 예상치 못한 에러:', error);
        return __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$server$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["NextResponse"].json({
            error: '서버 오류가 발생했습니다.',
            details: error instanceof Error ? error.message : String(error)
        }, {
            status: 500
        });
    }
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__b7fe0206._.js.map