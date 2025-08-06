# 🤖 Robot Simulator

A feature-rich robot simulator written in Python. This simulator allows you to control a robot inside a 2D grid with commands like moving forward, turning, diagonal movement, battery simulation, obstacle avoidance, and more.

---

## 🎯 Purpose

This project simulates a robot that moves within a grid while responding to user commands. It's designed for practicing:
- Object-Oriented Programming
- Custom exception handling
- Simulation logic
- CLI-based interaction
- Grid-based movement systems

---

## 🚀 How to Run

Make sure you have **Python 3** installed.

### Run in Terminal:

python3 robot_simulator.py

Choose a mode:

Type 1 for Interactive Mode (manual commands).

Type 2 for Demo Mode (automatic sample run).


🛠️ Features and Methods


✅ Movement

forward [steps]: Move the robot forward in the current direction.

left: Turn the robot left (counterclockwise).

right: Turn the robot right (clockwise).

diagonal <direction>: Move diagonally (e.g., northeast, southwest).


📏 Grid

show_grid(): Visual display of the robot, grid, and obstacles.

Expandable grid if expandable_grid=True.


🔋 Battery

Each move consumes battery.

charge [amount]: Recharge battery (default is 50%).



🚧 Obstacles

add_obstacle(x, y): Place an obstacle.

remove_obstacle(x, y): Remove obstacle.

Robot cannot pass through obstacles.



🧠 Commands

execute_command(command: str): Parses and runs commands such as "forward 3", "diagonal northeast", etc.


📋 Reporting

report(): Displays current position, direction, battery level, grid size, and move count.


🌀 Other


reset(): Resets robot to starting point.

expand_grid(new_width, new_height): Manually expand the grid.


📸 Example Commands (Interactive Mode)


forward 2

right

forward

diagonal southeast

obstacle 4 3

report

grid

reset

