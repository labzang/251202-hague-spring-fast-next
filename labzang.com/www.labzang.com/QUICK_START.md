# 🚀 빠른 시작 가이드

## Next.js 개발 서버 실행

### 일반적인 경우 (권장)

```powershell
cd www.labzang.com

# 방법 1: 스크립트 사용 (자동으로 lock 파일 삭제 후 시작)
pnpm fix:dev

# 방법 2: 수동 실행
# 1. lock 파일만 삭제
pnpm clean:lock
# 2. 개발 서버 시작
pnpm dev
```

### 문제가 지속될 때 (완전 초기화)

```powershell
cd www.labzang.com

# .next 폴더 전체 삭제 후 시작
pnpm fix:dev:full
```

## 📋 실행 순서 (단계별)

### 1단계: 포트 확인 및 정리

```powershell
# 포트 3000 사용 중인 프로세스 확인
netstat -ano | findstr :3000

# 프로세스가 있으면 종료 (PID 확인 후)
taskkill /PID [PID번호] /F
```

### 2단계: Lock 파일만 삭제 (일반적인 경우)

```powershell
cd www.labzang.com
pnpm clean:lock
```

### 3단계: 개발 서버 실행

```powershell
pnpm dev
```

### 문제가 지속될 때만: .next 폴더 전체 삭제

```powershell
cd www.labzang.com
pnpm clean
pnpm dev
```

## 🔧 스크립트 설명

| 명령어 | 설명 |
|--------|------|
| `pnpm dev` | 개발 서버 시작 |
| `pnpm clean:lock` | Lock 파일만 삭제 (빠름) |
| `pnpm clean` | .next 폴더 전체 삭제 (완전 초기화) |
| `pnpm fix:dev` | Lock 파일 삭제 후 자동으로 dev 시작 |
| `pnpm fix:dev:full` | .next 폴더 전체 삭제 후 자동으로 dev 시작 |

## ⚡ 원클릭 해결

```powershell
# 일반적인 경우 (lock 파일만 삭제)
cd www.labzang.com
.\fix-dev-server.ps1

# 문제가 지속될 때 (.next 폴더 전체 삭제)
cd www.labzang.com
.\fix-dev-server.ps1 -Full
```

## 💡 팁

- **일반적인 경우**: `pnpm clean:lock` 또는 `pnpm fix:dev` 사용
- **문제가 지속될 때만**: `pnpm clean` 또는 `pnpm fix:dev:full` 사용
- 첫 실행 시 `.next` 폴더가 없으면 Next.js가 자동으로 생성합니다
- `pnpm fix:dev`는 lock 파일 삭제 후 자동으로 `pnpm dev`를 실행합니다

