import chess
import chess.engine
import time
import serial

class RobotArmController:
    def __init__(self, name, port, baudrate=115200):
        self.name = name
        self.port = port
        self.baudrate = baudrate
        self.ser = None

        self.x_limit = (-120, 160)
        self.y_limit = (-40, 100)
        self.z_limit = (-100, 60)

        # ⛳ 체스 좌표 매핑 (직접 입력)
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
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(2)
        self.ser.flushInput()
        print(f"🤖 [{self.name}] 연결됨 (port: {self.port})")

    def send_command(self, command):
        if self.ser is None or not self.ser.is_open:
            print(f"⚠️ [{self.name}] 시리얼 포트가 닫혀 있음")
            return None
        self.ser.write((command + '\r\n').encode())
        time.sleep(0.3)
        response = self.ser.readline().decode().strip()
        print(f"[{self.name}] 📡 {command} → {response}")
        return response

    def move_to(self, x=0, y=0, z=0, A=0, B=0, C=0):
        x = min(max(self.x_limit[0], x), self.x_limit[1])
        y = min(max(self.y_limit[0], y), self.y_limit[1])
        z = min(max(self.z_limit[0], z), self.z_limit[1])
        self.send_command("G90")
        self.send_command(f"G0 X{x} Y{y} Z{z} A{A} B{B} C{C}")

    def pump(self, g):
        self.send_command(f"M3 S{g}")

    def chess_move(self, start, target):
        if start not in self.chess_positions or target not in self.chess_positions:
            print(f"⚠️ {start} 또는 {target} 좌표가 정의되지 않음!")
            return

        x1, y1, z1, A1, B1, C1 = self.chess_positions[start]
        x2, y2, z2, A2, B2, C2 = self.chess_positions[target]

        self.move_to(x1, -60, z1, A1, -10, C1)
        self.move_to(x1, y1, z1, A1, B1, C1)
        time.sleep(1)

        self.pump(500)
        time.sleep(2)

        self.move_to(x1, -60, z1, A1, -10, C1)
        time.sleep(1)

        self.move_to(x2, -60, z2, A2, -10, C2)
        time.sleep(1)

        self.move_to(x2, y2, z2, A2, B2, C2)
        time.sleep(1)

        self.pump(0)
        time.sleep(2)

        self.move_to(x2, -60, z2, A2, -10, C2)
        print(f"♟️ [{self.name}] 체스말 이동: {start} → {target}")
    

def convert_square_to_rc(square):
    col = ord(square[0]) - ord('a') + 1
    row = int(square[1])
    return (row, col)

def main():
    stockfish_path = "/opt/homebrew/bin/stockfish"
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    board = chess.Board()

    robot1 = RobotArmController("WHITE", port='/dev/tty.usbserial-110')
    #robot2 = RobotArmController("BLACK", port='/dev/tty.usbserial-140')

    robot1.connect()
    #robot2.connect()

    print("♟️ 체스 대결 시작!\n", board)

    while not board.is_game_over():
        input("⏎ 엔터를 눌러 다음 수 진행...")

        move = engine.play(board, chess.engine.Limit(time=0.1)).move
        from_sq = move.uci()[:2]
        to_sq = move.uci()[2:]
        from_rc = convert_square_to_rc(from_sq)
        to_rc = convert_square_to_rc(to_sq)

        print(f"\n👉 수: {move.uci().upper()} | {from_rc} → {to_rc}")

        if board.turn == chess.WHITE:
            robot1.chess_move(from_rc, to_rc)
        else:
            # robot2는 문자로만 표시
            flipped_from = (9 - from_rc[0], from_rc[1])
            flipped_to = (9 - to_rc[0], to_rc[1])
            print(f"📋 [BLACK 수동 조작 필요] 위치: {flipped_from} → {flipped_to}")

        board.push(move)
        print(board)

    print("🏁 게임 종료! 결과:", board.result())
    engine.quit()

if __name__ == "__main__":
    main()