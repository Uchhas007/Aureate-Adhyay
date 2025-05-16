import platform
import requests


def run():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()

        location = (
            f'IP Address: {ip_data.get("ip")}, '
            f'City: {ip_data.get("city")}, '
            f'Region: {ip_data.get("region")}, '
            f'Country: {ip_data.get("country")}, '
            f'Location (Lat, Long): {ip_data.get("loc")}'
        )

        os_info = platform.platform()
        return location, os_info

    except Exception as e:
        return "Error fetching data", str(e)


if __name__ == "__main__":
    loc, os_info = run()
