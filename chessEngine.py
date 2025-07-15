import chess
import chess.engine

def convert_square_to_rc(square):
    col = ord(square[0]) - ord('a') + 1
    row = 8 - int(square[1]) + 1
    return (row, col)

class RobotArmController:
    def __init__(self, name, port, baudrate=115200):
        self.name = name
        self.port = port
        self.baudrate = baudrate
        self.connected = False

    def connect(self):
        print(f"🤖 [{self.name}] 연결됨 (port: {self.port})")
        self.connected = True

    def print_move(self, move):
        from_sq = move.uci()[:2]
        to_sq = move.uci()[2:]
        from_rc = convert_square_to_rc(from_sq)
        to_rc = convert_square_to_rc(to_sq)
        print(f"👉 [{self.name}] 수: {move.uci().upper()} | {from_sq}({from_rc}) → {to_sq}({to_rc})")

def main():
    # 엔진 경로 수정 필요할 수 있음
    stockfish_path = "/opt/homebrew/bin/stockfish"

    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    board = chess.Board()

    # 로봇 2대 연결
    robot1 = RobotArmController("WHITE", port='/dev/tty.usbserial-110')
    robot2 = RobotArmController("BLACK", port='/dev/tty.usbserial-111')

    robot1.connect()
    robot2.connect()

    print("♟️ 체스 대결 시작!")
    print(board)

    while not board.is_game_over():
        input("⏎ 엔터를 눌러 다음 수 진행...")

        move = engine.play(board, chess.engine.Limit(time=0.1)).move

        if board.turn == chess.WHITE:
            robot1.print_move(move)
        else:
            robot2.print_move(move)

        board.push(move)
        print(board)

    print("🏁 게임 종료")
    print("결과:", board.result())
    engine.quit()

if __name__ == "__main__":
    main()
    
