# Arduino-Based Robotic Arm Chess System

## 📌 Project Overview
This project is an **automated chess-playing robotic arm system** built using **WLKATA Mirobot**, **Arduino**, and the **Stockfish chess engine**.  
The robotic arm physically moves pieces on a real chessboard based on AI-calculated moves.  
Through coordinate-based control and serial communication, the robot can both move and capture pieces automatically.

## 🚀 Key Features
- **Stockfish Integration**: Uses AI to calculate the next best move
- **Coordinate-Based Control**: Translates chessboard positions into precise robotic movements
- **Piece Capturing & Placement**: Automatically removes opponent pieces and places the player's piece
- **Auto & Manual Modes**: Supports both AI-driven autonomous moves and user-controlled operations
- **Serial Communication**: Commands are sent from Python to Arduino, which controls the robotic arm

## System Architecture
[User Input / AI]

↓

[Python Controller (with Stockfish)]

↓ (Serial Communication)

[Arduino Controller]

↓

[WLKATA Mirobot (Robotic Arm)]

## Project Structure
ChessRobot.py

## How to Run

### 1. Upload Arduino Code
- Install the Arduino IDE: [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)  
- Open `arduino/robot_arm.ino`  
- Select the correct port and upload to your Arduino board

### 2. Run Python Controller
- Install Python 3.x
- Install required packages:
  ```bash
  pip install pyserial stockfish

  python ChessRobot.py
