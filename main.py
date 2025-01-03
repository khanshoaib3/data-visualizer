import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk
from gi.repository import Adw

import pandas as pd
import plotly.express as px


class LabelWithKey(Gtk.Label):
    def __init__(self, key: str, **properties):
        super().__init__(**properties)
        self.key = key


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Data Analyzer')
        self.props.show_menubar = True
        info_page = self.get_main_layout()

        self.set_content(info_page)

    def get_main_layout(self) -> Gtk.CenterBox:
        main_box: Adw.NavigationSplitView = Adw.NavigationSplitView().new()

        sidebar: Adw.ToolbarView = Adw.ToolbarView().new()
        sidebar_header: Adw.HeaderBar = Adw.HeaderBar().new()
        sidebar_header.set_show_title(show_title=False)
        open_file_button: Gtk.Button = Gtk.Button(label='Open')
        open_file_button.add_css_class('suggested-action')
        sidebar_header.pack_start(open_file_button)
        sidebar.add_top_bar(sidebar_header)
        sidebar_list_box: Gtk.ListBox = Gtk.ListBox().new()
        sidebar_list_box.add_css_class("navigation-sidebar")
        sidebar.set_content(sidebar_list_box)
        sidebar = Adw.NavigationPage().new(child=sidebar, title='Sidebar')

        select_option_page: Adw.ToolbarView = Adw.ToolbarView().new()
        select_option_page_header: Adw.HeaderBar = Adw.HeaderBar().new()
        select_option_page_header.set_show_title(show_title=True)
        select_option_page.add_top_bar(select_option_page_header)

        stacks: Adw.NavigationView = Adw.NavigationView().new()
        default_page: Adw.NavigationPage = Adw.NavigationPage().new(child=Gtk.Label(label='Select an option!!'), title='Select Option')
        stacks.push(default_page)
        select_option_page.set_content(stacks)

        select_option_page = Adw.NavigationPage().new(child=select_option_page, title='content')

        main_box.set_sidebar(sidebar)
        main_box.set_content(select_option_page)

        buttons = {
            'table': 'Table',
            'bar': 'Bar',
            'bubble': 'Bubble Chart',
            'line': 'Line Graph',
            'scatter': 'Scatter Graph'
        }

        for key, value in buttons.items():
            label = LabelWithKey(label=value, key=key)
            label.set_xalign(0)
            sidebar_list_box.append(label)
        sidebar_list_box.connect('row-activated', self.select_result_page_callback, stacks)

        return main_box

    def select_result_page_callback(self, _, button: Gtk.ListBoxRow, stacks: Adw.NavigationView):
        dataset1 = pd.read_csv("/home/towk/Projects/test/data-science/covid.csv")

        option_tab: Adw.PreferencesPage = Adw.PreferencesPage().new()
        option_group: Adw.PreferencesGroup = Adw.PreferencesGroup().new()
        option_group_2: Adw.PreferencesGroup = Adw.PreferencesGroup().new()
        option_tab.add(option_group)
        option_tab.add(option_group_2)

        option_tab.set_size_request(600, 600)
        image_tab = Gtk.Box()

        result_stack: Adw.NavigationView = Adw.NavigationView()
        result_stack.push(Adw.NavigationPage().new(option_tab, "option"))

        column_list = Gtk.StringList()
        for col in dataset1.columns.to_list():
            column_list.append(col)

        x_button: Adw.ComboRow = Adw.ComboRow().new()
        # x_button.set_enable_search(True)
        x_button.set_title('x')
        x_button.set_model(column_list)
        option_group.add(x_button)

        y_button: Adw.ComboRow = Adw.ComboRow().new()
        # y_button.set_enable_search(True)
        y_button.set_title('y')
        y_button.set_model(column_list)
        option_group.add(y_button)

        plot_butt: Adw.ActionRow = Adw.ActionRow().new()
        plot_butt.set_title('Plot')
        plot_butt.add_css_class('suggested-action')
        plot_butt.set_activatable(True)
        option_group_2.add(plot_butt)

        stacks.pop()
        stacks.push(Adw.NavigationPage().new(child=result_stack, title=button.get_child().get_label()))
        page_type = button.get_child().key
        if page_type == 'bar':
            plot_butt.connect('activated', self.plot_graph, page_type, result_stack, image_tab,
                              dataset1, x_button, y_button, column_list)
        elif page_type == 'bubble':
            plot_butt.connect('activated', self.plot_graph, page_type, result_stack, image_tab,
                              dataset1, x_button, y_button, column_list)
        elif page_type == 'line':
            plot_butt.connect('activated', self.plot_graph, page_type, result_stack, image_tab,
                              dataset1, x_button, y_button, column_list)
        elif page_type == 'scatter':
            plot_butt.connect('activated', self.plot_graph, page_type, result_stack, image_tab,
                              dataset1, x_button, y_button, column_list)

    def plot_graph(self, button, graph_type, stack: Adw.NavigationView, image_tab: Gtk.Box, dataset, x: Gtk.DropDown,
                   y: Gtk.DropDown,
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
            px.scatter(dataset, x=x, y=y, color=y).write_image(".temp.png")

        img = Gtk.Image().new_from_file(".temp.png")
        img.set_size_request(600, 600)
        image_tab.append(img)
        stack.push(Adw.NavigationPage().new(image_tab, "image"))


def on_activate(app):
    win = MainWindow(application=app)
    win.present()


app = Adw.Application(application_id='com.github.towk.data-science-project')
app.connect('activate', on_activate)

app.run(None)
