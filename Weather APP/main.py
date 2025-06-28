import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                              QPushButton, QLineEdit, QVBoxLayout )
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setFixedSize(400, 600) 

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
                           QLabel, QPushButton{
                           font-family : calibri;
                           }
                           QLabel#city_label{
                           font-size : 40px;
                           font-style : italic;
                           }
                           QLineEdit#city_input{
                           font-size : 40px;
                           }
                           QPushButton#get_weather_button{
                           font-size : 30px;
                           font-weight: bold;
                           }
                           QLabel#temperature_label{
                           font-size : 75px;
                           }
                           QLabel#emoji_label{
                           font-size : 100px;
                           font-family : Segoe UI Emoji;
                           }
                           QLabel#description_label{
                           font-size : 50px;
                           }

        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Enter city name")
            return

        # you can get/generate this api key from https://home.openweathermap.org/api_keys 
        api_key = "Use your own api key" 
       
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:    
            response = requests.get(url, timeout=5)
            response.raise_for_status()  
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_err: 
            error_messages = {
                401: "Invalid API key",
                403: "Access forbidden",
                404: "City not found",
                500: "Server error",
                502: "Bad gateway",
                503: "Service unavailable",
                504: "Request timeout",
            }
            message = error_messages.get(response.status_code, "Request failed")
            self.display_error(message)
            
        except requests.exceptions.ConnectionError:
            self.display_error("No internet connection")
            
        except requests.exceptions.Timeout:
            self.display_error("Request timed out")
            
        except requests.exceptions.RequestException:
            self.display_error("Network error")

    def display_error(self, message):
        # Reset to smaller font and add word wrap for errors
        self.temperature_label.setStyleSheet("font-size: 30px; color: red;")
        self.temperature_label.setText(message)
        self.temperature_label.setWordWrap(True)  
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, weather_data):
        # Reset to normal styling for weather display
        self.temperature_label.setStyleSheet("font-size: 75px; color: black;")
        self.temperature_label.setWordWrap(False) 
        
        temperature_C = weather_data["main"]["temp"] - 273.15
        weather_description = weather_data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_C:.0f} °C")
        self.emoji_label.setText(self.get_emoji(weather_description))
        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_emoji(weather_description):
        emoji_map = {
        "clear sky": "☀️",
        "few clouds": "🌤️",
        "scattered clouds": "🌥️",
        "broken clouds": "☁️",
        "overcast clouds": "☁️",
        "shower rain": "🌧️",
        "rain": "🌧️",
        "light rain": "🌦️",
        "moderate rain": "🌧️",
        "heavy intensity rain": "🌧️",
        "very heavy rain": "🌧️",
        "extreme rain": "🌧️",
        "freezing rain": "🧊🌧️",
        "light snow": "🌨️",
        "snow": "❄️",
        "heavy snow": "❄️❄️",
        "sleet": "🌨️",
        "light shower sleet": "🌨️",
        "shower sleet": "🌨️",
        "light rain and snow": "🌧️❄️",
        "rain and snow": "🌧️❄️",
        "light shower snow": "🌨️",
        "shower snow": "🌨️",
        "heavy shower snow": "❄️❄️",
        "thunderstorm": "⛈️",
        "thunderstorm with light rain": "⛈️🌧️",
        "thunderstorm with heavy rain": "⛈️🌧️🌧️",
        "mist": "🌫️",
        "smoke": "🌫️",
        "haze": "🌫️",
        "sand": "🏜️",
        "dust": "🌪️",
        "fog": "🌁",
        "ash": "🌋",
        "squall": "🌬️",
        "tornado": "🌪️"
        }

        return emoji_map.get(weather_description, "🌍") 


if __name__ == '__main__':
    app = QApplication([])
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())