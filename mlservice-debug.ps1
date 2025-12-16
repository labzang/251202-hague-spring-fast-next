# mlservice 컨테이너 디버깅 및 로그 분석 PowerShell 스크립트
# 사용법: .\mlservice-debug.ps1

param(
    [string]$Action = "logs",  # logs, status, restart, shell
    [string]$Lines = "100"
)

function Show-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Cyan
}

function Show-ContainerStatus {
    Show-Header "컨테이너 상태 확인"
    
    $containers = docker ps -a --filter "name=mlservice" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"
    if ($containers) {
        Write-Host $containers
    } else {
        Write-Host "❌ mlservice 컨테이너를 찾을 수 없습니다." -ForegroundColor Red
    }
}

function Show-Logs {
    param([string]$LineCount)
    Show-Header "최근 로그 ($LineCount 줄)"
    
    $containerExists = docker ps -a --filter "name=mlservice" --format "{{.Names}}"
    if ($containerExists) {
        docker logs mlservice --tail $LineCount --timestamps
    } else {
        Write-Host "❌ mlservice 컨테이너가 존재하지 않습니다." -ForegroundColor Red
    }
}

function Show-LiveLogs {
    Show-Header "실시간 로그 (Ctrl+C로 종료)"
    Start-Sleep 1
    docker logs mlservice --tail 20 --follow --timestamps
}

function Restart-Container {
    Show-Header "컨테이너 재시작"
    
    Write-Host "mlservice 컨테이너를 재시작합니다..." -ForegroundColor Yellow
    docker compose restart mlservice
    
    Write-Host "재시작 완료. 상태 확인 중..." -ForegroundColor Green
    Start-Sleep 3
    Show-ContainerStatus
}

function Enter-Shell {
    Show-Header "컨테이너 셸 접속"
    
    $containerRunning = docker ps --filter "name=mlservice" --format "{{.Names}}"
    if ($containerRunning) {
        Write-Host "mlservice 컨테이너에 접속합니다. 'exit'로 나가세요." -ForegroundColor Green
        docker exec -it mlservice /bin/bash
    } else {
        Write-Host "❌ mlservice 컨테이너가 실행 중이지 않습니다." -ForegroundColor Red
    }
}

function Show-Menu {
    Show-Header "MLService 디버깅 도구"
    Write-Host "1. 컨테이너 상태 확인" -ForegroundColor White
    Write-Host "2. 최근 로그 보기 ($Lines 줄)" -ForegroundColor White
    Write-Host "3. 실시간 로그 보기" -ForegroundColor White
    Write-Host "4. 컨테이너 재시작" -ForegroundColor White
    Write-Host "5. 컨테이너 셸 접속" -ForegroundColor White
    Write-Host "6. 종료" -ForegroundColor White
    Write-Host ""
}

# 메인 실행 로직
switch ($Action.ToLower()) {
    "status" { Show-ContainerStatus }
    "logs" { Show-Logs $Lines }
    "live" { Show-LiveLogs }
    "restart" { Restart-Container }
    "shell" { Enter-Shell }
    "menu" {
        do {
            Show-Menu
            $choice = Read-Host "선택하세요 (1-6)"
            
            switch ($choice) {
                "1" { Show-ContainerStatus }
                "2" { Show-Logs $Lines }
                "3" { Show-LiveLogs }
                "4" { Restart-Container }
                "5" { Enter-Shell }
                "6" { 
                    Write-Host "종료합니다." -ForegroundColor Green
                    exit 0
                }
                default { 
                    Write-Host "잘못된 선택입니다. 1-6 중에서 선택하세요." -ForegroundColor Red 
                }
            }
            
            if ($choice -ne "6") {
                Write-Host ""
                Read-Host "계속하려면 Enter를 누르세요"
            }
        } while ($choice -ne "6")
    }
    default {
        Write-Host "사용법: .\mlservice-debug.ps1 [Action] [Lines]" -ForegroundColor Yellow
        Write-Host "Actions: status, logs, live, restart, shell, menu" -ForegroundColor White
        Write-Host "예시:" -ForegroundColor White
        Write-Host "  .\mlservice-debug.ps1 logs 50" -ForegroundColor Gray
        Write-Host "  .\mlservice-debug.ps1 live" -ForegroundColor Gray
        Write-Host "  .\mlservice-debug.ps1 menu" -ForegroundColor Gray
    }
}
