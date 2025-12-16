# ModuleNotFoundError 해결 가이드

## 문제
```
ModuleNotFoundError: No module named 'app.config'
```

## 해결 방법

### 1. 경로 설정 수정 완료

`main.py`에서 Docker 환경과 로컬 환경을 모두 지원하도록 경로 설정을 수정했습니다:

- **Docker 환경**: `/app/app/main.py` → `/app`을 sys.path에 추가
- **로컬 환경**: `ai.labzang.com/mlservice/app/main.py` → `ai.labzang.com`을 sys.path에 추가

### 2. Fallback 처리 추가

config 모듈을 찾을 수 없는 경우 기본값을 사용하도록 fallback 처리를 추가했습니다.

### 3. 파일 확인

다음 파일들이 올바르게 복사되었는지 확인하세요:

- `/app/app/config.py` (Docker 컨테이너 내부)
- `ai.labzang.com/mlservice/app/config.py` (로컬)

## 추가 문제 해결

### 만약 여전히 에러가 발생한다면:

1. **Docker 이미지 재빌드**
   ```bash
   docker compose --profile ai build mlservice
   ```

2. **컨테이너 내부 확인**
   ```bash
   docker compose --profile ai run mlservice ls -la /app/app/
   ```
   
   다음 파일들이 있어야 합니다:
   - config.py
   - main.py
   - titanic/

3. **config.py 파일 확인**
   ```bash
   docker compose --profile ai run mlservice cat /app/app/config.py
   ```

## 현재 수정된 내용

1. ✅ 경로 설정 개선 (Docker/로컬 환경 모두 지원)
2. ✅ Fallback 처리 추가 (config 없을 때 기본값 사용)
3. ✅ 중복 import 제거

## 테스트 방법

1. Docker 이미지 재빌드
2. 컨테이너 실행
3. 로그 확인

```bash
docker compose --profile ai up mlservice
```

로그에서 "Could not import config" 경고가 나타나면 config.py 파일이 복사되지 않은 것입니다.

