import os
import sys
import time
from datetime import datetime

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


def unit_action(adb, x, y, mod, all_troops=False, human_attack=False) :

    def _update_global_unit_coords(add=True):
        # automation.py 직접 실행 시 모듈명이 __main__ 이라서 분기
        mod = sys.modules.get("automation") or sys.modules["__main__"]
        load_runtime_state = mod.load_runtime_state
        save_runtime_state = mod.save_runtime_state

        state = load_runtime_state()
        coords = state.get("unit_action_coords", [])
        if not isinstance(coords, list):
            coords = []

        coord_x, coord_y = str(x), str(y)
        account = adb.runtime_read("account", -1) # 0일 때 본계정


        if add:
            now_ts = int(time.time())
            now_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            coords = [
                c for c in coords
                if not (
                    isinstance(c, dict)
                    and str(c.get("x")) == coord_x
                    and str(c.get("y")) == coord_y
                )
            ]
            coords.append({
                "x": coord_x,
                "y": coord_y,
                "time": now_human,
                "time_ts": now_ts,
                "port": adb.port,
                "account": account
            })
        else:
            coords = [
                c for c in coords
                if not (
                    isinstance(c, dict)
                    and str(c.get("x")) == coord_x
                    and str(c.get("y")) == coord_y
                )
            ]

        state["unit_action_coords"] = coords
        save_runtime_state(state)

    if adb.heal() > 0 :
        return 5

    if mod == "move" :
        text = "점령"
    elif mod == "back" :
        text = "소환"
    elif mod == "attack" :
        text = "공격"
    elif mod == "back_all" :
        text = "철수"


    if mod != "back_all" :
        adb.tap(160,800) # 좌표 검색
        time.sleep(1)
        adb.tap(185,470) # x
        time.sleep(1)
        adb.adb_backspace(5)
        adb.adb_input_text(f"{x}", press_enter=True)
        adb.tap(385,470) # y
        time.sleep(1)
        adb.adb_backspace(5)
        adb.adb_input_text(f"{y}", press_enter=True)
        time.sleep(1)
        adb.tap(270,565) # 이동
        time.sleep(1)
        adb.tap(270,480) # 땅 클릭
        time.sleep(1)


    adb.screen_shot(name="_military_base")
    time.sleep(1)

    
    ocr_result = adb.get_ocr_raw(file_name="capture_military_base.png", x_min=5, x_max=185, y_min=175, y_max=540, y_threshold=10, scale=1)
    processed_result = adb.process_ocr(result=ocr_result, x_min=5, x_max=185, y_min=175, y_max=540, y_threshold=10, scale=1, merge=False)

    if mod == "back_all" :
        for item in processed_result :
            if "주둔" in item[0] :
                adb.tap(165, item[2])
                time.sleep(1)
                adb.tap(385,590) # 소환 확인
    
        return 10

    if mod == "attack" or mod == "move":
        for item in processed_result :
            # 공격나갔는데 이미 주둔중인 병력 있으면 뺌
            if "주둔" in item[0] and mod == "attack" :
                unit_action(adb, x=x, y=y, mod="back_all")
                if all_troops == True :
                    return False
            # 이미 주둔 중
            elif any(keyword in item[0] for keyword in ["주둔"]) and mod == "move":
                return 30
            # 주둔을 위해 이미 이동중인 부대가 있음
            elif any(keyword in item[0] for keyword in ["X", "Y", "x", "y"]):
                print(item[0])
                return 20
            
    

    ocr_result = adb.get_ocr_raw(file_name="capture_military_base.png", x_min=115, x_max=425, y_min=475, y_max=840, y_threshold=10, scale=1)
    processed_result = adb.process_ocr(result=ocr_result, x_min=115, x_max=425, y_min=475, y_max=840, y_threshold=10, scale=1, merge=False)


    result = None
    flag = 0
    # 배치, 소환, 공격 버튼 누르기기
    if processed_result:
        for item in processed_result:
            # 여기서 걸리면 뭔가 있는 땅임
            if item[0] in ["채집", "수비"] :
                adb.back()
                time.sleep(1)
                if mod == "attack" :
                     _update_global_unit_coords(add=False)
                     return 200
                else :
                    return False
            # 여기서 걸리면 사람임
            elif item[0] in ["집결", "섬", "방문"] and human_attack == False :
                adb.back()
                time.sleep(1)
                return False
            elif item[0] == text and mod != "attack":
                # 원하는 기능의 동작 버튼 (ex>배치)
                result = (item[1], item[2]-10)
            # 이게 뜨면 그 자리에 뭐가 있기는 함
            if item[0] in ["상세", "공유"] :
                flag = 1

    # 공격 버튼 찾기
    if mod == "attack" :
        result = adb.search_template(name="attack")
        if result != [] :
            result = result[0][1:]
        else :
            result = None
    
    if result is None and mod == "attack" :

        # 사라짐
        if flag == 0 :
            # 모종의 이유로 사라졌으나 좌표는 지워줌
            _update_global_unit_coords(add=False)
            return 200

        return 100

    


    if result is not None :

        adb.tap(result[0], result[1])
        time.sleep(2)
        

        if mod == "back" :
            adb.tap(385,590) # 소환 확인
            return 2
        
        elif mod == "move" :
            time.sleep(1)
            adb.tap(180,190) # 영웅 취소
            time.sleep(1)

            adb.screen_shot(name="_allocation")
            result = adb.get_ocr_raw(file_name="capture_allocation.png", x_min=10, x_max=290, y_min=920, y_max=955, y_threshold=10, scale=3)
            processed_result = adb.process_ocr(result=result, x_min=10, x_max=290, y_min=920, y_max=955, y_threshold=10, scale=3, merge=False)

            flag = 0
            for item in processed_result:
                if "균등" in item[0] or "배치" in item[0] :
                    adb.tap(item[1], item[2]-45) # 균등 배치 버튼 클릭
                    time.sleep(1*adb.time)
                    adb.tap(410,910) # 출정
                    time.sleep(2*adb.time)
                    _update_global_unit_coords(add=True)
                    return True
                if "비례" in item[0] :
                    flag = 1

            if flag == 0 : # 비례라는 단어가 탐지되지 않은 경우
                adb.tap(220,890) # 균등배치
            elif flag == 1 : # 비례라는 단어가 탐지된 경우
                adb.tap(150,890) # 균등배치
            time.sleep(1*adb.time)
            adb.tap(410,910) # 출정
            time.sleep(2*adb.time)
            _update_global_unit_coords(add=True)
            return True
        
        elif mod == "attack" :

            if all_troops == False :
                adb.screen_shot(name="_allocation")
                # result = adb.get_ocr_raw(file_name="capture_allocation.png", x_min=10, x_max=290, y_min=920, y_max=955, y_threshold=10, scale=3)
                # processed_result = adb.process_ocr(result=result, x_min=10, x_max=290, y_min=920, y_max=955, y_threshold=10, scale=3, merge=False)
                result = adb.get_ocr_raw(file_name="capture_allocation.png", x_min=10, x_max=470, y_min=885, y_max=955, y_threshold=10, scale=3)
                processed_result = adb.process_ocr(result=result, x_min=10, x_max=470, y_min=885, y_max=955, y_threshold=10, scale=3, merge=False)

                flag = 0 # 배치 버튼 클릭 여부
                flag2 = 0 # 출정이 있는지 감지
                for item in processed_result:
                    if "균등" in item[0] :
                        adb.tap(item[1], item[2]-45) # 균등 배치 버튼 클릭
                        time.sleep(1*adb.time)
                        adb.tap(410,910) # 출정
                        time.sleep(2*adb.time)
                        _update_global_unit_coords(add=False)
                        return True
                    if "비례" in item[0] :
                        flag = 1
                    if any(keyword in item[0] for keyword in ["출정", "비례", "균등", "배치"]):
                        flag2 = 1

                if flag2 == 0 : # 출정할 슬롯 없음
                    return False

                if flag == 0 : # 비례라는 단어가 탐지되지 않은 경우
                    adb.tap(220,890) # 균등배치
                elif flag == 1 : # 비례라는 단어가 탐지된 경우
                    adb.tap(150,890) # 균등배치
                time.sleep(1*adb.time)
            if all_troops == True :
                adb.tap(410,910) # 출정
                _update_global_unit_coords(add=False)
                return True
    else :
        adb.back()
    return None
