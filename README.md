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

python3 app.py


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


## 🌐 Web Interface

In addition to the command-line simulator, a **web interface** was created to allow non-programmers to easily control the robot via buttons and custom commands on a simple webpage. This makes the simulator more accessible to users without programming knowledge.

The web interface is built using **Flask** for the backend and standard **HTML/CSS/JavaScript** for the frontend.

To run the web interface:

1. Start the Flask app (`app.py`).
2. Open your browser and navigate to `http://127.0.0.1:5000/`.
3. Use the buttons or type commands to control the robot.

