import flet as ft
import requests

API_URL = "http://192.168.0.4:5000/api/control"
MOTION_URL = "http://192.168.0.4:5000/api/motion"

def main(page: ft.Page):
    page.title = "Smart Room Controller"

    auto_switch = ft.Switch(label="Auto Mode", value=True)
    led_switch = ft.Switch(label="LED On/Off", value=False)
    fan_switch = ft.Switch(label="Fan On/Off", value=False)
    motion_text = ft.Text("Motion: Unknown")

    def send_control(_):
        data = {
            "auto": auto_switch.value,
            "led_on": led_switch.value,
            "fan_on": fan_switch.value
        }
        try:
            requests.post(API_URL, json=data)
        except:
            pass

    def refresh_status(_):
        try:
            motion_response = requests.get(MOTION_URL)
            motion = motion_response.json().get("motion", False)
            motion_text.value = "Motion: Detected" if motion else "Motion: None"
            page.update()
        except:
            motion_text.value = "Motion: Error"

    auto_switch.on_change = send_control
    led_switch.on_change = send_control
    fan_switch.on_change = send_control

    refresh_btn = ft.ElevatedButton("Refresh Motion", on_click=refresh_status)

    page.add(
        ft.Column([
            auto_switch,
            led_switch,
            fan_switch,
            motion_text,
            refresh_btn
        ])
    )

ft.app(target=main)
