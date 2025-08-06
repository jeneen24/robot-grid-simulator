from flask import Flask, request, jsonify, render_template
from robot_simulator import RobotSimulator  

app = Flask(__name__)

robot = RobotSimulator(grid_width=5, grid_height=5)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    cmd = data.get('command', '')

    try:
        robot.execute_command(cmd)
        status = robot.report()
        return jsonify({'status': 'success', 'data': status})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
