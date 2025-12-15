# 개발 서버 실행 방법

## npm run dev 에러 해결

루트 디렉토리에서 실행하면 에러가 발생합니다.

### 올바른 실행 방법

```bash
# 루트 디렉토리에서
cd www.labzang.com
npm run dev
```

또는 한 줄로:

```bash
cd www.labzang.com && npm run dev
```

### 프로젝트 구조

```
labzang.com/                    ← 루트 디렉토리 (package.json 없음)
├── www.labzang.com/           ← Next.js 앱 (package.json 있음) ✓
├── admin.labzang.com/         ← Next.js 앱 (package.json 있음)
├── ai.labzang.com/            ← Python 서비스
└── api.labzang.com/           ← Java 서비스
```

각 서비스는 독립적인 디렉토리에 있으므로 해당 디렉토리로 이동해야 합니다.

