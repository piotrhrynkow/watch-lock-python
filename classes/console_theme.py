from inquirer.themes import Theme
from blessed import Terminal
term = Terminal()


class QuestionTheme(Theme):

    def __init__(self):
        super(QuestionTheme, self).__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.bright_green
        self.Question.default_color = term.yellow
        self.Checkbox.selection_color = term.bold_black_on_bright_green
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '[✓]'
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '[ ]'
        self.List.selection_color = term.bold_black_on_bright_green
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal