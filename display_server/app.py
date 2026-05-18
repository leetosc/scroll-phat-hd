import os

from flask import Flask, jsonify, render_template, request

from .controller import DisplayController
from .registry import list_modes

app = Flask(__name__, template_folder="templates", static_folder="static")
controller = DisplayController()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/modes")
def api_modes():
    return jsonify({"modes": list_modes()})


@app.route("/api/state")
def api_state():
    return jsonify(controller.state())


@app.route("/api/mode", methods=["POST"])
def api_mode():
    data = request.get_json(silent=True) or {}
    mode_id = data.get("mode")
    if not mode_id:
        return jsonify({"error": "mode is required"}), 400
    try:
        controller.set_mode(mode_id, defaults_only=True)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(controller.state())


@app.route("/api/config", methods=["PATCH"])
def api_config():
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "config body required"}), 400
    controller.store.update(data)
    return jsonify(controller.state())


@app.route("/api/reset", methods=["POST"])
def api_reset():
    controller.reset_config()
    return jsonify(controller.state())


def main():
    host = os.environ.get("SCROLLPHAT_HOST", "0.0.0.0")
    port = int(os.environ.get("SCROLLPHAT_PORT", "8080"))
    controller.start_default()
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
