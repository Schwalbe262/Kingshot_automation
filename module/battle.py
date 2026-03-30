import os
import time

import cv2
import numpy as np


def heal(adb) :

    # state 기록록
    adb.runtime_write("state", "heal")


    # 힐 아이콘 인식
    adb.screen_shot(name="_heal")

    img_path = f"{adb.base}\\{adb._f('capture_heal.png')}"
    img = cv2.imread(img_path)
    img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_e = cv2.Canny(img_g, 80, 160)

    template_dir = os.path.join(os.getcwd(), "template")
    threshold = 0.55

    def detect_template(name):
        detections = []  # (template_name, cx, cy, score)
        tpl_path = os.path.join(template_dir, name)
        tpl = cv2.imread(tpl_path)
        if tpl is None:
            print(f"[WARN] 템플릿 로드 실패: {tpl_path}")
            return detections

        tpl_g = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
        tpl_e = cv2.Canny(tpl_g, 80, 160)

        res = cv2.matchTemplate(img_e, tpl_e, cv2.TM_CCOEFF_NORMED)
        ys, xs = np.where(res >= threshold)

        w, h = tpl.shape[1], tpl.shape[0]
        for x, y in zip(xs, ys):
            cx = x + w // 2
            cy = y + h // 2
            score = float(res[y, x])
            detections.append((name, cx, cy, score))

        detections.sort(key=lambda x: x[3], reverse=True)
        return detections

    # 현재 이미 heal을 하고있는지 인식
    detections2 = detect_template("heal_template2.png")
    detections3 = detect_template("heal_template3.png")

    detections = []
    # detect_template이 2D list 형태라 extend
    detections.extend(detections2)
    detections.extend(detections3)

    # 여기에 걸릴 경우 이미 heal을 하는 중이므로 return
    if detections != []:
        return 10

    # heal 버튼이 있는지 감지
    detections = detect_template("heal_template1.png")

    # 아무것도 없을 경우
    if detections == [] : 
        time.sleep(1)
        return False
    # 힐 버튼 아이콘 클릭
    else :
        adb.tap(detections[0][1], detections[0][2])
        time.sleep(1)


    # 힐 버튼 클릭 후 치료 버튼이 잘 뜨는지 인식
    adb.screen_shot(name="_heal")

    result = adb.get_ocr_raw(file_name="capture_heal.png", x_min=365, x_max=415, y_min=670, y_max=705, y_threshold=10, scale=3)
    processed_result = adb.process_ocr(result=result, x_min=365, x_max=415, y_min=670, y_max=705, y_threshold=10, scale=3, merge=True)

    has_heal = any("치료" in str(item[0]) for item in processed_result)
    
    # 힐 버튼 인식 됐을 경우 다음 진행
    if has_heal == True :
        adb.tap(100,700) # 빠른 선택
        time.sleep(0.5)
        adb.tap(100,700) # 빠른 선택
        time.sleep(0.5)
        adb.tap(390,700) # 치료 버튼 
        time.sleep(1)
        if adb.solve_resource() == True :
            adb.tap(390,700)
            time.sleep(1)
        adb.tap(390,700) # 연맹 협조
        time.sleep(1)
        adb.back()
        return True
    elif has_heal == False :
        return False
