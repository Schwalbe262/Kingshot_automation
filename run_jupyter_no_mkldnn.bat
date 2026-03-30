@echo off
REM oneDNN 끄고 Jupyter 실행 (Paddle OCR fused_conv2d 에러 회피)
set FLAGS_use_mkldnn=0
set FLAGS_use_dnnl=0
jupyter notebook
pause
