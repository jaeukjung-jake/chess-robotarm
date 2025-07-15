import serial
import time

class RobotArmController:
    """WLKATA Mirobot을 제어하는 클래스 (8x8 체스판에 맞게 조정)"""
    
    def __init__(self, port='/dev/tty.usbserial-110', baudrate=115200, timeout=1):
        """시리얼 포트를 초기화하는 생성자"""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None  # 시리얼 객체 초기화
        
        # 체스판 기준점 (1,1) = (-10, 40, 20)
        self.square_size = 5  # 한 칸 크기 (mm)
        self.x_min, self.y_min, self.z_ref = -10, 40, 20  # 체스판 (1,1) 기준점

        # 로봇팔 이동 한계
        self.x_limit = (-120, 160)  # X축 제한 (°)
        self.y_limit = (-40, 100)  # Y축 제한 (°)
        self.z_limit = (-100, 60)  # Z축 제한 (°)

         # (1,1) ~ (1,8)까지의 체스 좌표
        self.chess_positions = {
            (1, 1): (-50, -5, 50, 0, -55, 0),
            (1, 2): (-40, -10, 55, 0, -50, 0),
            (1, 3): (-28, -15, 60, 0, -40, 0),
            (1, 4): (-15, -12, 60, 0, -40, 0),
            (1, 5): (-3, -10, 60, 0, -40, 0),
            (1, 6): (10, -10, 60, 0, -45, 0),
            (1, 7): (22, -15, 60, 0, -50, 0),
            (1, 8): (30, 0, 48, 0, -50, 0),

            (2, 1): (-42, 10, 35, 0, -45, 0),
            (2, 2): (-34, 10, 37, 0, -45, 0),  # X 증가, Z는 약간 높이 유지
            (2, 3): (-25, 10, 40, 0, -45, 0),  # X 증가, Z 증가
            (2, 4): (-15, 10, 40, 0, -45, 0),  # X 증가, Z 유지
            (2, 5): (-5, 0, 47, 0, -45, 0),   # X 증가, Z 유지
            (2, 6): (7, 0, 47, 0, -45, 0),    # X 증가, Z 유지
            (2, 7): (18, 10, 38, 0, -45, 0),   # X 증가, Z 감소
            (2, 8): (26, 10, 35, 0, -45, 0),    # 이미 주어진 값

            (3, 1): (-38, 20, 20, 0, -45, 0),
            (3, 2): (-30, 20, 22, 0, -45, 0),  # X 증가, Z 증가
            (3, 3): (-22, 20, 24, 0, -45, 0),  # X 증가, Z 증가
            (3, 4): (-12, 20, 24, 0, -45, 0),  # X 증가, Z 유지
            (3, 5): (-3, 10, 35, 0, -45, 0),   # X 증가, Z 유지
            (3, 6): (6, 10, 35, 0, -55, 0),    # X 증가, Z 감소
            (3, 7): (13, 15, 30, 0, -50, 0),   # X 증가, Z 감소
            (3, 8): (22, 20, 20, 0, -45, 0),

            
            (4, 1): (-34, 25, 10, 0, -45, 0),
            (4, 2): (-28, 25, 12, 0, -45, 0),  # X 증가, Z 증가
            (4, 3): (-20, 25, 15, 0, -45, 0),  # X 증가, Z 증가
            (4, 4): (-12, 25, 15, 0, -45, 0),  # X 증가, Z 유지
            (4, 5): (-5, 25, 15, 0, -45, 0),   # X 증가, Z 유지
            (4, 6): (4, 30, 10, 0, -45, 0),    # X 증가, Z 감소
            (4, 7): (12, 30, 8, 0, -45, 0),    # X 증가, Z 감소
            (4, 8): (18, 30, 5, 0, -40, 0),    # 이미 주어진 값

            (5, 1): (-30, 40, -12, 0, -35, 0),
            (5, 2): (-25, 40, -10, 0, -35, 0),  # X 증가, Z 증가
            (5, 3): (-18, 40, -8, 0, -35, 0),  # X 증가, Z 증가
            (5, 4): (-10, 40, -8, 0, -35, 0),  # X 증가, Z 유지
            (5, 5): (-3, 40, -8, 0, -35, 0),   # X 증가, Z 유지
            (5, 6): (5, 45, -10, 0, -35, 0),   # X 증가, Z 감소
            (5, 7): (10, 45, -12, 0, -40, 0),  # X 증가, Z 감소
            (5, 8): (14, 45, -15, 0, -40, 0),

            (6, 1): (-28, 58, -40, 0, -25, 0),
            (6, 2): (-24, 58, -40, 0, -25, 0),  # X 증가, Z 유지
            (6, 3): (-18, 58, -40, 0, -25, 0),  # X 증가, Z 유지
            (6, 4): (-10, 58, -40, 0, -25, 0),  # X 증가, Z 유지
            (6, 5): (-4, 58, -40, 0, -25, 0),   # X 증가, Z 유지
            (6, 6): (3, 60, -40, 0, -30, 0),    # X 증가, Z 유지
            (6, 7): (8, 60, -40, 0, -30, 0),    # X 증가, Z 유지
            (6, 8): (13, 60, -40, 0, -30, 0),    # 이미 주어진 값

            (7, 1): (-26, 70, -55, 0, -40, 0),
            (7, 2): (-22, 70, -55, 0, -40, 0),  # X 증가, Z 유지
            (7, 3): (-17, 70, -55, 0, -40, 0),  # X 증가, Z 유지
            (7, 4): (-10, 70, -55, 0, -40, 0),  # X 증가, Z 유지
            (7, 5): (-4, 70, -55, 0, -40, 0),   # X 증가, Z 유지
            (7, 6): (1, 70, -55, 0, -40, 0),    # X 증가, Z 유지
            (7, 7): (6, 70, -55, 0, -40, 0),    # X 증가, Z 유지
            (7, 8): (10, 70, -55, 0, -40, 0) 

        }


    def connect(self):
        """시리얼 포트 연결"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # 포트 안정화 대기
            self.ser.flushInput()  # 이전 데이터 제거
            print(f"✅ {self.port} 포트에 연결됨!")
        except serial.SerialException as e:
            print(f"⚠️ 시리얼 포트 에러: {e}")

    def send_command(self, command):
        """G-code 명령을 보내고 응답을 읽는 함수"""
        if self.ser is None or not self.ser.is_open:
            print("⚠️ 시리얼 포트가 열려 있지 않습니다. 먼저 `connect()`를 실행하세요.")
            return None

        command_str = command + '\r\n'  # G-code 끝에 줄바꿈 추가
        print(f"📡 [전송] {command_str.strip()}")
        self.ser.write(command_str.encode())  # 바이트로 변환 후 전송
        time.sleep(0.5)  # 응답 대기

        response = self.ser.readline().decode().strip()
        print(f"📡 [응답] {response}")
        return response  # 응답 반환

    def move_to(self, x=0, y=0, z=0, A=0, B=0, C=0):
        """로봇팔을 지정된 X, Y, Z 위치로 이동"""
        # 제한 범위를 초과하지 않도록 값 조정
        x = min(max(self.x_limit[0], x), self.x_limit[1])
        y = min(max(self.y_limit[0], y), self.y_limit[1])
        z = min(max(self.z_limit[0], z), self.z_limit[1])

        self.send_command("G90")  # 절대 좌표 모드 설정
        self.send_command(f"G0 X{x} Y{y} Z{z} A{A} B{B} C{C}")

    def chess_to_xyz(self, row, col):
        """
        (row, col) 체스 좌표를 로봇팔 X, Y, Z 좌표로 변환.
        """
        x = self.x_min + (col - 1) * self.square_size  # X 좌표 변환
        y = self.y_min + (row - 1) * self.square_size  # Y 좌표 변환
        z = self.z_ref - ((row - 1) * self.square_size)  # Z 좌표 변환
        return (x, y, z)

    def gripper(self, g):
        """로봇팔 그리퍼 각도 작동 (30~60)"""
        self.send_command(f"M3 S{g}")

    def close(self):
        """시리얼 포트 닫기"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 시리얼 포트가 닫혔습니다.")

    def pump(self,g):
        """펌프 작동 1000, 500, 0"""
        self.send_command(f"m3 s{g}")

    def chess_move(self, start, target):
        """
        체스판에서 체스말을 이동하는 함수
        :param start: (row, col) 말이 있는 위치
        :param target: (row, col) 이동할 위치
        """
        if start not in self.chess_positions or target not in self.chess_positions:
            print(f"⚠️ {start} 또는 {target} 좌표가 정의되지 않음!")
            return

        x1, y1, z1, A1, B1, C1 = self.chess_positions[start]
        x2, y2, z2, A2, B2, C2 = self.chess_positions[target]

        # 1️⃣ 출발 위치로 이동
        self.move_to(x1,-60,z1,A1,-10,C1)
        self.move_to(x1, y1, z1, A1, B1, C1)
        time.sleep(1)

        # 2️⃣ 체스말 집기
        self.pump(500)
        time.sleep(2)

        # 3️⃣ Y, B 축을 조정하여 수직 상승 (Y=-50, B=-10)
        self.move_to(x1, -60, z1, A1, -10, C1)
        time.sleep(1)

        # 4️⃣ 목표 위치로 이동
        self.move_to(x2, -60, z2, A2, -10, C2)
        time.sleep(1)

        # 5️⃣ 목표 위치에서 Y, B 축을 조정하여 수직 하강
        self.move_to(x2, y2, z2, A2, B2, C2)
        time.sleep(1)

        # 6️⃣ 체스말 놓기
        self.pump(0)
        time.sleep(2)

        self.move_to(x2,-60,z2,A2,-10,C2)

        print(f"♟️ 체스말 이동 완료: {start} → {target}")



if __name__ == "__main__":
    robot = RobotArmController(port='/dev/tty.usbserial-110', baudrate=115200)
    robot.connect()


    #robot.move_to(-50, -5, 50, 0, -55, 0)
    robot.move_to(22, -15, 60, 0, -50, 0)
    
    #robot.chess_move((1,7),(3,6))

    # 6행 미세 조정 후 7행 끝

    robot.close()
