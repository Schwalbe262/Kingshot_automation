import time


def get_people(adb):

    # people 템플릿 유무 확인
    result = adb.search_template(name="people")

    # 템플릿 일치 시
    if result != [] :
        # 해당 버튼 클릭릭
        adb.tap(result[0][1], result[0][2])
        time.sleep(1)

        # 스크린샷 찍어 "환영하기" 문구 확인
        adb.screen_shot(name="_people")
        result = adb.get_ocr_raw(file_name="capture_people.png", x_min=210, x_max=330, y_min=820, y_max=860, y_threshold=10, scale=1)
        processed_result = adb.process_ocr(result=result, x_min=210, x_max=330, y_min=820, y_max=860, y_threshold=10, scale=1, merge=True)

        # "환영하기" 문구 포함 시
        if any("환영" in str(item[0]) for item in processed_result if len(item) > 0) :
            # "환영하기" 버튼 클릭
            adb.tap(270, 840)
            time.sleep(5)
            return True
        else :
            return False
    else :
        return False
