from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass


class PrintStatementUI(BaseWPFClass):

    def __init__(self, print_string="", error_string=""):
        BaseWPFClass.__init__(self, "PrintStatementUI.xaml")
        """"""

        self.print_statements.Text = print_string
        self.error_statements.Text = error_string
        #
        self.ShowDialog()
