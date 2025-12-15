This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## 🚀 빠른 시작

### 1. pnpm 설치 (아직 설치하지 않은 경우)

```bash
npm install -g pnpm
```

### 2. 의존성 설치

```bash
pnpm install
```

### 3. 개발 서버 실행

**일반적인 경우 (권장):**
```bash
# 방법 1: 자동 정리 후 시작 (lock 파일만 삭제)
pnpm fix:dev

# 방법 2: 수동 실행
pnpm clean:lock  # lock 파일만 삭제
pnpm dev         # 개발 서버 시작
```

**문제가 지속될 때만 (.next 폴더 전체 삭제):**
```bash
pnpm fix:dev:full
```

### 4. 브라우저에서 확인

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## 📋 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `pnpm dev` | 개발 서버 시작 |
| `pnpm build` | 프로덕션 빌드 |
| `pnpm start` | 프로덕션 서버 실행 |
| `pnpm clean:lock` | Lock 파일만 삭제 (빠름) |
| `pnpm clean` | .next 폴더 전체 삭제 |
| `pnpm fix:dev` | Lock 파일 삭제 후 자동으로 dev 시작 |
| `pnpm fix:dev:full` | .next 폴더 전체 삭제 후 자동으로 dev 시작 |

## 🔧 문제 해결

개발 서버가 시작되지 않을 때:

1. **일반적인 경우**: `pnpm fix:dev` 실행 (lock 파일만 삭제)
2. **문제가 지속될 때**: `pnpm fix:dev:full` 실행 (.next 폴더 전체 삭제)

자세한 내용은 [QUICK_START.md](./QUICK_START.md) 또는 [FIX_DEV_SERVER_LOCK.md](./FIX_DEV_SERVER_LOCK.md)를 참고하세요.

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
