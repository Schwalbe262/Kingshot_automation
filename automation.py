# TODOLIST

# 병영 업그레이드 필요할 경우 인식해서 병사생산 일시중지 기능 추가
# 하위 업그레이드 충족 필요시 업그레이드 진행 기능
# 연맹 도움 기능 자동화

import subprocess
import time

from paddleocr import PaddleOCR

import numpy as np

import cv2

import re

import os

from datetime import datetime

import traceback

import random

class ADB: 
    def __init__(self, device_ip="127.0.0.1", port=5555):
        self.adb_path = "C:\\platform-tools-latest-windows\\platform-tools\\adb.exe"
        self.device_ip = device_ip
        self.port = port
        self.device_id = f"{self.device_ip}:{self.port}"

        self.ocr = PaddleOCR(lang="korean", use_gpu=False, show_log=False)

        self.state = 0 # 0 : 대기방, 1 : 게임시작, 2 : 그 외
        self.state_cul = 0 # 같은 state 몇번 지속인지 기록
        self.base = "C:\\Users\\NEC\\Pictures\\BlueStacks"

        self.calvary = False
        self.infantry = False
        self.archer = False

        self.itr = 0

        self.time = 1

    def _f(self, name):
        """동시 실행 시 디바이스별 고유 파일명 (포트 접미사)."""
        if not name.endswith('.png'):
            return name + f'_{self.port}.png'
        return name.replace('.png', f'_{self.port}.png')

    def shell(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout = result.stdout.decode('euc-kr', errors='ignore')
            stderr = result.stderr.decode('euc-kr', errors='ignore')
            if result.returncode == 0:
                return stdout.strip()
            else:
                return stderr.strip()
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def connect(self):
        command = f'{self.adb_path} connect {self.device_id}'
        # print(f"Executing command: {command}")
        return self.shell(command)

    def apps(self, app_package):
        command = f'{self.adb_path} -s {self.device_id} shell monkey -p {app_package} -c android.intent.category.LAUNCHER 1'
        return self.shell(command)
    
    def tap(self, x, y):
        command = f'{self.adb_path} -s {self.device_id} shell input tap {x} {y}'
        # print(command)
        return self.shell(command)

    def back(self) :
        command = f'{self.adb_path} -s {self.device_id} shell input keyevent 4'
        return self.shell(command)

    def home(self):
        command = f'{self.adb_path} -s {self.device_id} shell input keyevent 3'
        return self.shell(command)

    def game_start(self) :
        self.tap(475,50) # 게임시작

    def drag_with_adb(self, x1, y1, x2, y2, duration_ms=500):
        """
        adb 객체를 사용하여 (x1, y1)에서 (x2, y2)까지 마우스 드래그(터치 스와이프)를 수행합니다.
        duration_ms: 드래그 지속 시간(밀리초 단위)
        """
        # adb shell input swipe <x1> <y1> <x2> <y2> <duration(ms)>
        cmd = [
            self.adb_path,  # 예를 들어 'C:\\platform-tools-latest-windows\\platform-tools\\adb.exe'
            "-s", f"127.0.0.1:{self.port}",
            "shell",
            "input",
            "swipe",
            str(x1), str(y1), str(x2), str(y2), str(duration_ms)
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Drag failed:", result.stderr)
        else:
            pass


    def update_kingshot(self) :

        self.home()
        time.sleep(1)
        self.tap(270,150)
        time.sleep(1)
        self.tap(375,425)
        time.sleep(1)
        self.tap(230,50)
        time.sleep(1)
        self.typing("king shot")
        time.sleep(1)

    def start_kingshot(self) :
        self.tap(110,330)

    def typing(self, word=""):

        def tap_key(c) : 
            if c == "a" : self.tap(53,751)
            elif c == "b" : self.tap(324,832)
            elif c == "c" : self.tap(218,832)
            elif c == "d" : self.tap(161,751)
            elif c == "e" : self.tap(136,669)
            elif c == "f" : self.tap(215,751)
            elif c == "g" : self.tap(271,751)
            elif c == "h" : self.tap(322,751)
            elif c == "i" : self.tap(407,669)
            elif c == "j" : self.tap(380,751)
            elif c == "k" : self.tap(431,751)
            elif c == "l" : self.tap(488,751)
            elif c == "m" : self.tap(432,832)
            elif c == "n" : self.tap(378,832)
            elif c == "o" : self.tap(457,669)
            elif c == "p" : self.tap(513,669)
            elif c == "q" : self.tap(27,669)
            elif c == "r" : self.tap(192,669)
            elif c == "s" : self.tap(109,751)
            elif c == "t" : self.tap(244,669)
            elif c == "u" : self.tap(350,669)
            elif c == "v" : self.tap(270,832)
            elif c == "w" : self.tap(82,669)
            elif c == "x" : self.tap(164,832)
            elif c == "y" : self.tap(299,669)
            elif c == "z" : self.tap(108,832)
                
            elif c == " " : self.tap(273,910)
                
            elif c == "1" : self.tap(28,664)
            elif c == "2" : self.tap(80,664)
            elif c == "3" : self.tap(135,664)
            elif c == "4" : self.tap(190,664)
            elif c == "5" : self.tap(242,664)
            elif c == "6" : self.tap(298,664)
            elif c == "7" : self.tap(350,664)
            elif c == "8" : self.tap(405,664)
            elif c == "9" : self.tap(458,664)
            elif c == "0" : self.tap(514,664)
                
            elif c == "|" : self.tap(42,913)

        string = list(word) # 타이핑
        for c in string :
            tap_key(c)


    def msg_check(self, msg, x_min, x_max, y_min, y_max, y_threshold, scale):
        self.screen_shot(name="_check_msg")
        result = self.get_ocr_raw(
            file_name="capture_check_msg.png",
            x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
            y_threshold=y_threshold, scale=scale
        )
        processed_result = self.process_ocr(
            result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
            y_threshold=y_threshold, scale=scale
        )
        return any(msg in str(item[0]) for item in processed_result)



    def get_money(self) :

        self.tap(50,920) # 토벌
        time.sleep(1)
        self.tap(460,690) # 수령
        time.sleep(1)

        result = self.msg_check(msg="수령", x_min=230, x_max=315, y_min=670, y_max=720, y_threshold=10, scale=3)

        if result == True :
            self.tap(260,690) # 수령
            time.sleep(1)
            self.back()
            time.sleep(1)

        self.back()
        time.sleep(1)



    def has_keywords(self, processed_result, keywords, min_count=1):
        """
        Checks if at least `min_count` of the given `keywords` are present (as substrings)
        in the first element of each sublist in `processed_result`.

        Args:
            processed_result (list): The OCR result list.
            keywords (list or str): Keywords to check for.
            min_count (int): Minimum number of keywords that must be found.

        Returns:
            bool: True if at least `min_count` keywords are found, False otherwise.
        """
        # Ensure keywords is a list
        if isinstance(keywords, str):
            keywords = [keywords]
        found = set()
        for keyword in keywords:
            for item in processed_result:
                if keyword in str(item[0]):
                    found.add(keyword)
                    break  # No need to count the same keyword more than once
        return len(found) >= min_count





    def get_state(self, solve_abnormal=True) :

        self.screen_shot(name="_get_state")

        state = {
            "in": False,
            "out": False,
            "queue": False,
            "abnormal": False,
            "action": False
        }


        result = self.get_ocr_raw(file_name="capture_get_state.png", x_min=0, x_max=540, y_min=870, y_max=960, y_threshold=10, scale=1)
        processed_result = self.process_ocr(result=result, x_min=0, x_max=540, y_min=870, y_max=960, y_threshold=10, scale=1, merge=False)

        result1 = self.has_keywords(processed_result, ["토벌", "가방", "상점", "영웅", "연맹"], min_count=3)
        result2 = self.has_keywords(processed_result, ["야외"], min_count=1)
        result3 = self.has_keywords(processed_result, ["도시"], min_count=1)

        if result1 and result2:
            state["in"] = True
        elif result1 and result3:
            state["out"] = True



        if state["in"] :

            # 도시 큐 창이 열려있는지 체크 (reference 1)
            result = self.get_ocr_raw(file_name="capture_get_state.png", x_min=5, x_max=330, y_min=185, y_max=220, y_threshold=10, scale=1)
            processed_result = self.process_ocr(result=result, x_min=5, x_max=330, y_min=185, y_max=220, y_threshold=10, scale=1, merge=False)
            result = self.has_keywords(processed_result, ["도시", "야외"], min_count=1)
            if solve_abnormal and result :
                self.tap(355,415) # 창 닫기
                state["action"] = True
                return state


        elif state["out"] :
            dtd = 1


        else :

            # 게임 종료창 (reference 4)
            result = self.get_ocr_raw(file_name="capture_get_state.png", x_min=150, x_max=400, y_min=400, y_max=500, y_threshold=10, scale=1)
            processed_result = self.process_ocr(result=result, x_min=150, x_max=400, y_min=400, y_max=500, y_threshold=10, scale=1, merge=False)
            result = self.has_keywords(processed_result, ["게임", "종료"], min_count=2)
            if solve_abnormal and result :
                self.back()
                state["action"] = True
                return state


            # 건설 창이 열려있는지 체크
            result = self.get_ocr_raw(file_name="capture_get_state.png", x_min=0, x_max=540, y_min=855, y_max=960, y_threshold=10, scale=1)
            processed_result = self.process_ocr(result=result, x_min=0, x_max=540, y_min=855, y_max=960, y_threshold=10, scale=1, merge=False)
            result = self.has_keywords(processed_result, ["건설", "가속"], min_count=2)
            if solve_abnormal and result :
                self.back()
                state["action"] = True
                return state


            # 가방에 들어가 있는지 체크
            result = self.get_ocr_raw(file_name="capture_get_state.png", x_min=65, x_max=125, y_min=5, y_max=50, y_threshold=10, scale=1)
            processed_result = self.process_ocr(result=result, x_min=65, x_max=125, y_min=5, y_max=50, y_threshold=10, scale=1, merge=False)
            result = self.has_keywords(processed_result, ["가방"], min_count=1)
            if solve_abnormal and result :
                self.back()
                state["action"] = True
                return state


            # 그 외
            self.back()
            state["action"] = True
            return state



        return state


    def solve_abnormal(self) :

        return 0





    def state_check(self):

        self.tap(10,415)
        time.sleep(0.5 * self.time)
        self.tap(90,200) # 도시 클릭
        time.sleep(0.5 * self.time)

        self.screen_shot(name="_state_check1")

        result = self.get_ocr_raw_advanced(file_name="capture_state_check1.png", x_min=60, x_max=300, y_min=255, y_max=640, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
        processed_result = self.process_ocr(result=result, x_min=60, x_max=300, y_min=255, y_max=640, y_threshold=10, scale=3, merge=True)

        list = [["대열1", "업그", "레이드"], ["대열2", "업그", "레이드"], ["보병"], ["기병"], ["궁병"], ["과학", "기술", "연구"]]
        result_s1 = []
        index = 0


        broke_early = False
        for i in range(len(processed_result) - 1):
            curr_text = str(processed_result[i][0]).replace(" ", "")      # 현재 원소 text (공백 제거)
            next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

            flag = True # 과학기술연구 / 과학기술연구 중첩으로 있는거 검출용 (False되면 검출 된 경우)

            for comp in list[index]:
                if comp in curr_text:
                    for comp2 in list[index]:
                        if comp2 in next_text:
                            flag = False
                    if flag == True :
                        result_s1.append(next_text)
                        # print(f"{curr_text} : {next_text}")
                        index = index + 1
                        break

            if index == 6:
                broke_early = True
                break

        # for문을 다 못돌았을 때 조기 종료 (인식 에러 있는 경우)
        if not broke_early :
            self.tap(355,415)
            time.sleep(0.5 * self.time)
            print(f"adb{self.itr} state1 인식 에러 발생")
            print(processed_result)
            return False
            
        for itr, res in enumerate(result_s1):

            if "한가" in res or "가함" in res : # 한가함
                result_s1[itr] = 1
            elif (res.count(":") == 2 and all(part.isalnum() for part in res.split(":"))) : # 진행 중
                result_s1[itr] = 0
            elif "완료" in res : # 완료 (병사 훈련)
                result_s1[itr] = 2
            else : # 인식 안되는 경우 -> 진행 중 처리
                result_s1[itr] = 0


        # ==============for state2 ==============

        self.tap(250,200) # 야외 클릭
        time.sleep(0.5 * self.time)

        self.screen_shot(name="_state_check2")

        result = self.get_ocr_raw_advanced(file_name="capture_state_check2.png", x_min=60, x_max=300, y_min=255, y_max=640, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
        processed_result = self.process_ocr(result=result, x_min=60, x_max=300, y_min=255, y_max=640, y_threshold=10, scale=3, merge=True)

        result_s2 = []
        index = 0

        broke_early = False
        for i in range(len(processed_result) - 1):
            curr_text = str(processed_result[i][0]).replace(" ", "")      # 현재 원소 text (공백 제거)
            next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

            if any(keyword in curr_text for keyword in ["행군", "대열", "복귀", "공격격"]):
                result_s2.append(next_text)
                index = index + 1
            elif "방앗간" in curr_text:
                result_s2.append("빵")
                index = index + 1
            elif "벌목장" in curr_text:
                result_s2.append("목재")
                index = index + 1
            elif "채석장" in curr_text:
                result_s2.append("석재")
                index = index + 1
            elif "철광장" in curr_text:
                result_s2.append("철광")
                index = index + 1
            if any(keyword in curr_text for keyword in ["비어", "채집"]):
                result_s2.append("채집")
                index = index + 1

            if index == 6:
                broke_early = True
                break

        # for문을 다 못돌았을 때 조기 종료 (인식 에러 있는 경우)
        if not broke_early :
            self.tap(90,200) # 도시 클릭
            time.sleep(0.5 * self.time)
            self.tap(355,415) # 창 닫기
            time.sleep(0.5 * self.time)
            print(f"adb{self.itr} state2 인식 에러 발생")
            print(processed_result)
            return False

        for itr, res in enumerate(result_s2):

            if "한가함" in res : # 한가함
                result_s2[itr] = 0
            elif any(material in res for material in ["빵", "목재", "석재", "철광"]) :
                result_s2[itr] = res
            else :
                result_s2[itr] = 2

        self.tap(90,200) # 도시 클릭
        time.sleep(0.5 * self.time)
        self.tap(355,415) # 창 닫기
        time.sleep(0.5 * self.time)

        result = [result_s1, result_s2]
        return result


        
                

    
    def get_stamina(self) :

        self.tap(35,35) # 초상화 클릭
        time.sleep(1.0 * self.time)

        self.screen_shot(name="_check_stamina")

        result = self.get_ocr_raw(file_name="capture_check_stamina.png", x_min=80, x_max=150, y_min=820, y_max=850, y_threshold=10, scale=1)
        processed_result = self.process_ocr(result=result, x_min=80, x_max=150, y_min=820, y_max=850, y_threshold=10, scale=1, merge=True)

        stamina = int(str(processed_result[0][0]).split('/')[0].strip())
        print(f"adb{self.itr} stamina: {stamina}")

        if stamina > 0 :
            pass
        else :
            stamina = 0

        self.back()
        time.sleep(0.5 * self.time)

        return stamina



    
    def get_unit(self, type) :

        if type == "보병" :
            self.tap(10,415)
            time.sleep(1)
            self.tap(305,420) # 보병
            time.sleep(1)
            self.tap(270,315) # 생산 확인
            time.sleep(1)

        elif type == "기병" :
            self.tap(10,415)
            time.sleep(1)
            self.tap(305,475) # 기병
            time.sleep(1)
            self.tap(270,315) # 생산 확인
            time.sleep(1)

        elif type == "궁병" :
            self.tap(10,415)
            time.sleep(1)
            self.tap(305,530) # 궁병
            time.sleep(1)
            self.tap(270,315) # 생산 확인
            time.sleep(1)



    def research(self) :


        def research_try(itr=3) :

            for attempt in range(itr):

                self.screen_shot(name="_research")

                result = self.get_ocr_raw_advanced(file_name="capture_research.png", x_min=30, x_max=510, y_min=115, y_max=950, y_threshold=10, scale=3, binary_threshold=170)
                processed_result = self.process_ocr(result=result, x_min=30, x_max=510, y_min=115, y_max=950, y_threshold=10, scale=3, merge=False)

                position = pattern_search(processed_result)

                # print("========== 연구 큐 인식   ==========")
                # print(processed_result)
                # print("================================")
                # print(position)
                # print("================================")

                if position == [] :
                    self.drag_with_adb(270, 530, 270, 450, duration_ms=100)
                    time.sleep(1)
                    continue

                for x, y in position:

                    print(x, y)

                    if x != 0 and y != 0:
                        self.tap(x, y)
                        time.sleep(1)

                        self.screen_shot(name="_research_check")
                        result = self.get_ocr_raw_advanced(file_name="capture_research_check.png", x_min=310, x_max=510, y_min=650, y_max=850, y_threshold=10, scale=3, binary_threshold=170)
                        processed_result = self.process_ocr(result=result, x_min=310, x_max=510, y_min=650, y_max=850, y_threshold=10, scale=3, merge=False)
                        

                        x_check = 0
                        y_check = 0
                        button_flag = False

                        for item in processed_result:
                            if "연구" in str(item[0]):
                                x_check = item[1]
                                y_check = item[2]
                                button_flag = True
                                break

                        if button_flag == False:
                            self.screen_shot(name="_research_state")
                            result = self.get_ocr_raw_advanced(file_name="capture_research_state.png", x_min=65, x_max=230, y_min=5, y_max=45, y_threshold=10, scale=3, binary_threshold=170)
                            processed_result = self.process_ocr(result=result, x_min=65, x_max=230, y_min=5, y_max=45, y_threshold=10, scale=3, merge=False)
                            flag = False
                            for item in processed_result:
                                if "과학" in str(item[0]):
                                    flag = True
                                    break
                            if flag == False :
                                time.sleep(1)
                                self.back()
                            
                        elif button_flag == True:
                            # print("========== 연구 버튼 인식 ==========")
                            # print(processed_result)
                            # print(x_check, y_check)
                            # print("================================")

                            self.tap(x_check, y_check)  # 연구 버튼
                            time.sleep(1)
                                    
                            self.tap(455, 895)  # 연맹 협조
                            time.sleep(1)
                            self.back()
                            time.sleep(1)
                            print(f"adb{self.itr} 과학기술 연구 시작 (시도 {attempt+1})")
                            return True

                time.sleep(1)
                self.drag_with_adb(270, 530, 270, 450, duration_ms=100)
                time.sleep(1)

            return False
        

        def pattern_search(processed_result) :

            position = []

            x = 0
            y = 0
            pattern = r"^\d+/\d+$"
            for item in processed_result:
                if re.match(pattern, item[0].replace(" ", "")):
                    x = item[1]
                    y = item[2]
                    position.append([x, y])

            return position




        self.tap(10,415)
        time.sleep(2)
        self.tap(305,610) # 과학기술 연구
        time.sleep(3)
        self.tap(360,550) # 연구 버튼
        time.sleep(2)


        # self.drag_with_adb(270, 400, 270, 600, duration_ms=500)
        time.sleep(1)

        result = research_try()

        if result == True :
            time.sleep(1)
            return True
        else :
            time.sleep(1)
            self.tap(100,85)
            time.sleep(1)
            self.drag_with_adb(270, 300, 270, 400, duration_ms=300)

        result = research_try()

        if result == True :
            time.sleep(1)
            return True
        else :
            time.sleep(1)
            self.tap(270,85)
            time.sleep(1)
            self.drag_with_adb(270, 300, 270, 400, duration_ms=300)

        result = research_try()

        if result == True :
            time.sleep(1)
            return True
        else :
            time.sleep(1)
            self.tap(440,85)
            time.sleep(1)
            self.drag_with_adb(270, 300, 270, 400, duration_ms=1000)
            time.sleep(1)
            self.drag_with_adb(270, 300, 270, 400, duration_ms=1000)
            time.sleep(1)
            self.drag_with_adb(270, 300, 270, 400, duration_ms=1000)

        result = research_try(itr=8)

        if result == True :
            time.sleep(1)
            return True
        else :
            self.back()
            time.sleep(1)





        

        

        
  

    def build_city_new(self, building) :

        def upgrade_button(self) :

            self.screen_shot(name="_upgrade_button")
            result = self.get_ocr_raw_advanced(file_name="capture_upgrade_button.png", x_min=320, x_max=480, y_min=875, y_max=935, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
            processed_result = self.process_ocr(result=result, x_min=320, x_max=480, y_min=875, y_max=935, y_threshold=10, scale=3, merge=False)

            for result in processed_result :
                text = str(result[0]).replace(" ", "")

                keywords = ["업그레이드", "업그레", "업그", "레이드"]
                if any(keyword in text for keyword in keywords):
                    self.tap(400,910)
                    time.sleep(1*self.time)
                    abnormal = self.check_abnormal()
                    if abnormal == False :
                        self.tap(270,330) # 도움 버튼
                    return True

        self.tap(10,415)
        time.sleep(1*self.time)
        if building == 1 :
            self.tap(305,285) # 건물 1
        elif building == 2 :
            self.tap(305,335) # 건물 2
        time.sleep(2*self.time)


        # ====================
        # 1번 케이스 일반 건물
        # ====================

        # 건물 확인
        self.screen_shot(name="_check_building")
        result = self.get_ocr_raw_advanced(file_name="capture_check_building.png", x_min=200, x_max=350, y_min=300, y_max=335, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
        processed_result = self.process_ocr(result=result, x_min=200, x_max=350, y_min=300, y_max=335, y_threshold=10, scale=3, merge=False)

        keywords = ["보병", "기병", "궁병"]
        for result in processed_result :
            text = str(result[0]).replace(" ", "")
            if any(keyword in text for keyword in keywords): # 
                self.tap(365,550) # 훈련 버튼
                time.sleep(0.5*self.time)
                
                # 훈련 상태인지 체크
                self.screen_shot(name="_check_training")
                result = self.get_ocr_raw_advanced(file_name="capture_check_training.png", x_min=320, x_max=440, y_min=810, y_max=855, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
                processed_result = self.process_ocr(result=result, x_min=320, x_max=440, y_min=810, y_max=855,  y_threshold=10, scale=3, merge=False)
                for result in processed_result :
                    if "가속" in result[0] :
                        self.tap(465,685) # 취소 버튼
                        time.sleep(0.5*self.time)
                        self.tap(380,590)
                        time.sleep(0.5*self.time)
                        break
                self.back()
                time.sleep(0.5*self.time)
                self.tap(275,400)
                time.sleep(0.5*self.time)

        # 대사관에 도움 요청 떠있는 경우 건물 눌러도 업그레이드 안뜨는 경우 있음음
        if processed_result == [] : 
            self.tap(275,460)
            time.sleep(0.5*self.time)



        # 좌표 확인
        x = 0
        y = 0

        self.screen_shot(name="_upgrade_button")
        result = self.get_ocr_raw_advanced(file_name="capture_upgrade_button.png", x_min=170, x_max=410, y_min=520, y_max=640, y_threshold=10, scale=3, gamma=0.8, use_binary=False)
        processed_result = self.process_ocr(result=result, x_min=170, x_max=410, y_min=520, y_max=640, y_threshold=10, scale=3, merge=False)

        for result in processed_result :
            text = str(result[0]).replace(" ", "")

            keywords = ["업그레이드", "업그레", "업그", "레이드", "건설설"]
            if any(keyword in text for keyword in keywords):
                x = result[1]
                y = result[2] - 40
                break

        # 업그레이드 버튼이 인식 된 경우
        if x != 0 and y != 0 :
            self.tap(x, y)
            time.sleep(1*self.time)
            self.tap(390,750)
            time.sleep(2)
            abnormal = self.check_abnormal()
            if abnormal == False :
                self.tap(270,330) # 도움 버튼
            return True

        # ====================
        # ====================


        # ====================
        # 2번 케이스 특수 건물
        # ====================
        self.tap(450,465) # 일단 업그레이드 버튼 눌러보기
        time.sleep(2*self.time)

        if upgrade_button(self) :
            return True

        for _ in range(10) :
            self.tap(450,500) # 업그레이드 해보기
            time.sleep(0.5*self.time)
            self.tap(450,400) # 일단 업그레이드 버튼 눌러보기
            time.sleep(2*self.time)
            if upgrade_button(self) :
                return True
        # ====================
        # ====================








  
        




    def build_city(self, building) :

        def check_msg(msg, x_min, x_max, y_min, y_max, y_threshold, scale):
            self.screen_shot(name="_barracks_button")
            result = self.get_ocr_raw(
                file_name="capture_barracks_button.png",
                x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            processed_result = self.process_ocr(
                result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            # print(processed_result)
            return any(msg in str(item[0]) for item in processed_result)

        def is_upgrade_word(text):
            """
            OCR에서 분리되어 인식될 수 있는 '업그레이드'도 허용하기 위한 함수.
            예: '업그' + '레이드', '업그레' + '이드', 또는 글자가 분리됨
            """
            # 완전 일치
            if text == "업그레이드":
                return True

            # 부분 문자열 조합 허용 (공백 포함)
            merged = text.replace(" ", "")
            if "업그레이드" in merged:
                return True

            # 일부 패턴: '업그', '업그레', '레이드', '이드' 등이 섞여 있을 때
            parts = ["업그", "업그레", "레이드", "이드"]
            score = 0
            for p in parts:
                if p in text:
                    score += 1
            # 2개 이상 들어가면 업그레이드로 간주 (분할 케이스 커버)
            if score >= 2:
                return True

            return False

        def merge_upgrade_ocr_items(processed_result):
            """
            분리된 '업그레이드' 단어를 합치기 위한 헬퍼 함수
            processed_result: [[str, x, y, ...], ...]
            """
            # 단일 텍스트로 인식되었으면 OK, 아니라면 여러 결과 조합
            upgrades = []
            n = len(processed_result)
            for i, item in enumerate(processed_result):
                text = str(item[0]).replace(" ", "")
                # 부분 일치 or 시작/끝 조합 확인
                if text == "업그레이드":
                    upgrades.append(item)
                    continue

                # 조합 케이스(예: 다음 ocr 박스와 이어질 경우)
                if text.startswith("업그") or text.startswith("업그레"):
                    # 다음 박스가 있으면 붙여서 판단
                    if (i + 1) < n:
                        next_text = str(processed_result[i+1][0]).replace(" ", "")
                        combined = text + next_text
                        if "업그레이드" in combined:
                            # 평균 위치로 대표 좌표 생성 (최소 x, 최소 y)
                            new_x = (item[1] + processed_result[i+1][1]) / 2
                            new_y = (item[2] + processed_result[i+1][2]) / 2
                            upgrades.append([combined, new_x, new_y])
                            continue
                # 혹시 '레이드' 또는 '이드'로 끝남 + 직전이 업그레/업그이면 체크
                if (text.endswith("레이드") or text.endswith("이드")) and i > 0:
                    prev_text = str(processed_result[i-1][0]).replace(" ", "")
                    combined = prev_text + text
                    if "업그레이드" in combined:
                        # 평균 위치로 대표 좌표 생성 (최소 x, 최소 y)
                        new_x = (item[1] + processed_result[i-1][1]) / 2
                        new_y = (item[2] + processed_result[i-1][2]) / 2
                        upgrades.append([combined, new_x, new_y])
                        continue
                # 단건도 길이가 충분하면(5글자 이상 등) "업그에이드" 등 잘못 인식 차단
                if len(text) >= 4 and "업그" in text and "이드" in text:
                    upgrades.append(item)
                    continue
            return upgrades

        def upgrade_ocr(self, x_min, x_max, y_min, y_max, y_threshold, scale) :
            self.screen_shot(name="_upgrade_button")
            result = self.get_ocr_raw(file_name="capture_upgrade_button.png", x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, y_threshold=y_threshold, scale=scale)
            processed_result = self.process_ocr(result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, y_threshold=y_threshold, scale=scale)

            # 여기서 분리된 단어까지 커버하도록 업그레이드 인식
            upgrade_items = merge_upgrade_ocr_items(processed_result)
            first_upgrade = upgrade_items[0] if upgrade_items else None
            return first_upgrade

        def upgrade_check(self) :
            x = 0
            y = 0

            self.screen_shot(name="_upgrade_check")
            result = self.get_ocr_raw(file_name="capture_upgrade_check.png", x_min=110, x_max=465, y_min=470, y_max=680, y_threshold=10, scale=3)
            processed_result = self.process_ocr(result=result, x_min=110, x_max=465, y_min=470, y_max=680, y_threshold=10, scale=3, merge=False)

            has_detail = any("상세" in str(item[0]) for item in processed_result)
            # 업그레이드 여부를 개선된 함수로 판단
            has_upgrade = False
            for item in processed_result:
                if is_upgrade_word(str(item[0])):
                    has_upgrade = True
                    break

            result = has_detail and has_upgrade

            if result == True:
                upgrade_items = merge_upgrade_ocr_items(processed_result)
                first_upgrade = upgrade_items[0] if upgrade_items else None
                if first_upgrade is not None:
                    x = first_upgrade[1]
                    y = first_upgrade[2]

                    if "업그레이드" == first_upgrade[0] or "업그레이드" in str(first_upgrade[0]):
                        return result, x, y-50


                    # # 분리 강인성: 좌표 변환은 기존대로
                    # if "상세 업그레이드" == first_upgrade[0] :
                    #     return result, x+50, y-50
                    # elif "업그레이드" == first_upgrade[0] or "업그레이드" in str(first_upgrade[0]):
                    #     return result, x, y-50
                    # else:
                    #     return result, x+50, y-50

            return result, x, y



        self.tap(10,415)
        time.sleep(1)
        if building == 1 :
            self.tap(305,285) # 건물 1
        elif building == 2 :
            self.tap(305,335) # 건물 2
        time.sleep(3)

        calvary = False
        infantry = False
        archer = False  

        # # 훈련 취소
        # troop_names = ["기병대", "궁병대", "보병대"]
        # for troop in troop_names:
        #     check_resource = check_msg(msg=troop, x_min=245, x_max=325, y_min=300, y_max=335, y_threshold=10, scale=3)
        #     if check_resource:
        #         for x, y in [(400, 520), (465, 685), (380, 585)]:
        #             self.tap(x, y)
        #             time.sleep(1)
        #         self.back()
        #         time.sleep(1)


        # # 원래대로 되돌리기 - 반복문 최적화 이전의 코드를 복원
        # if self.calvary == False :
        #     check_resource = check_msg(msg="기병대", x_min=245, x_max=325, y_min=300, y_max=335, y_threshold=10, scale=3)
        #     if check_resource == True :
        #         self.calvary = True
        #         calvary = True
        #         print(f"기병대 건설 예약")


        # if self.infantry == False :
        #     check_resource = check_msg(msg="보병대", x_min=245, x_max=325, y_min=300, y_max=335, y_threshold=10, scale=3)
        #     if check_resource == True :
        #         self.infantry = True
        #         infantry = True
        #         print("보병대 건설 예약")

        # if self.archer == False :
        #     check_resource = check_msg(msg="궁병대", x_min=245, x_max=325, y_min=300, y_max=335, y_threshold=10, scale=3)
        #     if check_resource == True :
        #         self.archer = True
        #         archer = True
        #         print("궁병대 건설 예약")

        
        # 건설 인식해서 되도록 수정
        check_resource = check_msg(msg="건설", x_min=240, x_max=300, y_min=875, y_max=905, y_threshold=10, scale=3)
        if check_resource == True :
            self.tap(270,900)
            time.sleep(3)
            print("신규 건물 건설")
            return True
        # check_resource = check_msg(msg="방어탑", x_min=5, x_max=150, y_min=375, y_max=425, y_threshold=10, scale=3)
        # if check_resource == True :
        #     self.tap(270,900)
        #     time.sleep(3)
        #     print("방어탑 건설")
        #     return True
        # check_resource = check_msg(msg="민가", x_min=5, x_max=150, y_min=375, y_max=425, y_threshold=10, scale=3)
        # if check_resource == True :
        #     self.tap(270,900)
        #     time.sleep(3)
        #     print("민가 건설")
        #     return True


        self.tap(260,420) # 한번 눌러주기
        time.sleep(1)
        self.tap(270,420) # 한번 눌러주기
        time.sleep(1)

        check_resource = check_msg(msg="건설", x_min=405, x_max=515, y_min=475, y_max=530, y_threshold=10, scale=3)
        if check_resource == True :
            self.tap(460,500)
            time.sleep(3)
            print("신규 장비 건설")
            return True


        # 일반 건물

        result, x, y = upgrade_check(self)
        time.sleep(3)


        if result == True :
            self.tap(x,y) # 업그레이드 버튼 누르기
            time.sleep(3)


            check_resource = check_msg(msg="추가", x_min=380, x_max=515, y_min=425, y_max=680, y_threshold=10, scale=3)
            if check_resource == True :
                self.tap(500,185)
                time.sleep(3)
                print("건물 업그레이드 자원 부족")
                return False


            result = upgrade_ocr(self, x_min=240, x_max=510, y_min=580, y_max=820, y_threshold=10, scale=3)

            if result != None : 
                x = result [1]
                y = result [2]
                self.tap(x,y) # 업그레이드 버튼 누르기
                
            time.sleep(3)
            self.tap(270,330) # 도움 버튼

            if calvary == True :
                self.calvary = False
            if infantry == True :
                self.infantry = False
            if archer == True :
                self.archer = False


        # 포탑 등 업그레이드
        result = upgrade_ocr(self, x_min=360, x_max=535, y_min=350, y_max=655, y_threshold=10, scale=3)

        if result != None :
            x = result[1]
            y = result[2]

            self.tap(x,y) # 업그레이드 버튼
            time.sleep(0.5)
            self.tap(495,900) # 업그레이드 확인
            time.sleep(3)
            self.tap(270,330) # 도움 버튼







    def unit_training(self, unit) :

        def check_msg(msg, x_min, x_max, y_min, y_max, y_threshold, scale):
            self.screen_shot(name="_barracks_button")
            result = self.get_ocr_raw(
                file_name="capture_barracks_button.png",
                x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            processed_result = self.process_ocr(
                result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            return any(msg in str(item[0]) for item in processed_result)

        self.tap(10,415)
        time.sleep(1)

        if unit == "보병" :
            self.tap(305,420) # 보병
        elif unit == "기병" :
            self.tap(305,475) # 기병
        elif unit == "궁병" :
            self.tap(305,530) # 궁병

        time.sleep(3)
        self.tap(395,525) # 훈련버튼
        time.sleep(1)
        self.tap(390,830) # 생산버튼
        time.sleep(2)

        check_resource = check_msg(msg="추가", x_min=210, x_max=330, y_min=90, y_max=125, y_threshold=10, scale=3)
        if check_resource == True :
            # self.tap(500,105)
            self.back()
            time.sleep(3)
            print("병력 생산 자원 부족")
            

        # self.tap(40,25) # 뒤로가기
        self.back()
        time.sleep(1)







    def troops_back(self):

        def check_msg(msg, x_min, x_max, y_min, y_max, y_threshold, scale):
            self.screen_shot(name="_barracks_button")
            result = self.get_ocr_raw(
                file_name="capture_barracks_button.png",
                x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            processed_result = self.process_ocr(
                result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                y_threshold=y_threshold, scale=scale
            )
            return any(msg in item[0] for item in processed_result)

        y_coords = [200, 245, 290, 335]
        for y in y_coords:
            self.tap(165, y)
            time.sleep(1)
            result = check_msg("행군", 215, 330, 230, 275, 10, 3)
            if result:
                self.back()
            else:
                self.tap(385, 590)
            time.sleep(1)


    def resource_remain(self) :

        def parse_million_value(text):
            if text is None or not isinstance(text, (str, bytes)):
                return 0.0
            text_nospace = re.sub(r'[^a-zA-Z0-9]', '', str(text))
            match_m = re.match(r"(\d+)\s*M", text_nospace, re.IGNORECASE)
            match_k = re.match(r"(\d+)\s*K", text_nospace, re.IGNORECASE)

            if match_m:
                number_str = match_m.group(1)
                number = float(number_str) / 10  # 104 -> 10.4
                multiplier = 1e6
                return number * multiplier
            elif match_k:
                number_str = match_k.group(1)
                number = float(number_str) / 10  # 104 -> 10.4
                multiplier = 1e3
                return number * multiplier
            return 0.0

        self.tap(370,20) # 자원버튼 클릭
        time.sleep(1)
        self.screen_shot(name="_resource_remain")

        
        # Helper to safely extract text from OCR result
        def get_first_text(result):
            if result and isinstance(result, list) and len(result) > 0 and len(result[0]) > 0:
                return result[0][0]
            return ""

        result = self.get_ocr_raw(file_name="capture_resource_remain.png", x_min=345, x_max=430, y_min=375, y_max=395, y_threshold=10, scale=3)
        result = self.process_ocr(result=result, x_min=345, x_max=430, y_min=375, y_max=395, y_threshold=10, scale=3)
        text = get_first_text(result)
        bread_value = parse_million_value(text)

        result = self.get_ocr_raw(file_name="capture_resource_remain.png", x_min=345, x_max=430, y_min=460, y_max=480, y_threshold=10, scale=3)
        result = self.process_ocr(result=result, x_min=345, x_max=430, y_min=460, y_max=480, y_threshold=10, scale=3)
        text = get_first_text(result)
        wood_value = parse_million_value(text)

        result = self.get_ocr_raw(file_name="capture_resource_remain.png", x_min=345, x_max=430, y_min=545, y_max=565, y_threshold=10, scale=3)
        result = self.process_ocr(result=result, x_min=345, x_max=430, y_min=545, y_max=565, y_threshold=10, scale=3)
        text = get_first_text(result)
        stone_value = parse_million_value(text)

        result = self.get_ocr_raw(file_name="capture_resource_remain.png", x_min=345, x_max=430, y_min=630, y_max=655, y_threshold=10, scale=3)
        result = self.process_ocr(result=result, x_min=345, x_max=430, y_min=630, y_max=655, y_threshold=10, scale=3)
        text = get_first_text(result)
        iron_value = parse_million_value(text)

        self.tap(515,265) # 자원버튼 클릭


        return bread_value, wood_value, stone_value, iron_value


    def hunting(self) :

        # 한단계 높여서 안됐을 시 코드 추가필요

        self.tap(35,660) # 서치버튼

        time.sleep(1*self.time)

        self.tap(70,675) # 야수
        time.sleep(1*self.time)

        self.tap(365,790) # 한단계 높이기
        time.sleep(1*self.time)
        self.tap(270,910) # 검색
        time.sleep(5*self.time)

        self.tap(270,470) # 공격
        time.sleep(1*self.time)
        self.tap(220,890) # 균등배치
        time.sleep(1*self.time)
        self.tap(410,910) # 출정
        time.sleep(2*self.time)




    def resource_farming(self, resource) :

        def check_msg(self, msg, x_min, x_max, y_min, y_max, y_threshold, scale) :

            self.screen_shot(name="_resource_check")
            result = self.get_ocr_raw(file_name="capture_resource_check.png", x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, y_threshold=y_threshold, scale=scale)
            processed_result = self.process_ocr(result=result, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, y_threshold=y_threshold, scale=scale)

            check_result = any(msg in item[0] for item in processed_result)
            return check_result

        self.tap(35,660) # 서치버튼

        time.sleep(1)

        self.drag_with_adb(510, 685, 30, 685, duration_ms=1000)

        time.sleep(1)

        if resource == "빵" :
            self.tap(125,685) # 빵
        elif resource == "목재" :
            self.tap(240,685) # 목재
        elif resource == "석재" :
            self.tap(360,685) # 석재
        elif resource == "철광" :
            self.tap(480,685) # 철광



        self.tap(365,790) # 한단계 높이기
        time.sleep(1)
        self.tap(270,910) # 검색
        time.sleep(10)



        for _ in range(3):
            check_result = check_msg(self, "채집", 240, 305, 455, 485, 10, 3)
            if check_result == True:
                break
            elif check_result == False:  # 검색이 안되는 경우
                self.tap(55,790) # 한단계 낮추기
                time.sleep(1)
                self.tap(270,910) # 검색
                time.sleep(10)
                

        self.tap(270,470) # 채집
        time.sleep(1)

        # 잔여 칸 없는 경우
        result = check_msg(self, "행군", 215, 330, 230, 275, 10, 3)
        
        if result == True : # 잔여 칸 없는 경우
            self.back()
            time.sleep(2)
            self.back()
            time.sleep(2)
            return False
        elif result == False : # 잔여 칸 있는 경우 배치
            self.tap(320,190) # 영웅 2 취소
            time.sleep(1)
            self.tap(460,190) # 영웅 3 취소
            time.sleep(1)
            self.tap(220,890) # 균등배치
            time.sleep(1)
            self.tap(410,910) # 출정
            time.sleep(2)
            return True


    def get_hero(self) :

        self.tap(10,415)
        time.sleep(1)
        self.drag_with_adb(170, 625, 170, 275, duration_ms=500)
        time.sleep(0.5)
        self.screen_shot(name="_hero")

        result = self.get_ocr_raw(file_name="capture_hero.png", x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3)
        processed_result = self.process_ocr(result=result, x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3, merge=True)

        processed_result


        target_avg = None  # 결과를 담을 변수

        for i in range(len(processed_result) - 1):
            curr_text = str(processed_result[i][0]).replace(" ", "")      # 현재 원소 text (공백 제거)
            next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

            if "고급모" in curr_text and "무료모" in next_text:
                curr_val = float(processed_result[i][2])      # 고급모집의 2번 인덱스
                print(curr_val)
                next_val = float(processed_result[i + 1][2])  # 무료모집의 2번 인덱스
                target_avg = (curr_val + next_val) / 2.0
                self.tap(305, target_avg) # 모집 버튼 누르기
                time.sleep(1)
                self.tap(150, 630) # 고급 모집 버튼 누르기
                time.sleep(10) # 뽑기 애니메이션 기다림림
                self.back()
                time.sleep(1)
                self.back()
                print(f"adb{self.itr} 고급 모집 완료")
                break
            elif "에픽모" in curr_text and "무료모" in next_text:
                curr_val = float(processed_result[i][2])      # 에픽픽모집의 2번 인덱스
                print(curr_val)
                next_val = float(processed_result[i + 1][2])  # 무료모집의 2번 인덱스
                target_avg = (curr_val + next_val) / 2.0
                self.tap(305, target_avg) # 모집 버튼 누르기
                time.sleep(1)
                self.tap(150, 900) # 고급 모집 버튼 누르기
                time.sleep(10) # 뽑기 애니메이션 기다림림
                self.back()
                time.sleep(1)
                self.back()
                print(f"adb{self.itr} 에픽 모집 완료")
                break

        time.sleep(1)
        self.tap(355,415) # 영웅 창 닫기


    def get_supply(self) :

        self.tap(10,415)
        time.sleep(1)
        self.drag_with_adb(170, 625, 170, 275, duration_ms=800)
        time.sleep(0.5)
        self.screen_shot(name="_supply")

        result = self.get_ocr_raw(file_name="capture_supply.png", x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3)
        processed_result = self.process_ocr(result=result, x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3, merge=True)

        processed_result

        target_avg = None  # 결과를 담을 변수

        for i in range(len(processed_result) - 1):
            curr_text = str(processed_result[i][0]).replace(" ", "")      # 현재 원소 text (공백 제거)
            next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

            if "창고보급" in curr_text and "완료" in next_text:
                curr_val = float(processed_result[i][2])      # y좌표
                print(curr_val)
                next_val = float(processed_result[i + 1][2])  # y좌표
                target_avg = (curr_val + next_val) / 2.0
                self.tap(305, target_avg) # 보급품 수령 버튼튼
                time.sleep(1)
                self.tap(270,420)
                time.sleep(1)
                self.tap(275,345) # 수령 버튼
                time.sleep(10)
                self.tap(270,420)
                print(f"adb{self.itr} 보급품 수령 완료료")
                break


        time.sleep(1)
        self.tap(355,415) # 영웅 창 닫기


    def union_research(self) :

        self.tap(10,415)
        time.sleep(1)
        self.drag_with_adb(170, 625, 170, 275, duration_ms=800)
        time.sleep(1)
        self.screen_shot(name="_union_research")

        result = self.get_ocr_raw(file_name="capture_union_research.png", x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3)
        processed_result = self.process_ocr(result=result, x_min=5, x_max=325, y_min=250, y_max=645, y_threshold=10, scale=3, merge=True)


        target_avg = None  # 결과를 담을 변수

        for i in range(len(processed_result) - 1):
            curr_text = str(processed_result[i][0]).replace(" ", "")      # 현재 원소 text (공백 제거)
            next_text = str(processed_result[i + 1][0]).replace(" ", "")  # 다음 원소 text (공백 제거)

            if "기부" in curr_text and "가능" in next_text:
                curr_val = float(processed_result[i][2])      # 고급모집의 2번 인덱스
                next_val = float(processed_result[i + 1][2])  # 무료모집의 2번 인덱스
                target_avg = (curr_val + next_val) / 2.0
                self.tap(300, target_avg) # 연맹 기부 버튼 누르기
                time.sleep(1)
                self.tap(400, 920) # 연맹 버튼 누르기
                time.sleep(3)
                self.tap(420, 700) # 연맹 과학 기술 버튼 누르기
                time.sleep(1)
                break
            else :
                pass
        else:
            self.tap(355,415)
            return False


        time.sleep(1)
        self.tap(510,530)
        time.sleep(1)

        self.screen_shot(name="_union_research_queue")

        result = self.get_ocr_raw_advanced(file_name="capture_union_research_queue.png", x_min=30, x_max=510, y_min=235, y_max=950, y_threshold=10, scale=3, binary_threshold=170)
        processed_result = self.process_ocr(result=result, x_min=30, x_max=510, y_min=235, y_max=950, y_threshold=10, scale=3, merge=False)

        pattern = r"^\d+/\d+$"
        for item in processed_result:

            x = 0
            y = 0

            if re.match(pattern, item[0].replace(" ", "")):

                x = item[1]
                y = item[2]

                if x != 0 and y != 0 :
                    self.tap(x,y)
                    time.sleep(1)

                    self.screen_shot(name="_union_done")
                    result = self.get_ocr_raw_advanced(file_name="capture_union_done.png", x_min=295, x_max=475, y_min=690, y_max=820, y_threshold=10, scale=3, binary_threshold=170)
                    processed_result = self.process_ocr(result=result, x_min=295, x_max=475, y_min=690, y_max=820, y_threshold=10, scale=3, merge=False)

                    for item in processed_result:
                        if "기부" in str(item[0]):
                            x = item[1]
                            y = item[2]
                            self.tap(385,765) # 기부 버튼
                            time.sleep(1)
                            self.back()
                            time.sleep(1)
                            self.back()
                            print(f"adb{self.itr} 연맹 연구 기여 완료")
                            return True
                    else :
                        self.back()
                        time.sleep(1)










    def get_quest(self) :

        for _ in range(20) :

            flag = False

            self.tap(30,790) # 퀘스트 버튼
            time.sleep(1)
            self.screen_shot(name="_quest")

            result = self.get_ocr_raw(file_name="capture_quest.png", x_min=360, x_max=530, y_min=200, y_max=750, y_threshold=10, scale=3)
            processed_result = self.process_ocr(result=result, x_min=360, x_max=530, y_min=200, y_max=750, y_threshold=10, scale=3, merge=True)
            print(processed_result)

            for item in processed_result:
                if item[0] == "수령":
                    x = item[1]
                    y = item[2]
                    self.tap(x,y)
                    time.sleep(1)
                    flag = True
                    break 

            self.back() # 아무것도 수령할거 없는 경우
            time.sleep(1)

            self.check_abnormal()
            time.sleep(1)

            if flag == False:
                break




    def get_people(self) :

        self.tap(470,610)
        time.sleep(1)
        self.screen_shot(name="_people")

        result = self.get_ocr_raw(file_name="capture_people.png", x_min=210, x_max=330, y_min=820, y_max=860, y_threshold=10, scale=1)
        processed_result = self.process_ocr(result=result, x_min=210, x_max=330, y_min=820, y_max=860, y_threshold=10, scale=1, merge=True)

        if processed_result :
            self.tap(270,840)
            time.sleep(5)


    def read_letter(self) :

        self.tap(500,785)
        time.sleep(1)
        self.tap(420,930)
        time.sleep(1)
        self.back()
        time.sleep(1)
        self.back()


    def get_VIP(self) :

        self.tap(490,60)
        time.sleep(2)
        self.tap(470,215)
        time.sleep(2)
        self.back()
        time.sleep(2)
        self.back()






        



    def screen_shot(self, name="") :
        local_name = self._f(f"capture{name}.png")
        dest_path = f"{self.base}\\{local_name}"
        command = f'{self.adb_path} -s {self.device_id} shell screencap -p /sdcard/Pictures/Screenshots/capture{name}.png'
        self.shell(command)
        command = f'{self.adb_path} -s {self.device_id} pull /sdcard/Pictures/Screenshots/capture{name}.png "{dest_path}"'
        self.shell(command)



    def crop_image(self, file_name="capture.png", x_min=0, x_max=480, y_min=0, y_max=1000) :
        img_path = f"{self.base}\\{self._f(file_name)}"
        image = cv2.imread(img_path)
        cropped_image = image[y_min:y_max, x_min:x_max]
        cropped_img_path = f"{self.base}\\{self._f('cropped_' + file_name)}"
        cv2.imwrite(cropped_img_path, cropped_image)
        return cropped_image


    def compare_inout(self, cropped_file_name="cropped_capture_inout.png", in_ref="in.png", out_ref="out.png"):
        """크롭된 이미지가 in.png에 더 가까운지 out.png에 더 가까운지 판단. 'in' 또는 'out' 반환. 참조 이미지는 코드 실행 경로에서 로드."""
        crop = cv2.imread(f"{self.base}\\{self._f(cropped_file_name)}")
        in_img = cv2.imread(in_ref)
        out_img = cv2.imread(out_ref)
        if crop is None:
            raise FileNotFoundError(f"Cropped image not found: {cropped_file_name}")
        if in_img is None or out_img is None:
            raise FileNotFoundError(f"Reference images not found: {in_ref}, {out_ref} (실행 경로: {os.getcwd()})")
        # 크기 맞추기 (참조 이미지 크기에 맞춤)
        h, w = in_img.shape[:2]
        crop = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)
        out_img = cv2.resize(out_img, (w, h), interpolation=cv2.INTER_LINEAR)
        # 유사도: MSE가 작을수록 더 유사
        mse_in = np.mean((crop.astype(float) - in_img.astype(float)) ** 2)
        mse_out = np.mean((crop.astype(float) - out_img.astype(float)) ** 2)
        return "in" if mse_in <= mse_out else "out"

    def matches_reference(self, cropped_file_name, reference_name="reconnect.png", mse_threshold=800):
        """크롭된 이미지가 참조 이미지와 일치하는지 판단. MSE가 threshold 이하면 True. 참조 이미지는 코드 실행 경로에서 로드."""
        crop = cv2.imread(f"{self.base}\\{self._f(cropped_file_name)}")
        ref = cv2.imread(reference_name)
        if crop is None:
            raise FileNotFoundError(f"Cropped image not found: {cropped_file_name}")
        if ref is None:
            raise FileNotFoundError(f"Reference image not found: {reference_name} (실행 경로: {os.getcwd()})")
        h, w = ref.shape[:2]
        crop = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)
        mse = np.mean((crop.astype(float) - ref.astype(float)) ** 2)
        return mse <= mse_threshold

    def check_reconnect(self, mse_threshold=800) :

        self.screen_shot(name="_reconnect")
        self.crop_image(file_name="capture_reconnect.png", x_min=50, x_max=490, y_min=320, y_max=630)
        return self.matches_reference(
            cropped_file_name="cropped_capture_reconnect.png",
            reference_name="reconnect.png",
            mse_threshold=mse_threshold
        )

    def check_help(self, mse_threshold=800) :

        self.screen_shot(name="_help")
        self.crop_image(file_name="capture_help.png", x_min=375, x_max=430, y_min=825, y_max=875)
        return self.matches_reference(
            cropped_file_name="cropped_capture_help.png",
            reference_name="help.png",
            mse_threshold=mse_threshold
        )




    def get_ocr(self, file_name="capture.png", x_min=0, x_max=480, y_min=0, y_max=1000, y_threshold=10):
        img_path = f"{self.base}\\{self._f(file_name)}"
        image = cv2.imread(img_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at path: {img_path}")
        height, width, _ = image.shape
        cropped_image = image[y_min:y_max, x_min:x_max]
        cropped_img_path = f"{self.base}\\{self._f('cropped_' + file_name)}"
        cv2.imwrite(cropped_img_path, cropped_image)
        result = self.ocr.ocr(cropped_img_path, cls=False)

        # print(result)

        if result == [None] : # ocr 텍스트 없음조건
            return [None]

        # 1. 결과를 Y좌표 기준으로 필터링
        lines = []
        for line in result[0]:
            coords = line[0]  # OCR 좌표
            text = line[1][0]  # OCR 텍스트
            x_mean = np.mean([coords[0][0], coords[2][0]])  # X좌표 평균값
            y_mean = np.mean([coords[0][1], coords[2][1]])  # Y좌표 평균값

            # Y좌표 필터링
            lines.append({"x_mean": x_mean, "y_mean": y_mean, "text": text})

        # 2. Y좌표 기준으로 정렬
        lines.sort(key=lambda x: x["y_mean"])

        # 3. Y좌표 차이에 따라 그룹화
        grouped_lines = []
        current_line = []

        for item in lines:
            if not current_line:
                current_line.append(item)
            else:
                # 이전 Y좌표와 비교하여 같은 줄인지 판단
                if abs(item["y_mean"] - current_line[-1]["y_mean"]) <= y_threshold:
                    current_line.append(item)
                else:
                    # X좌표 기준으로 정렬 후 저장
                    grouped_lines.append(sorted(current_line, key=lambda x: x["x_mean"]))
                    current_line = [item]

        # 마지막 줄 추가
        if current_line:
            grouped_lines.append(sorted(current_line, key=lambda x: x["x_mean"]))

        # 4. 결과 출력
        # for line in grouped_lines:
            # print(" ".join([item["text"] for item in line]))

        return grouped_lines
    

    def get_ocr_raw(self, file_name="capture.png", x_min=0, x_max=480, y_min=0, y_max=1000, y_threshold=10, scale=3):
        img_path = f"{self.base}\\{self._f(file_name)}"
        image = cv2.imread(img_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at path: {img_path}")
        cropped_image = image[y_min:y_max, x_min:x_max]
        if scale and scale != 1:
            h, w = cropped_image.shape[:2]
            cropped_image = cv2.resize(cropped_image, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
            cropped_image = cv2.cvtColor(cv2.equalizeHist(gray), cv2.COLOR_GRAY2BGR)
        cropped_img_path = f"{self.base}\\{self._f('cropped_' + file_name)}"
        cv2.imwrite(cropped_img_path, cropped_image)
        result = self.ocr.ocr(cropped_img_path, cls=False)

        return result


    def get_ocr_raw_advanced(
        self,
        file_name="capture.png",
        x_min=0, x_max=480, y_min=0, y_max=1000,
        y_threshold=10,
        scale=3,
        use_clahe=True,
        clahe_clip_limit=2.0,
        clahe_tile_grid_size=(8, 8),
        use_gamma=True,
        gamma=1.2,
        use_binary=True,
        binary_threshold=0,        # 값 
        binary_inv=True           # 글자를 흰색으로 만들고 싶으면 True
    ):
        img_path = f"{self.base}\\{self._f(file_name)}"
        image = cv2.imread(img_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at path: {img_path}")
        cropped_image = image[y_min:y_max, x_min:x_max]
        if scale and scale != 1:
            h, w = cropped_image.shape[:2]
            cropped_image = cv2.resize(cropped_image, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)

        # 1) 그레이 변환
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # 2) CLAHE (선택)
        if use_clahe:
            clahe = cv2.createCLAHE(clipLimit=clahe_clip_limit, tileGridSize=clahe_tile_grid_size)
            gray = clahe.apply(gray)
        else:
            # 기존 equalizeHist 유지하고 싶으면 여기에서 사용
            gray = cv2.equalizeHist(gray)

        # 3) 감마 보정 (선택)
        if use_gamma and gamma != 1.0:
            inv_gamma = 1.0 / gamma
            table = (np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)])
                    .astype("uint8"))
            gray = cv2.LUT(gray, table)

        # 4) 이진화 (선택) – 글자를 확실히 흰색/배경 검정으로
        if use_binary:
            if binary_threshold == 0:
                # OTSU 자동 임계값
                thresh_type = cv2.THRESH_BINARY_INV if binary_inv else cv2.THRESH_BINARY
                _, gray = cv2.threshold(gray, 0, 255, thresh_type + cv2.THRESH_OTSU)
            else:
                thresh_type = cv2.THRESH_BINARY_INV if binary_inv else cv2.THRESH_BINARY
                _, gray = cv2.threshold(gray, binary_threshold, 255, thresh_type)

        cropped_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        cropped_img_path = f"{self.base}\\{self._f('cropped_' + file_name)}"
        cv2.imwrite(cropped_img_path, cropped_image)
        result = self.ocr.ocr(cropped_img_path, cls=False)

        return result
    

    def process_ocr(self, result, x_min=0, x_max=480, y_min=0, y_max=1000, y_threshold=10, scale=1, merge=True):
        if result is None or result == [None] or result[0] is None:
            return []
        processed_lines = []

        for block in result[0]:
            coords = block[0]
            text = block[1][0]
            confidence = block[1][1]  # 인식률

            # 업스케일된 이미지로 OCR한 경우: scale로 나눈 뒤 원본 기준으로 보정
            x_coords = [point[0] / scale + x_min for point in coords]
            y_coords = [point[1] / scale + y_min for point in coords]

            x_mean = np.mean(x_coords)
            y_mean = np.mean(y_coords)

            # 각 영역의 x 최소/최대와 y 최소/최대 계산
            x_left = min(x_coords)
            x_right = max(x_coords)
            y_top = min(y_coords)
            y_bottom = max(y_coords)

            processed_lines.append({
                "text": text,
                "x_mean": x_mean,
                "y_mean": y_mean,
                "x_left": x_left,
                "x_right": x_right,
                "y_top": y_top,
                "y_bottom": y_bottom,
                "confidence": confidence
            })

        # Y좌표 기준으로 정렬
        processed_lines.sort(key=lambda x: x["y_mean"])

        # mod=False: 병합 없이 블록 단위로 반환
        if not merge:
            return [[item["text"], item["x_mean"], item["y_mean"],
                     item["x_left"], item["x_right"], item["y_top"], item["y_bottom"],
                     item["confidence"]] for item in processed_lines]

        # 같은 줄 텍스트 병합 (mod=True, 기본)
        grouped_lines = []
        current_line = []

        for item in processed_lines:
            if not current_line:
                current_line.append(item)
            else:
                # 같은 줄인지 확인 (y_threshold 기준)
                if abs(item["y_mean"] - current_line[-1]["y_mean"]) <= y_threshold:
                    current_line.append(item)
                else:
                    # 병합 후 저장 (X좌표 기준으로 정렬)
                    grouped_lines.append(sorted(current_line, key=lambda x: x["x_mean"]))
                    current_line = [item]

        if current_line:
            grouped_lines.append(sorted(current_line, key=lambda x: x["x_mean"]))

        # 병합된 결과 처리
        final_output = []
        for group in grouped_lines:
            merged_text = " ".join([item["text"] for item in group])
            x_mean = np.mean([item["x_mean"] for item in group])
            y_mean = np.mean([item["y_mean"] for item in group])
            x_left = min([item["x_left"] for item in group])
            x_right = max([item["x_right"] for item in group])
            y_top = min([item["y_top"] for item in group])
            y_bottom = max([item["y_bottom"] for item in group])
            confidence = np.mean([item["confidence"] for item in group])

            final_output.append([merged_text, x_mean, y_mean, x_left, x_right, y_top, y_bottom, confidence])

        return final_output


    def ocr_to_plain(self, ocr) :

        result_text = ""

        for line in ocr:
            # 각 줄의 텍스트를 공백으로 연결하고 줄바꿈 추가
            line_text = " ".join([item["text"] for item in line])
            result_text += line_text + "\n"

        # 마지막 줄바꿈 제거
        result_text = result_text.strip()

        return result_text    



    def check_abnormal(self) :

        itr = 0

        while True :

            # 비정상 화면 해결
            state = self.get_state()
            if state["action"] == False :
                itr = itr + 1
                break
            time.sleep(1)

        if itr == 0 : # abnormal 없음
            return False
        else : 
            return True


        
            

    


    

def init_bluestacks_and_adbs():
    """
    BlueStacks 인스턴스 실행 + ADB 객체 초기화 + 킹샷 앱 실행.

    반환값:
        adbs (list[ADB]): 초기화된 ADB 인스턴스 리스트
        success (bool): kingshot이 정상 실행됐다고 판단하면 True,
                        아니라면 False (추후 OCR 로직으로 판단 예정)
    """
    print("시작!")

    # BlueStacks 인스턴스 실행
    commands = [
        # [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_1"],  # 5555
        [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_12"],
        [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_13"],
        [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_14"],
        [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_15"],
        # [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_7"],
        [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_8"],
        # [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_9"],
        # [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_10"],
        # [r"C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe", "--instance", "Pie64_11"],
    ]

    processes = []
    for cmd in commands:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)
        time.sleep(3)  # 명령 실행 간 지연 시간 추가

    time.sleep(10)

    # ADB 연결 및 kingshot 실행
    adbs = []
    # adbs.append(ADB(port=5555))
    adbs.append(ADB(port=5675))
    adbs.append(ADB(port=5685))
    adbs.append(ADB(port=5695))
    adbs.append(ADB(port=5705))
    # adbs.append(ADB(port=5625))
    adbs.append(ADB(port=5635))
    # adbs.append(ADB(port=5645))
    # adbs.append(ADB(port=5655))
    # adbs.append(ADB(port=5665))

    for adb in adbs:
        adb.connect()

    for adb in adbs:
        adb.home()

    time.sleep(3)

    for adb in adbs:
        adb.start_kingshot()
        time.sleep(1)

    time.sleep(15)

    success = True

    # 어플리케이션 정상 실행 여부 판단
    for iteration, adb in enumerate(adbs):
        adb.screen_shot(name="_initialize")
        result = adb.get_ocr_raw(file_name="capture_initialize.png", x_min=0, x_max=540, y_min=0, y_max=960, y_threshold=10, scale=1)
        processed_result = adb.process_ocr(result=result, x_min=0, x_max=540, y_min=0, y_max=960, y_threshold=10, scale=1, merge=False)
        result = adb.has_keywords(processed_result, ["Store", "store", "시스템"], min_count=2)

        if processed_result == [] :
            result = True

        if result:
            print(f"adb{iteration}에서 실행 실패 감지")
            success = False
        time.sleep(1)

    # 실행 실패 시 BlueStacks 프로세스 종료 (Popen + taskkill로 실제 엔진까지 확실히 종료)
    if not success:
        print("실행 실패: BlueStacks 프로세스 종료 중...")
        # 1) Popen으로 띄운 프로세스 종료 시도
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
            except Exception as e:
                print(f"Popen 프로세스 종료 중 오류: {e}")
        # 2) Windows taskkill로 BlueStacks 관련 프로세스 강제 종료 (런처가 남긴 실제 엔진까지 처리)
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

    return adbs, success

# 초기화 실행: 실패 시 전체 파이썬 프로세스 종료
adbs, _init_success = init_bluestacks_and_adbs()
if not _init_success:
    import sys
    sys.exit(1)



from concurrent.futures import ThreadPoolExecutor, as_completed


time.sleep(10)

timer = time.time() - 15 * 60 # 철수 원하면 3으로
back_timer = time.time()
back_trigger = False

# 각 adb별로 루프 카운트 (adb마다 5번 돌면 자원 채취)
loop_count = {}


def check_exception_case(adb) :

    check_resource = adb.msg_check(msg="오프라인", x_min=190, x_max=350, y_min=170, y_max=205, y_threshold=10, scale=3)
    if check_resource == True :
        adb.back()
        time.sleep(3)

    check_resource = adb.msg_check(msg="패키지", x_min=60, x_max=430, y_min=60, y_max=105, y_threshold=10, scale=3)
    if check_resource == True :
        adb.back()
        time.sleep(3)

    check_resource = adb.msg_check(msg="이정표", x_min=65, x_max=150, y_min=5, y_max=50, y_threshold=10, scale=3)
    if check_resource == True :
        adb.back()
        time.sleep(3)


def check_abnormal(adb) :

    while True :

        # 비정상 화면 해결
        state = adb.get_state()
        if state["action"] == False :
            break
        time.sleep(1)



def run_one_adb(itr, adb):
    """한 디바이스에 대한 작업 (병렬 실행용). 에러 시 로그만 하고 넘어감."""
    try:
        print(f"adb{itr} 시작")

        adb.itr = itr

        # 튕겼는지 체크

        adb.screen_shot(name="_initialize")
        result = adb.get_ocr_raw(file_name="capture_initialize.png", x_min=0, x_max=540, y_min=0, y_max=960, y_threshold=10, scale=1)
        processed_result = adb.process_ocr(result=result, x_min=0, x_max=540, y_min=0, y_max=960, y_threshold=10, scale=1, merge=False)
        result = adb.has_keywords(processed_result, ["Store", "store", "시스템"], min_count=2)

        if result :
            adb.start_kingshot()
            time.sleep(5)

        # reconnet 창이 떠있는지 확인
        reconnect_check = adb.check_reconnect()
        reconnect_check 


        if reconnect_check == True :
            print("reconnection")
        elif reconnect_check == False :


            
            check_abnormal(adb)

            
            check_exception_case(adb)


            if loop_count.get(itr, 0) == 0 :

                adb.get_people()
                time.sleep(1)

                check_abnormal(adb)
                adb.read_letter()
                time.sleep(1)

                check_abnormal(adb)
                adb.get_VIP()
                time.sleep(1)

                check_abnormal(adb)
                adb.get_money()
                time.sleep(1)

            

            




            # 현재 위치 판단 (예외처리)
            check_abnormal(adb)

            adb.screen_shot(name="_inout")
            adb.crop_image(file_name="capture_inout.png", x_min=465, x_max=505, y_min=930, y_max=955)
            result = adb.compare_inout(cropped_file_name="cropped_capture_inout.png")  # "in" 또는 "out"

            if result == "in" : # in 버튼이 뜨는 경우 (밖에 있는 경우)
                adb.tap(490,910) # 안으로 들어오기
                time.sleep(10)

            if adb.check_help() == True :
                adb.tap(400,820) # 연맹 도움
                time.sleep(1)




            state = adb.state_check()
            [build1, build2, unit1, unit2, unit3, research] = [3, 3, 3, 3, 3, 3]
            queue_check = False
            if state is not False :
                [build1, build2, unit1, unit2, unit3, research] = state[0]
                queue_check = any(str(x) == "0" for x in state[1])
                print(f"adb{itr} : {state[0]}")
                print(f"adb{itr} : {state[1]}")
                print(f"adb{itr} : {queue_check}")

                if queue_check == True :
                    stamina = adb.get_stamina()



            # build1, build2, unit1, unit2, unit3, research = adb.state_check()
            # print(f"adb{itr}", build1, build2, unit1, unit2, unit3, research)

            # queue_check = adb.state_check2()
            # if queue_check == True :
            #     time.sleep(1)
            #     stamina = adb.get_stamina()

            
            # check_exception_case(adb)
            # time.sleep(1)
            check_abnormal(adb)

            if unit1 == 2 :
                adb.get_unit(type="보병")
                time.sleep(1)
                # print("보병 훈련 완료")
            if unit2 == 2 :
                adb.get_unit(type="기병")
                time.sleep(1)
                # print("기병 훈련 완료")
            if unit3 == 2 :
                adb.get_unit(type="궁병")
                time.sleep(1)
                # print("궁병 훈련 완료")


            # check_exception_case(adb)
            # time.sleep(1)
            check_abnormal(adb)


            if adb.check_help() == True :
                adb.tap(400,820) # 연맹 도움
                time.sleep(1)

            if build1 == 1 :
                adb.build_city_new(building=1)
                time.sleep(1)
                # print("건물 1 건설 시작")
            if build2 == 1 :
                adb.build_city_new(building=2)
                time.sleep(1)
                print("건물 2 건설 시작")


            # check_exception_case(adb)
            # time.sleep(1)
            check_abnormal(adb)


            if unit1 in (1, 2) or unit2 in (1, 2) or unit3 in (1, 2):

                check_exception_case(adb)
                if adb.check_help() == True :
                    adb.tap(400,820) # 연맹 도움
                    time.sleep(1)


                if unit1 == 1 :
                    adb.unit_training(unit="보병")
                    time.sleep(1)
                    # print("보병 훈련 시작")
                if unit2 == 1 :
                    adb.unit_training(unit="기병")
                    time.sleep(1)
                    # print("기병 훈련 시작")
                if unit3 == 1 :
                    adb.unit_training(unit="궁병")
                    time.sleep(1)
                    # print("궁병 훈련 시작")


            check_abnormal(adb)
            if adb.check_help() == True :
                adb.tap(400,820) # 연맹 도움
                time.sleep(1)

            if research == 1 :
                adb.research()
                time.sleep(1)

            
            check_abnormal(adb)
            if adb.check_help() == True :
                adb.tap(400,820) # 연맹 도움
                time.sleep(1)


            adb.union_research()
            time.sleep(1)



            # 자원 채취
            if queue_check == True :

                if reconnect_check == True :
                    adb.tap(380,595) # reconnect
                    time.sleep(10)

                check_exception_case(adb)

                check_abnormal(adb)

                # adb.get_money()
                # time.sleep(1)

                # 현재 위치 판단
                adb.screen_shot(name="_inout")
                adb.crop_image(file_name="capture_inout.png", x_min=465, x_max=505, y_min=930, y_max=955)
                result = adb.compare_inout(cropped_file_name="cropped_capture_inout.png")  # "in" 또는 "out"

                if result == "out" : # out 버튼이 뜨는 경우 (도시 안에 있는 경우)
                    adb.tap(490,910) # 야외로 나가기
                    time.sleep(10)


                    if stamina > 50 : # 사냥
                        adb.hunting()

        
                    else : # 자원 채취취
                        bread_value, wood_value, stone_value, iron_value = adb.resource_remain()
                        print(f"adb{itr} : {bread_value/1e+6}, {wood_value/1e+6}, {stone_value/1e+6}, {iron_value/1e+6}")
                        stone_value = stone_value * 5
                        iron_value = iron_value * 20

                        time.sleep(3)


                        resource_list = [bread_value, wood_value, stone_value, iron_value]
                        
                        # 이미 수집 중인 자원은 배제
                        if "빵" in state[1] :
                            resource_list.remove(bread_value)
                        elif "목재" in state[1] :
                            resource_list.remove(wood_value)
                        elif "석재" in state[1] :
                            resource_list.remove(stone_value)
                        elif "철광" in state[1] :
                            resource_list.remove(iron_value)

                        if resource_list == [] :
                            resource_list = [bread_value, wood_value, stone_value, iron_value]


                        min_value = min(resource_list)

                        if min_value == bread_value:
                            resource = "빵"
                        elif min_value == wood_value:
                            resource = "목재"
                        elif min_value == stone_value:
                            resource = "석재"
                        else:
                            resource = "철광"

                        while True :
                            # 비정상 화면 해결
                            state = adb.get_state()
                            if state["action"] == False :
                                break
                            time.sleep(1)

                        result = adb.resource_farming(resource=resource)


                    time.sleep(1)     

                    adb.tap(490,910) # 도시로 돌아가기  

                    time.sleep(5)

                    check_abnormal(adb)
                    time.sleep(1)

                    adb.read_letter()
                    time.sleep(1)

                    check_abnormal(adb)
                    time.sleep(1)

                    adb.get_quest()
                    time.sleep(1)

                


                


        





        # # 각 adb 루프가 5번 돌면 한 번 자원 채취
        # if loop_count.get(itr, 0) % 10 == 0 :

        #     if reconnect_check == True :
        #         adb.tap(380,595) # reconnect
        #         time.sleep(10)

        #     check_exception_case(adb)

        #     check_abnormal(adb)

        #     # adb.get_money()
        #     # time.sleep(1)

        #     # 현재 위치 판단
        #     adb.screen_shot(name="_inout")
        #     adb.crop_image(file_name="capture_inout.png", x_min=465, x_max=505, y_min=930, y_max=955)
        #     result = adb.compare_inout(cropped_file_name="cropped_capture_inout.png")  # "in" 또는 "out"

        #     if result == "out" : # out 버튼이 뜨는 경우 (도시 안에 있는 경우)
        #         adb.tap(490,910) # 야외로 나가기
        #         time.sleep(10)


        #     bread_value, wood_value, stone_value, iron_value = adb.resource_remain()
        #     print(f"adb{itr} : {bread_value/1e+6}, {wood_value/1e+6}, {stone_value/1e+6}, {iron_value/1e+6}")
        #     stone_value = stone_value * 5
        #     iron_value = iron_value * 20

        #     time.sleep(3)

        #     for i in range(3):  # 루프 6번까지만 돌게
        #         # 네 자원 값 중 가장 낮은 값 기준으로 리소스 이름 선택
        #         min_value = min(bread_value, wood_value, stone_value, iron_value)

        #         if min_value == bread_value:
        #             resource = "빵"
        #         elif min_value == wood_value:
        #             resource = "목재"
        #         elif min_value == stone_value:
        #             resource = "석재"
        #         else:
        #             resource = "철광"

        #         while True :
        #             # 비정상 화면 해결
        #             state = adb.get_state()
        #             if state["action"] == False :
        #                 break
        #             time.sleep(1)

        #         result = adb.resource_farming(resource=resource)
        #         if result == False:  # 잔여 칸 없는 경우 break
        #             break
        #         time.sleep(1)

        #     adb.tap(490,910) # 도시로 돌아가기

        #     if isinstance(adbs, list) and len(adbs) == 1:
        #         time.sleep(10)

        #     # timer = time.time()


        if loop_count.get(itr, 0) % 30 == 0 :

            print(f"adb{itr} loop 30 진입")

            if reconnect_check == True :
                adb.tap(380,595) # reconnect
                time.sleep(10)


            check_abnormal(adb)

            check_exception_case(adb)

            adb.get_hero()
            time.sleep(1)

            check_abnormal(adb)

            adb.get_supply()
            time.sleep(1)

            





        # 이 adb의 루프 카운트 +1 (각자 따로 돔)
        loop_count[itr] = loop_count.get(itr, 0) + 1

    except Exception as e:
        print(f"adb{itr} 오류: {e}")
        traceback.print_exc()


import threading

def adb_worker(itr, adb):
    """한 디바이스 전용 무한 루프. 다른 adb와 무관하게 독립 동작."""
    while True:
        try:
            run_one_adb(itr, adb)
        except Exception as e:
            print(f"adb{itr} 루프 예외: {e}")
            traceback.print_exc()
        time.sleep(1)

threads = []
for itr, adb in enumerate(adbs):
    t = threading.Thread(target=adb_worker, args=(itr, adb))
    t.start()
    threads.append(t)
    print(f"adb{itr} 스레드 시작 (독립 루프)")

# 메인은 스레드들이 돌아가도록 대기만 함 (종료 시까지)
for t in threads:
    t.join()
