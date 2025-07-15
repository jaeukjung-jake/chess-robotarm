import wlkatapython
import serial
import time

# 시리얼 포트 설정
ser = serial.Serial('COM6', 115200)
time.sleep(2)  # 2초 대기

# Mirobot 객체 생성 및 초기화
mirobot = wlkatapython.Mirobot_UART()
mirobot.init(ser, -1)  # -1은 기본 주소를 의미합니다.

# 로봇 팔을 홈 위치로 이동4
mirobot.homing()

print('end')

# 시리얼 포트 닫기
ser.close()


# e4 = wlkatapython.E4_UART()
# e4.init(serial.Serial('COM13', 115200), -1)
# e4.homing()

# mt4 = wlkatapython.MT4_UART()
# mt4.init(serial.Serial('COM13', 115200), -1)
# mt4.homing()

# ms4220 = wlkatapython.MS4220_UART()
# ms4220.init(serial.Serial('COM13', 38400), 10)
# ms4220.speed(100)

