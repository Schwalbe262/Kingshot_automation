# runner.py
import subprocess
import threading
import time

RUNTIME = 8 * 60  # 8분(초)


def shutdown_bluestacks_processes(processes, reason="요청됨"):
    print(f"{reason}: BlueStacks 프로세스 종료 중...")
    # 1) Popen으로 띄운 프로세스 종료 시도
    for process in processes:
        if process is None:
            continue
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)
        except Exception as e:
            print(f"Popen 프로세스 종료 중 오류: {e}")

    # 2) Windows taskkill로 BlueStacks 관련 프로세스 강제 종료
    bluestacks_process_names = ["HD-Player.exe", "HD-Adb.exe", "BstkDrv.exe"]
    for proc_name in bluestacks_process_names:
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", proc_name],
                capture_output=True,
                timeout=10,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
    time.sleep(1)


def stream_output(process):
    if process.stdout is None:
        return
    for line in process.stdout:
        print("[automation.py]", line, end="")


while True:
    print("automation.py 시작")
    # stdout과 stderr를 실시간으로 받아서 터미널에 출력
    proc = subprocess.Popen(
        ["python", "-u", "automation.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        text=True,
        encoding="euc-kr",
        errors="replace",  # UTF-8이 아닌 바이트(CP949 등)가 나와도 크래시 방지
    )

    try:
        start_time = time.time()
        output_thread = threading.Thread(target=stream_output, args=(proc,), daemon=True)
        output_thread.start()

        while proc.poll() is None:
            if time.time() - start_time > RUNTIME:
                raise subprocess.TimeoutExpired(cmd="automation.py", timeout=RUNTIME)
            time.sleep(0.5)

        output_thread.join(timeout=2)
        shutdown_bluestacks_processes([proc], reason="automation.py 자체 종료 감지")
        print("automation.py가 자체 종료됨, 즉시 재시작")
    except subprocess.TimeoutExpired:
        print("10분 경과, automation.py 강제 종료 후 재시작")
        shutdown_bluestacks_processes([proc], reason="10분 타임아웃")