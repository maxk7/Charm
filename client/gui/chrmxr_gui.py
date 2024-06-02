from textual import events
from textual.app import App, ComposeResult
from textual.widgets import TextArea, RichLog, DataTable, Label, Static
from rich.table import Table
from rich.text import Text
import requests
import socketio
import json

cmdNumber = 0                   # command id number
sio = socketio.Client()         # socketio for viz data
url = 'http://127.0.0.1:5000'   # url for code post


# Handles incoming audio data from websocket
@sio.on('audio-feed-reply')
def on_audio_feed(data):
    log = app.query_one(RichLog)
    log.write(data)


# Request audio data via websocket
def get_audio():
    try:
        response = sio.emit('audio-feed')
        return response
    except socketio.exceptions.BadNamespaceError:
        return 400


# Helper function to POST Hydra
def send_code(content, log):
    global cmdNumber
    cmdNumber += 1
    
    json_data = json.dumps({'code': content})
    response = requests.post(url+'/run-js', headers={'Content-Type': 'application/json'}, data=json_data)

    # process the response
    if "400" in str(response):
        message = "[steel_blue]400 ✿[/]"
    elif "403" in str(response):
        message = "[steel_blue]403 ✿[/]"
    elif "404" in str(response):
        message = "[steel_blue]404 ✿[/]"
    elif "200" in str(response):
        message = "[deep_pink3]200 ❤︎[/]"
    else:
        message = None

    # Clean outputting of response to RichLog 
    table = Table(show_header=False, show_lines=False, padding=(0, 1, 0, 1), box=None)
    table.add_column(width=5)
    table.add_column(width=5)
    table.add_row(f"[dim]{cmdNumber}[/]", message)
    log.write(table)

    return response


# CODE EDITOR
''' Keybinds
grave  update   code
opt+1  decrease cutoff
opt+2  increase cutoff
opt+3  decrease smooth
opt+4  increase smooth
'''
class ExtendedTextArea(TextArea):
    def on_key(self, event: events.Key) -> None:
        log = app.query_one(RichLog)

        # keybind to post code to server
        if event.character == "`":
            response = send_code(self.text, log)
            event.prevent_default()

        # test keybind to retreive audio data
        if event.character == "~":
            log.write(get_audio())
            event.prevent_default()

        # additional logic to handle settings posts
        else:
            table = app.query_one(HydraDashboard)

            # decrease cutoff
            if event.character == "¡":
                newCutoff = table.getCutoff() - 0.1
                response = send_code(f"a.setCutoff({newCutoff})", log)

                if "200" in str(response):
                    table.setCutoff(newCutoff)
                    table.refreshDash() 

                event.prevent_default()

            # increase cutoff 
            elif event.character == "™":
                newCutoff = table.getCutoff() + 0.1
                response = send_code(f"a.setCutoff({newCutoff})", log)

                if "200" in str(response):
                    table.setCutoff(newCutoff)
                    table.refreshDash() 

                event.prevent_default()

            # decrease smooth
            elif event.character == "£":
                newSmooth = table.getSmooth() - 0.05
                response = send_code(f"a.setSmooth({newSmooth})", log)

                if "200" in str(response):
                    table.setSmooth(newSmooth)
                    table.refreshDash() 

                event.prevent_default()

            # increase smooth
            elif event.character == "¢":
                newSmooth = table.getSmooth() + 0.05
                response = send_code(f"a.setSmooth({newSmooth})", log)

                if "200" in str(response):
                    table.setSmooth(newSmooth)
                    table.refreshDash() 

                event.prevent_default()


# Dashboard widget for displaying vizualizer settings
class HydraDashboard(DataTable):
    ROWS = [
        ["SETTINGS MODULE", "VALUE"],
        ["---------------", "-----"],
        ["setCutoff", 3.00],
        ["setSmooth", 0.35]
    ]

    # Helper function to update the table widget
    def refreshDash(self):
        self.clear()
        self.add_rows(self.ROWS)

    # Getters
    def getCutoff(self):
        return self.ROWS[2][1]


    def getSmooth(self):
        return self.ROWS[3][1]


    # Setters
    def setCutoff(self, value):
        self.ROWS[2][1] = value


    def setSmooth(self, value):
        self.ROWS[3][1] = value


# APPLICATION
class charm(App):
    CSS_PATH = "stylesheet.tcss"
    heading = Text().assemble("charm xr   ", ("-   max konzerowsky", "dim"))

    def compose(self) -> ComposeResult:
        yield Label(self.heading)
        yield HydraDashboard(show_header=False, show_cursor=False)
        yield Static()
        yield ExtendedTextArea.code_editor(theme='css')
        yield RichLog(markup=True)
        

    def on_mount(self) -> None:
        table = self.query_one(HydraDashboard)
        table.add_columns("", "")
        table.refreshDash()


if __name__ == "__main__":
    try:
        sio.connect('http://127.0.0.1:5000')
    except socketio.exceptions.ConnectionError:
        print("unable to establish audio pipeline")

    app = charm()
    app.run()

