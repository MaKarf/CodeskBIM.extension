from initialize import Alert as CodeskAlert, CopyColor as CodeskCopyColorToClipboard


class Alert:
    def __init__(self, title="Alert", header="Header", content="Content"):
        CodeskAlert(title=title, header=header, content=content)


class CopyColorToClipboard:
    def __init__(self, rgb_color, hex_color):
        CodeskCopyColorToClipboard(rgbColor=rgb_color, hexColor=hex_color)
