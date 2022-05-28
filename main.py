import math

import requests
import time

headers = requests.utils.default_headers()

headers.update({
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36",
    "accept-encoding": "gzip, deflate",
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
})


def get_data():
    req = requests.get(
        'http://192.168.0.12:8080/get?magAccuracy&magX&magY',
        headers=headers)

    res = req.json()
    try:
        mag_x = res['buffer']['magX']['buffer'][0]
        mag_y = res['buffer']['magY']['buffer'][0]
    except:
        return 0, 0
    return mag_x, mag_y


def calculate_angle(x, y):
    angle = math.atan2(x, y) * 180 / math.pi
    if angle > 0:
        return 360 - angle
    return -angle


def compas(angle):
    if angle > 337.25 or angle < 22.5:
        return "North (Север)"
    elif 292.5 < angle < 337.25:
        return "North-West (Северо-Запад)"
    elif 247.5 < angle < 292.5:
        return "West (Запад)"
    elif 202.5 < angle < 247.5:
        return "South-West (Юго-Запад)"
    elif 157.5 < angle < 202.5:
        return "South (Юг)"
    elif 112.5 < angle < 157.5:
        return "South-East (Юго-Восток)"
    elif 67.5 < angle < 112.5:
        return "East (Восток)"
    elif 0 < angle < 67.5:
        return "North-East (Северо-Восток)"


def main():
    while True:
        mag_x, mag_y = get_data()
        angle = calculate_angle(mag_x, mag_y)
        side = compas(angle)
        print(angle, side)

        time.sleep(0.2)


if __name__ == '__main__':
    main()
