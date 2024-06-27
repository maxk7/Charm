"""
Author: Max Konzerowsky
Description: Extensible TUI connection to local hydra visualizer
"""

#### textual imports ####
# UI
from textual.app import App, ComposeResult
from textual.widgets import TextArea, RichLog, Label 
from textual.binding import Binding

# Widgets
from modules.HydraExtensions import HydraExtensionModule
from modules.VisDash import HydraDashboard
from modules.ToggleDash import ToggleDashboard
from modules.ConnectionLog import ConnectionLog
from modules.Temp0 import Tempo

####  other imports  ####
# Rich UI Imports
from rich.table import Table
from rich.text import Text

# Connection Imports
import requests
import socketio
import json

# Additional tools
from datetime import datetime
import os
import re

####  end of imports ####


# client variables
cmdNumber = 0                   # initial command id number
sio = socketio.Client()         # socketio for viz data
url = 'http://127.0.0.1:5000'   # url for code post


#### Viz Gui Aduio Connection (WIP) ####
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

####  ----------------------------- ####


# Post Code to Hydra
def send_code(content, log):
    global cmdNumber
    cmdNumber += 1

    try:
        modules = app.query_one(ToggleDashboard)
        JSExtensionStatus = modules.getTestMethod()

        if JSExtensionStatus == modules.symbEnabled:
            content = HydraExtensionModule(content)
    
    except:
        pass # default to not applying edits

    json_data = json.dumps({'code': content})
    response = requests.post(url+'/run-js', headers={'Content-Type': 'application/json'}, data=json_data)

    # process the response
    if "40" in str(response):
        # 400, 403, 404
        message = "[steel_blue]error ✿[/]"
    elif "200" in str(response):
        message = "[deep_pink3]sent! ❤︎[/]"
    else:
        message = None

    # Clean outputting of response to ConnectionLog 
    table = Table(show_header=False, show_lines=False, padding=(0, 0, 0, 0), box=None)
    table.add_column(width=5)
    table.add_column(width=7, justify="center")
    table.add_row(f"[dim]{cmdNumber}[/]", message)
    log.write(table)

    return response


#### application ####
class chrm(App):
    spacing = 4 # adjust header spacing to preferences
    heading = Text().assemble("⊹ chrm xr ⊹"
                              +" "*spacing,
                              ("-"+" "*spacing
                               +"max konzerowsky", "dim"))

    BINDINGS = [
        # Hydra Editor 
        Binding("`", "sendCode", "Update", priority=True),

        # Quick Update 
        Binding("¡", "increaseCutoff(0.1)", "[+] Cutoff", priority=True),
        Binding("™", "increaseCutoff(-0.1)", "[-] Cutoff", priority=True),
        Binding("£", "increaseSmooth(0.05)", "[+] Smooth", priority=True),
        Binding("¢", "increaseSmooth(-0.05)", "[-] Smooth", priority=True),

        # Extension Toggle
        Binding("≠", "toggleHydra3xtend", "Toggle Hy3x", priority=True),

        # Tempo
        Binding("º", "tempoTap", "", priority=True),
        Binding("–", "sendTempo", "", priority=True),

        # Application General 
        Binding("ß", "saveCode", "Save", priority=True),
    ]

    CSS_PATH = "stylesheet.tcss"


    def compose(self) -> ComposeResult:
        yield Label(self.heading)
        yield HydraDashboard(show_header=False, show_cursor=False)
        yield ToggleDashboard(show_header=False, show_cursor=False)
        yield TextArea.code_editor(theme='css')
        yield Tempo("")
        yield ConnectionLog()
        

    def on_mount(self) -> None:
        # initialize both tables without a header row
        HydraDash = self.query_one(HydraDashboard)
        HydraDash.add_columns("", "")
        HydraDash.refreshDash()
        
        ToggleDash = self.query_one(ToggleDashboard)
        ToggleDash.add_columns("", "")
        ToggleDash.refreshDash()


    ### keybind functions ###
    def action_sendCode(self) -> None:
        # keybind to post code to server
        log = self.query_one(RichLog)
        text = self.query_one(TextArea).text
        send_code(text, log)


    def action_getAudio(self) -> None:
        log = self.query_one(RichLog)
        log.write(get_audio())


    def action_increaseCutoff(self, amount) -> None:
        table = self.query_one(HydraDashboard)
        newCutoff = table.getCutoff() + amount
        response = send_code(f"a.setCutoff({newCutoff})", self.query_one(RichLog))

        if "200" in str(response):
            table.setCutoff(newCutoff)
            table.refreshDash() 


    def action_increaseSmooth(self, amount) -> None:
        table = self.query_one(HydraDashboard)
        newSmooth = table.getSmooth() + amount
        response = send_code(f"a.setSmooth({1 - newSmooth})", self.query_one(RichLog))

        if "200" in str(response):
            table.setSmooth(newSmooth)
            table.refreshDash() 


    def action_toggleHydra3xtend(self) -> None:
        modules = self.query_one(ToggleDashboard)
        moduleStatus = modules.getTestMethod()

        # toggle status
        if moduleStatus == modules.symbEnabled:
            modules.setTestMethod(modules.symbDisabled)
        else:
            modules.setTestMethod(modules.symbEnabled)

        modules.refreshDash()


    def action_tempoTap(self) -> None:
        tempoWidget = app.query_one(Tempo)
        tempoWidget.tap()


    def action_sendTempo(self) -> None:
        tempo = app.query_one(Tempo)
        log = app.query_one(RichLog)
        send_code(f"bpm = {tempo.tempo}", log)


    def action_saveCode(self) -> None:
        editor = app.query_one(TextArea)

        # attempt filename
        match = re.search(r"^\/\/ *(\w*)", editor.text)

        # Save the match to the variable file_name
        file_name = match.group(1) if match else datetime.now().strftime("%H%M%S %d%m")
        file_path = os.path.expanduser(f"~/Desktop/Summer/Hydra/saves/{file_name}.txt")
        
        with open(file_path, "w") as file:
            file.write(editor.text)

    ### ----------------- ###

#### end of application ####


if __name__ == "__main__":
    try:
        sio.connect('http://127.0.0.1:5000')
    except socketio.exceptions.ConnectionError:
        print("unable to establish audio pipeline")

    app = chrm()
    app.run()

