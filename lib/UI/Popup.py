from lib.AppMethods import Alert as CodeskAlert


class Alert:
    def __init__(self, title="Alert", header="Header", content="Content"):
        CodeskAlert(title=title, header=header, content=content)


