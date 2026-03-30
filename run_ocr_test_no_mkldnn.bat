@echo off
REM oneDNN 끄고 OCR_test 노트북만 실행 (Paddle fused_conv2d 에러 회피)
set FLAGS_use_mkldnn=0
set FLAGS_use_dnnl=0
cd /d "%~dp0"
jupyter notebook OCR_test.ipynb
pause
