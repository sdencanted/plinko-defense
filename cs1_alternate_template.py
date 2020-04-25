from kivy.app import App
from kivy.uix.label import Label


class AlternateApp(App):

    def build(self):
        self.lab = Label(text="pootis")
        self.lab.bind(on_touch_down=self.alternate)
        return self.lab
        pass

    def alternate(self, instance, touch):
        print("spencer")
        self.lab.text = "painis"
        pass


myapp = AlternateApp()
myapp.run()
