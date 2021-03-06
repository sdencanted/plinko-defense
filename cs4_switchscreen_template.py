from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        self.add_widget(self.layout)
        # Add your code below to add the two Buttons
        self.settings_btn = Button(text="settings", on_press=self.change_to_setting, font_size=24)
        self.quit_btn = Button(text="i do not wish to exist", on_press=self.quit_app, font_size=24)

        self.layout.add_widget(self.settings_btn)
        self.layout.add_widget(self.quit_btn)
        # return self.layout
        pass

    def change_to_setting(self, value):
        self.manager.transition.direction = 'left'
        # modify the current screen to a different "name"
        self.manager.current = "settings"

    def quit_app(self, value):
        App.get_running_app().stop()
        Window.close()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        # Add your code below to add the label and the button
        self.add_widget(self.layout)
        self.settings_label = Label(text="Sample Text")
        self.back_to_menu_btn = Button(text="i am done", on_press=self.change_to_menu, font_size=24)
        self.layout.add_widget(self.back_to_menu_btn)
        self.layout.add_widget(self.settings_label)
        # return self.layout
        pass

    def change_to_menu(self, value):
        self.manager.transition.direction = 'right'
        # modify the current screen to a different "name"
        self.manager.current = "menu"


class SwitchScreenApp(App):
    def build(self):
        sm = ScreenManager()
        ms = MenuScreen(name='menu')
        st = SettingsScreen(name='settings')
        sm.add_widget(ms)
        sm.add_widget(st)
        sm.current = 'menu'
        return sm


SwitchScreenApp().run()
