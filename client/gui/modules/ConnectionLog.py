from textual.widgets import RichLog

class ConnectionLog(RichLog):
    def on_mount(self) -> None:
        self.markup=True
        self.max_lines=5

