import random
from enum import Enum
from typing import List, Tuple, Optional, Dict

class Direction(Enum):
    """Enumeration for robot directions"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class RobotSimulatorError(Exception):
    """Custom exception for robot simulator errors"""
    pass

class OutOfBoundsError(RobotSimulatorError):
    """Exception raised when robot tries to move out of bounds"""
    pass

class InvalidCommandError(RobotSimulatorError):
    """Exception raised for invalid commands"""
    pass

class ObstacleError(RobotSimulatorError):
    """Exception raised when robot hits an obstacle"""
    pass

class BatteryDeadError(RobotSimulatorError):
    """Exception raised when robot battery is dead"""
    pass

class RobotSimulator:
    """
    A comprehensive robot simulator with enhanced features.
    
    Features:
    - Basic movement (forward, left, right)
    - Boundary checking
    - Battery simulation
    - Diagonal movement
    - Obstacle handling
    - Grid expansion
    - Command history
    """
    
    def __init__(self, grid_width: int = 5, grid_height: int = 5, 
                 battery_level: int = 100, expandable_grid: bool = False):
        """
        Initialize the robot simulator.
        
        Args:
            grid_width: Width of the grid
            grid_height: Height of the grid  
            battery_level: Initial battery level (0-100)
            expandable_grid: Whether grid can expand automatically
        """
        self.x = 0
        self.y = 0
        self.direction = Direction.NORTH
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.battery_level = max(0, min(100, battery_level))
        self.expandable_grid = expandable_grid
        self.obstacles: set = set()
        self.command_history: List[str] = []
        self.move_count = 0
        
        # Direction vectors for movement
        self.direction_vectors = {
            Direction.NORTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, -1),
            Direction.WEST: (-1, 0)
        }
        
        # Diagonal direction vectors
        self.diagonal_vectors = {
            'northeast': (1, 1),
            'southeast': (1, -1),
            'southwest': (-1, -1),
            'northwest': (-1, 1)
        }
        
        print(f"Robot initialized at ({self.x}, {self.y}) facing {self.direction.name}")
        print(f"Grid size: {self.grid_width}x{self.grid_height}")
        print(f"Battery level: {self.battery_level}%")
    
    def _consume_battery(self, amount: int = 1):
        """Consume battery for operations"""
        if self.battery_level <= 0:
            raise BatteryDeadError("Robot battery is dead! Cannot perform actions.")
        
        self.battery_level = max(0, self.battery_level - amount)
        if self.battery_level == 0:
            print("Warning: Battery critically low!")
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid boundaries"""
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height
    
    def _expand_grid_if_needed(self, x: int, y: int):
        """Expand grid if expandable_grid is enabled and position is outside"""
        if not self.expandable_grid:
            return
        
        if x >= self.grid_width:
            self.grid_width = x + 1
            print(f"Grid expanded! New width: {self.grid_width}")
        
        if y >= self.grid_height:
            self.grid_height = y + 1
            print(f"Grid expanded! New height: {self.grid_height}")
    
    def forward(self, steps: int = 1):
        """
        Move the robot forward in its current direction.
        
        Args:
            steps: Number of steps to move forward
        """
        try:
            self._consume_battery(steps)
            
            dx, dy = self.direction_vectors[self.direction]
            new_x = self.x + (dx * steps)
            new_y = self.y + (dy * steps)
            
            # Check for expandable grid
            if self.expandable_grid:
                self._expand_grid_if_needed(new_x, new_y)
            
            # Check boundaries
            if not self._is_valid_position(new_x, new_y):
                raise OutOfBoundsError(
                    f"Cannot move to ({new_x}, {new_y}) - outside grid boundaries "
                    f"({self.grid_width}x{self.grid_height})"
                )
            
            # Check for obstacles
            if (new_x, new_y) in self.obstacles:
                raise ObstacleError(f"Cannot move to ({new_x}, {new_y}) - obstacle present!")
            
            self.x, self.y = new_x, new_y
            self.move_count += steps
            
            print(f"Moved forward {steps} step(s) to ({self.x}, {self.y})")
            
        except (OutOfBoundsError, ObstacleError, BatteryDeadError) as e:
            print(f"Error: {e}")
            raise
    
    def left(self):
        """Turn the robot left (counter-clockwise)"""
        try:
            self._consume_battery()
            self.direction = Direction((self.direction.value - 1) % 4)
            print(f"Turned left, now facing {self.direction.name}")
        except BatteryDeadError as e:
            print(f"Error: {e}")
            raise
    
    def right(self):
        """Turn the robot right (clockwise)"""
        try:
            self._consume_battery()
            self.direction = Direction((self.direction.value + 1) % 4)
            print(f"Turned right, now facing {self.direction.name}")
        except BatteryDeadError as e:
            print(f"Error: {e}")
            raise
    
    def diagonal(self, direction: str):
        """
        Move diagonally in the specified direction.
        
        Args:
            direction: One of 'northeast', 'southeast', 'southwest', 'northwest'
        """
        try:
            direction = direction.lower()
            if direction not in self.diagonal_vectors:
                raise InvalidCommandError(
                    f"Invalid diagonal direction: {direction}. "
                    f"Valid options: {list(self.diagonal_vectors.keys())}"
                )
            
            self._consume_battery(2)  # Diagonal moves cost more battery
            
            dx, dy = self.diagonal_vectors[direction]
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check for expandable grid
            if self.expandable_grid:
                self._expand_grid_if_needed(new_x, new_y)
            
            # Check boundaries
            if not self._is_valid_position(new_x, new_y):
                raise OutOfBoundsError(
                    f"Cannot move diagonally to ({new_x}, {new_y}) - outside grid boundaries"
                )
            
            # Check for obstacles
            if (new_x, new_y) in self.obstacles:
                raise ObstacleError(f"Cannot move to ({new_x}, {new_y}) - obstacle present!")
            
            self.x, self.y = new_x, new_y
            self.move_count += 1
            
            print(f"Moved diagonally {direction} to ({self.x}, {self.y})")
            
        except (InvalidCommandError, OutOfBoundsError, ObstacleError, BatteryDeadError) as e:
            print(f"Error: {e}")
            raise
    
    def report(self):
        """Report the current position and status of the robot"""
        status = f"""
=== ROBOT STATUS REPORT ===
Position: ({self.x}, {self.y})
Facing: {self.direction.name}
Battery Level: {self.battery_level}%
Grid Size: {self.grid_width}x{self.grid_height}
Total Moves: {self.move_count}
Obstacles: {len(self.obstacles)} present
Commands Executed: {len(self.command_history)}
========================"""
        print(status)
        return {
            'x': self.x,
            'y': self.y,
            'direction': self.direction.name,
            'battery': self.battery_level,
            'grid_size': (self.grid_width, self.grid_height),
            'moves': self.move_count,
            'obstacles': len(self.obstacles)
        }
    
    def add_obstacle(self, x: int, y: int):
        """Add an obstacle to the grid"""
        if not self._is_valid_position(x, y):
            raise OutOfBoundsError(f"Cannot place obstacle at ({x}, {y}) - outside grid")
        
        if (x, y) == (self.x, self.y):
            raise ObstacleError("Cannot place obstacle on robot's current position")
        
        self.obstacles.add((x, y))
        print(f"Obstacle added at ({x}, {y})")
    
    def remove_obstacle(self, x: int, y: int):
        """Remove an obstacle from the grid"""
        if (x, y) in self.obstacles:
            self.obstacles.remove((x, y))
            print(f"Obstacle removed from ({x}, {y})")
        else:
            print(f"No obstacle at ({x}, {y}) to remove")
    
    def charge_battery(self, amount: int = 50):
        """Charge the robot's battery"""
        old_level = self.battery_level
        self.battery_level = min(100, self.battery_level + amount)
        gained = self.battery_level - old_level
        print(f"Battery charged! Gained {gained}% (now {self.battery_level}%)")
    
    def expand_grid(self, new_width: int, new_height: int):
        """Manually expand the grid"""
        if new_width < self.grid_width or new_height < self.grid_height:
            raise InvalidCommandError("Cannot shrink grid size")
        
        self.grid_width = new_width
        self.grid_height = new_height
        print(f"Grid expanded to {self.grid_width}x{self.grid_height}")
    
    def reset(self):
        """Reset robot to initial position and state"""
        self.x = 0
        self.y = 0
        self.direction = Direction.NORTH
        self.battery_level = 100
        self.obstacles.clear()
        self.command_history.clear()
        self.move_count = 0
        print("Robot reset to initial state")
    
    def show_grid(self):
        """Display a visual representation of the grid"""
        print("\n=== GRID VISUALIZATION ===")
        for y in range(self.grid_height - 1, -1, -1):  # Top to bottom
            row = ""
            for x in range(self.grid_width):
                if x == self.x and y == self.y:
                    # Robot position with direction indicator
                    direction_symbols = {
                        Direction.NORTH: "↑",
                        Direction.EAST: "→",
                        Direction.SOUTH: "↓",
                        Direction.WEST: "←"
                    }
                    row += f" {direction_symbols[self.direction]} "
                elif (x, y) in self.obstacles:
                    row += " # "  # Obstacle
                else:
                    row += " . "  # Empty space
            print(f"{y:2d} |{row}|")
        
        # X-axis labels
        x_labels = "   "
        for x in range(self.grid_width):
            x_labels += f" {x} "
        print(x_labels)
        print("========================\n")
    
    def execute_command(self, command: str):
        """
        Execute a command string.
        
        Args:
            command: Command string to execute
        """
        try:
            command = command.strip().lower()
            parts = command.split()
            
            if not parts:
                raise InvalidCommandError("Empty command")
            
            cmd = parts[0]
            self.command_history.append(command)
            
            if cmd == "forward" or cmd == "f":
                steps = int(parts[1]) if len(parts) > 1 else 1
                self.forward(steps)
            elif cmd == "left" or cmd == "l":
                self.left()
            elif cmd == "right" or cmd == "r":
                self.right()
            elif cmd == "diagonal" or cmd == "d":
                if len(parts) < 2:
                    raise InvalidCommandError("Diagonal command requires direction")
                self.diagonal(parts[1])
            elif cmd == "report":
                self.report()
            elif cmd == "charge":
                amount = int(parts[1]) if len(parts) > 1 else 50
                self.charge_battery(amount)
            elif cmd == "grid":
                self.show_grid()
            elif cmd == "reset":
                self.reset()
            elif cmd == "obstacle":
                if len(parts) >= 3:
                    x, y = int(parts[1]), int(parts[2])
                    self.add_obstacle(x, y)
                else:
                    raise InvalidCommandError("Obstacle command requires x y coordinates")
            else:
                raise InvalidCommandError(f"Unknown command: {cmd}")
                
        except (ValueError, IndexError) as e:
            error_msg = f"Invalid command format: {command}"
            print(f"Error: {error_msg}")
            raise InvalidCommandError(error_msg)
        except RobotSimulatorError:
            # Re-raise simulator-specific errors
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise RobotSimulatorError(f"Unexpected error: {e}")

def interactive_mode():
    """Run the robot simulator in interactive mode"""
    print("=== Robot Simulator Interactive Mode ===")
    print("Available commands:")
    print("  forward [steps] - Move forward (f)")
    print("  left - Turn left (l)")
    print("  right - Turn right (r)")
    print("  diagonal <direction> - Move diagonally (d)")
    print("  report - Show status")
    print("  charge [amount] - Charge battery")
    print("  grid - Show grid visualization")
    print("  obstacle <x> <y> - Add obstacle")
    print("  reset - Reset robot")
    print("  help - Show this help")
    print("  quit - Exit simulator")
    print("=========================================\n")
    
    # Initialize robot with some obstacles for demonstration
    robot = RobotSimulator(grid_width=8, grid_height=8, expandable_grid=True)
    robot.add_obstacle(2, 2)
    robot.add_obstacle(3, 3)
    robot.add_obstacle(1, 4)
    
    robot.show_grid()
    
    while True:
        try:
            command = input("Robot> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif command.lower() == 'help':
                print("\nAvailable commands:")
                print("  forward [steps], left, right, diagonal <dir>")
                print("  report, charge [amount], grid, obstacle <x> <y>")
                print("  reset, help, quit")
                continue
            
            if command:
                robot.execute_command(command)
                
                # Random battery drain for realism
                if random.random() < 0.1:  # 10% chance
                    robot.battery_level = max(0, robot.battery_level - 1)
                    if robot.battery_level <= 20:
                        print(f"Warning: Low battery ({robot.battery_level}%)")
        
        except RobotSimulatorError as e:
            print(f"Simulator Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def demo_mode():
    """Run a demonstration of the robot simulator"""
    print("=== Robot Simulator Demo ===\n")
    
    # Create robot with custom settings
    robot = RobotSimulator(grid_width=6, grid_height=6, battery_level=80)
    
    # Add some obstacles
    robot.add_obstacle(2, 2)
    robot.add_obstacle(3, 2)
    robot.add_obstacle(1, 4)
    
    # Demo commands
    commands = [
        "report",
        "forward 2",
        "right",
        "forward",
        "diagonal northeast", 
        "left",
        "forward",
        "grid",
        "charge 20",
        "report"
    ]
    
    print("Executing demo commands...")
    for cmd in commands:
        print(f"\n> {cmd}")
        try:
            robot.execute_command(cmd)
        except RobotSimulatorError as e:
            print(f"Command failed: {e}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    print("Robot Simulator Options:")
    print("1. Interactive Mode")
    print("2. Demo Mode")
    
    choice = input("Select mode (1/2): ").strip()
    
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        demo_mode()
    else:
        print("Running demo by default...")
        demo_mode()





