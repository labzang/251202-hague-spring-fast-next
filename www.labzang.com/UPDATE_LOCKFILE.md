# pnpm-lock.yaml 업데이트 가이드

## 문제
Vercel 배포 시 `pnpm-lock.yaml`이 `package.json`과 동기화되지 않아 발생하는 에러입니다.

## 해결 방법

### 방법 1: 로컬에서 lockfile 업데이트 (권장)

로컬에서 다음 명령어를 실행하여 lockfile을 업데이트하고 커밋하세요:

```bash
cd www.labzang.com
pnpm install
git add pnpm-lock.yaml
git commit -m "chore: update pnpm-lock.yaml"
git push
```

### 방법 2: Vercel 빌드 설정 사용 (임시 해결책)

`vercel.json` 파일이 생성되었습니다. 이 파일은 Vercel이 `--no-frozen-lockfile` 옵션을 사용하여 설치하도록 설정합니다.

하지만 **권장 방법은 방법 1**입니다. lockfile을 업데이트하여 커밋하는 것이 더 안정적입니다.

## 참고

- `vercel.json`의 `installCommand`는 Vercel 빌드 시 사용됩니다.
- 로컬에서 lockfile을 업데이트하면 향후 배포가 더 안정적입니다.

