from initialize import Alert as CodeskAlert, CopyColor as CodeskCopyColorToClipboard


class Alert:
    def __init__(self, title="Alert", header="Header", content="Content"):
        CodeskAlert(title=title, header=header, content=content)


