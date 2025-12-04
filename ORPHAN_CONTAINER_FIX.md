# Orphan Container 경고 해결

## 🔍 문제

```
Found orphan containers ([redis]) for this project. 
If you removed or renamed this service in your compose file, 
you can run this command with the --remove-orphans flag to clean it up.
```

## 📋 원인

- `docker-compose.yaml`에서 `redis` 서비스를 제거했지만
- 이전에 실행된 `redis` 컨테이너가 남아있었음
- Docker Compose가 이 컨테이너를 "orphan"으로 인식

## ✅ 해결 방법

### 방법 1: --remove-orphans 플래그 사용 (권장)
```powershell
docker compose down --remove-orphans
docker compose up
```

### 방법 2: 수동으로 orphan 컨테이너 제거
```powershell
# 모든 컨테이너 중지 및 제거
docker compose down

# 특정 orphan 컨테이너 제거
docker rm -f redis
```

## 🎯 해결 완료

다음 명령어로 정리 완료:
```powershell
docker compose down --remove-orphans
```

**결과:**
- ✅ redis 컨테이너 제거됨
- ✅ gateway, oauthservice, userservice 컨테이너 제거됨
- ✅ labzang-network 네트워크 제거됨

## 💡 앞으로 사용법

### Orphan 경고 없이 실행
```powershell
# 방법 1: down 시 orphan 제거
docker compose down --remove-orphans
docker compose up

# 방법 2: up 시 orphan 제거 (Docker Compose v2.20+)
docker compose up --remove-orphans
```

### 정상 실행
```powershell
# 이제 경고 없이 실행됩니다
docker compose up
```

## 📝 참고

- **Orphan Container**: docker-compose.yaml에 정의되지 않았지만 이전에 실행된 컨테이너
- **--remove-orphans**: 이러한 orphan 컨테이너를 자동으로 제거하는 플래그
- **Upstash Redis 사용**: 로컬 redis 컨테이너는 더 이상 필요 없음

