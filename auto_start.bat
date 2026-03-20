@echo off
REM 1) 프로젝트 폴더로 이동
cd /d "%USERPROFILE%\Documents\GitHub\Kingshot_automation"

REM 2) conda 환경 활성화
call "C:\ProgramData\anaconda3\Scripts\activate.bat" mafia2024

REM 3) run.py 실행
python run.py