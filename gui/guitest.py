from textual import events
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Sparkline, RichLog
import math
import requests

text_log = None
data = [math.sin(x) for x in range(0, 100)]

class ExtendedTextArea(TextArea):
    def on_key(self, event: events.Key) -> None:
        if event.character == "(":
            self.insert("()")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()

        if event.character == "`":
            url = 'http://127.0.0.1:5000/post-data'
            code = self.text
            response = requests.post(url, json={'code': code})
            app.query_one(RichLog).write(response)
            event.prevent_default()
        

class TextAreaConsoleLog(RichLog):
    pass


class TextAreaKeyPressHook(App):
    CSS_PATH = "guitest.tcss"

    def compose(self) -> ComposeResult:
        yield Sparkline(data, summary_function=max)
        yield ExtendedTextArea.code_editor(language="javascript")
        yield TextAreaConsoleLog()


if __name__ == "__main__":
    app = TextAreaKeyPressHook()
    app.run()
