from flask import Flask, render_template, redirect, url_for, request

class BellAudioClassifierWebUI:
    def __init__(self):
        self.running = False
        self.made_shots = 0

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

def create_app():
    app = Flask(__name__)
    web_ui = BellAudioClassifierWebUI()

    @app.route('/')
    def index():
        return render_template('index.html',
                               running=web_ui.running,
                               made_shots=web_ui.made_shots)

    @app.route('/start', methods=['POST'])
    def start():
        web_ui.start()
        return redirect(url_for('index'))

    @app.route('/stop', methods=['POST'])
    def stop():
        web_ui.stop()
        return redirect(url_for('index'))

    @app.route('/quit', methods=['POST'])
    def quit():
        # Hier könnte der Server beendet werden
        return redirect(url_for('index'))

    return app