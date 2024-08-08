import gi
# Data analysis and Manipulation
import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Data Visualization
import matplotlib.pyplot as plt
import plotly.offline
from plotly.figure_factory import create_table

# Importing Plotly
import plotly.offline as py

# import word cloud
# from wordcloud import WordCloud

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Data Science Project')
        self.props.show_menubar = True
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        stack = Gtk.Stack()
        stack.props.transition_type = Gtk.StackTransitionType.OVER_LEFT_RIGHT
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

        select_option_page = Gtk.Box()
        select_option_page.set_size_request(600, 600)
        select_option_page.append(Gtk.Label(label="Select an option!!"))

        main_box = Gtk.CenterBox()
        main_box.set_start_widget(sidebar)
        main_box.set_center_widget(select_option_page)

        buttons = {
            'table': 'Table',
            'bar': 'Bar',
            'bubble': 'Bubble Chart',
            'line': 'Line Graph',
            'scatter': 'Scatter Graph'
        }

        for key, value in buttons.items():
            btn = Gtk.Button(label=value)
            sidebar.append(btn)
            btn.connect('clicked', self.select_result_page_callback, key, main_box)

        return main_box

    def select_result_page_callback(self, button: Gtk.Button, page_type: str, main_box: Gtk.CenterBox):
        dataset1 = pd.read_csv("/home/towk/Projects/test/data-science/covid.csv")

        option_tab = Gtk.Box()
        option_tab.set_size_request(600, 600)
        image_tab = Gtk.Box()

        result_stack = Gtk.Stack()
        result_stack.props.transition_type = Gtk.StackTransitionType.SLIDE_UP
        result_stack.props.transition_duration = 250
        result_stack.add_named(option_tab, "option")
        result_stack.add_named(image_tab, "image")
        result_stack.set_visible_child_name("option")

        column_list = Gtk.StringList()
        for col in dataset1.columns.to_list():
            column_list.append(col)

        x_button: Gtk.DropDown = Gtk.DropDown.new(column_list)
        x_button.set_enable_search(True)
        option_tab.append(x_button)

        y_button: Gtk.DropDown = Gtk.DropDown.new(column_list)
        y_button.set_enable_search(True)
        option_tab.append(y_button)

        plot_butt = Gtk.Button(label='Plot')
        option_tab.append(plot_butt)

        main_box.set_center_widget(result_stack)
        if page_type == 'bar':
            plot_butt.connect('clicked', self.plot_graph, page_type, result_stack, image_tab, dataset1, x_button, y_button,
                              column_list)
        elif page_type == 'bubble':
            plot_butt.connect('clicked', self.plot_graph, page_type, result_stack, image_tab, dataset1, x_button, y_button,
                              column_list)
        elif page_type == 'line':
            plot_butt.connect('clicked', self.plot_graph, page_type, result_stack, image_tab, dataset1, x_button, y_button,
                              column_list)
        elif page_type == 'scatter':
            plot_butt.connect('clicked', self.plot_graph, page_type, result_stack, image_tab, dataset1, x_button, y_button,
                              column_list)

    def plot_graph(self, button, graph_type, stack: Gtk.Stack, image_tab: Gtk.Box, dataset, x: Gtk.DropDown, y: Gtk.DropDown,
                   list: Gtk.StringList):
        x = list.get_item(x.get_selected()).get_string()
        y = list.get_item(y.get_selected()).get_string()
        dataset = dataset.head(15)

        if graph_type == 'bar':
            px.bar(dataset, x=x, y=y, color=y).write_image(".temp.png")
        elif graph_type == 'bubble':
            px.scatter(dataset, x=x, y=y, size=y, color=y, size_max=80).write_image(".temp.png")
        elif graph_type == 'line':
            px.line(dataset, x=x, y=y).write_image(".temp.png")
        elif graph_type == 'scatter':
            px.scatter(dataset, x=x, y=y).write_image(".temp.png")

        img = Gtk.Image().new_from_file(".temp.png")
        img.set_size_request(600, 600)
        image_tab.append(img)
        stack.set_visible_child_name("image")


def on_activate(app):
    win = MainWindow(application=app)
    win.present()


app = Gtk.Application(application_id='com.github.towk.data-science-project')
app.connect('activate', on_activate)

app.run(None)
