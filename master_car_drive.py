from flask import Flask, request
import PiMotor

LM = PiMotor.Motor("MOTOR1", 2)
RM = PiMotor.Motor("MOTOR4", 2)
app = Flask(__name__)

@app.route("/", methods=["POST"])
def take_input():
    try:
        left_val = float(request.form["left"])
        right_val = float(request.form["right"])
        print(left_val, right_val)
        # run forward or reverse motor for left
        [LM.reverse, LM.forward][left_val > 0](abs(left_val) * 99)
        # run forward or reverse motor for right
        [RM.reverse, RM.forward][right_val > 0](abs(right_val) * 99)

        return "OK"

    except Exception as e:
        LM.stop()
        RM.stop()
        print(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
