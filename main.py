import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Data Science Project')
        self.props.show_menubar = True

        header = Gtk.HeaderBar()

        self.set_titlebar(header)

        stack = Gtk.Stack()

        stack.props.transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT

        stack.props.transition_duration = 500

        self.set_child(stack)

        info_page = self._get_information_page()

        label1 = Gtk.Label()
        label1.set_markup('<big>A fancy label</big>')
        stack.add_titled(label1, 'file', 'File Chooser')
        stack.add_titled(info_page, 'info', 'Info')
        stack.set_visible_child_name('file')

        stack_switcher = Gtk.StackSwitcher()

        stack_switcher.set_stack(stack)

        header.set_title_widget(stack_switcher)

    def _get_information_page(self) -> Gtk.CenterBox:
        sidebar = Gtk.ListBox()
        imageLayout = Gtk.Box(spacing=6)

        label1 = Gtk.Label(label='Big asssss Label 1')
        sidebar.append(label1)
        label2 = Gtk.Label(label='Label 2')
        sidebar.append(label2)
        label3 = Gtk.Label(label='Label 3')
        sidebar.append(label3)
        label4 = Gtk.Label(label='Label 4')
        sidebar.append(label4)
        label5 = Gtk.Label(label='Label 5')
        sidebar.append(label5)

        button11 = Gtk.Button(label='Hello')
        imageLayout.append(button11)

        main_box = Gtk.CenterBox()
        main_box.set_start_widget(sidebar)
        main_box.set_center_widget(imageLayout)

        return main_box


def on_activate(app):
    win = MainWindow(application=app)
    win.present()


app = Gtk.Application(application_id='com.github.towk.data-science-project')
app.connect('activate', on_activate)

app.run(None)
