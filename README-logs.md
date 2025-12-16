# MLService 로그 관리 도구

MLService 컨테이너의 로그를 효율적으로 관리하고 디버깅하기 위한 스크립트 모음입니다.

## 📁 파일 목록

### 1. `view-mlservice-logs.ps1` (PowerShell)
**기본 로그 뷰어** - 실시간 로그 출력

```powershell
# 기본 사용 (최근 50줄 + 실시간)
.\view-mlservice-logs.ps1

# 최근 100줄부터 실시간 출력
.\view-mlservice-logs.ps1 -Lines 100

# 실시간 팔로우 없이 최근 로그만
.\view-mlservice-logs.ps1 -Lines 50 -Follow:$false
```

### 2. `view-mlservice-logs.sh` (Bash)
**Linux/Mac용 로그 뷰어**

```bash
# 실행 권한 부여 (Linux/Mac)
chmod +x view-mlservice-logs.sh

# 기본 사용
./view-mlservice-logs.sh

# 최근 100줄부터 출력
./view-mlservice-logs.sh 100

# 실시간 팔로우 없이
./view-mlservice-logs.sh 50 false
```

### 3. `mlservice-debug.ps1` (PowerShell)
**종합 디버깅 도구** - 메뉴 방식의 다기능 도구

```powershell
# 인터랙티브 메뉴 모드
.\mlservice-debug.ps1 menu

# 직접 명령 실행
.\mlservice-debug.ps1 status        # 컨테이너 상태 확인
.\mlservice-debug.ps1 logs 100      # 최근 100줄 로그
.\mlservice-debug.ps1 live          # 실시간 로그
.\mlservice-debug.ps1 restart       # 컨테이너 재시작
.\mlservice-debug.ps1 shell         # 컨테이너 셸 접속
```

## 🚀 빠른 시작

### Windows 사용자
```powershell
# 1. 실시간 로그 보기
.\view-mlservice-logs.ps1

# 2. 종합 디버깅 (추천)
.\mlservice-debug.ps1 menu
```

### Linux/Mac 사용자
```bash
# 1. 실행 권한 부여
chmod +x view-mlservice-logs.sh

# 2. 실시간 로그 보기
./view-mlservice-logs.sh
```

## 📋 주요 기능

### ✅ 컨테이너 상태 확인
- 실행 중인지 자동 감지
- 포트 및 이미지 정보 표시
- 상태에 따른 안내 메시지

### 📊 로그 출력 옵션
- **타임스탬프**: 각 로그 라인에 시간 정보
- **라인 수 조절**: 최근 N줄부터 출력
- **실시간 팔로우**: 새로운 로그 자동 업데이트
- **컬러 출력**: 가독성을 위한 색상 구분

### 🔧 디버깅 기능
- 컨테이너 재시작
- 셸 접속 (bash)
- 상태 모니터링
- 인터랙티브 메뉴

## 💡 사용 팁

### 로그 필터링
```powershell
# 에러 로그만 보기
docker logs mlservice 2>&1 | Select-String "ERROR"

# 특정 시간대 로그
docker logs mlservice --since "2024-12-11T14:00:00"

# 특정 키워드 검색
docker logs mlservice | Select-String "워드클라우드"
```

### 성능 모니터링
```powershell
# 컨테이너 리소스 사용량
docker stats mlservice --no-stream

# 컨테이너 정보 상세 보기
docker inspect mlservice
```

## 🚨 문제 해결

### 컨테이너가 실행되지 않는 경우
```powershell
# 컨테이너 시작
docker compose up mlservice -d

# 전체 서비스 시작
docker compose up -d
```

### 로그가 너무 많은 경우
```powershell
# 로그 파일 크기 제한 (docker-compose.yml에 추가)
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 한글 깨짐 문제
```powershell
# PowerShell 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📞 지원

문제가 발생하면 다음 정보와 함께 문의하세요:
1. 운영체제 (Windows/Linux/Mac)
2. Docker 버전: `docker --version`
3. 컨테이너 상태: `docker ps -a`
4. 에러 로그: `docker logs mlservice --tail 50`
