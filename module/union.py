import re
import time




def _enter_union_tap(adb, mod="None"):

    adb.tap(400, 920)  # 연맹 버튼 누르기
    time.sleep(2)

    if mod == "science":
        adb.tap(420, 700)  # 연맹 과학 기술 버튼 누르기
    else:
        pass

    time.sleep(1)


def union_research(adb):
    adb.tap(10, 415)
    time.sleep(1)
    adb.drag_with_adb(170, 625, 170, 275, duration_ms=800)
    time.sleep(1)
    adb.screen_shot(name="_union_research")

    result = adb.get_ocr_raw(
        file_name="capture_union_research.png",
        x_min=5,
        x_max=325,
        y_min=250,
        y_max=645,
        y_threshold=10,
        scale=3,
    )
    processed_result = adb.process_ocr(
        result=result,
        x_min=5,
        x_max=325,
        y_min=250,
        y_max=645,
        y_threshold=10,
        scale=3,
        merge=True,
    )

    target_avg = None  # 결과를 담을 변수

    for i in range(len(processed_result) - 1):
        curr_text = str(processed_result[i][0]).replace(" ", "")  # 현재 원소 text (공백 제거)
        next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

        if "기부" in curr_text and "가능" in next_text:
            curr_val = float(processed_result[i][2])  # 고급모집의 2번 인덱스
            next_val = float(processed_result[i + 1][2])  # 무료모집의 2번 인덱스
            target_avg = (curr_val + next_val) / 2.0
            adb.tap(300, target_avg)  # 연맹 기부 버튼 누르기
            time.sleep(1)
            
            # 연맹 버튼 누르기
            _enter_union_tap(adb, mod="science")

            break
        else:
            pass
    else:
        adb.tap(355, 415)
        return False

    time.sleep(1)
    adb.tap(510, 530)
    time.sleep(1)

    # green thumb 탐색
    result = adb.search_template(name="union_research")

    # 인식 된 경우
    if result != [] :
        adb.tap(result[0][1]+35, result[0][2]+35)
        time.sleep(1)
        
        # 기부 버튼 뜨는지 탐색
        adb.screen_shot(name="_union_done")
        result = adb.get_ocr_raw_advanced(file_name="capture_union_done.png", x_min=295, x_max=475, y_min=690, y_max=820, y_threshold=10, scale=3, binary_threshold=170)
        processed_result = adb.process_ocr(result=result, x_min=295, x_max=475, y_min=690, y_max=820, y_threshold=10, scale=3, merge=False)

        for item in processed_result:
            if "기부" in str(item[0]):
                x = item[1]
                y = item[2]
                for _ in range(10):
                    adb.tap(385, 765)  # 기부 버튼
                    time.sleep(0.5)
                adb.back()
                time.sleep(0.5)
                adb.back()
                time.sleep(0.5)
                adb.back()
                time.sleep(0.5)
                return True
        else:
            adb.back()
            time.sleep(0.5)
            adb.back()
            time.sleep(0.5)

    # 인식 안된 경우
    else :
        adb.back()
        time.sleep(0.5)
        adb.back()
        time.sleep(0.5)
        return False

