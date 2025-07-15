import serial
import time

# 시리얼 포트 설정
port = '/dev/tty.usbserial-110'  # 사용 중인 포트 확인 후 변경  # 하나는 110 , 하나는 140
baudrate = 115200  # 보드레이트 설정

try:
    # 시리얼 포트 열기
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"시리얼 포트 {port}에 연결됨")

        # 포트가 열릴 때까지 대기 (안정화)
        time.sleep(2)

        def send_command(command):
            """G-code 명령을 보내고 응답을 읽는 함수"""
            command_str = command + '\r\n'  # G-code 끝에 줄바꿈 추가
            ser.write(command_str.encode())  # 바이트로 변환 후 전송
            time.sleep(0.5)  # 응답 대기
            response = ser.readline().decode().strip()
            print(f"응답: {response}")

        # 홈 포지션 이동 테스트
        
        send_command("$h")

except serial.SerialException as e:
    print(f"시리얼 포트 에러: {e}")
except Exception as e:
    print(f"예상치 못한 에러: {e}")
