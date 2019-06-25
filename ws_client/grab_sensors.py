""" Websocket client. Used to run as a service, for obtain data from sensors """
import asyncio
import datetime
import pathlib
from typing import Any, AnyStr, Dict

import Adafruit_DHT
import aiohttp
import aiosqlite
import mh_z19
import yaml


def load_config(filename : AnyStr) -> Dict:
    """
    Load config of our app
    :param filename:
    :return:
    """
    project_root = pathlib.Path(__file__).parent

    with open(f"{project_root}/{filename}", "rt") as file:
        data = yaml.safe_load(file)
    data["URL"] = f"http://{data['HOST']}:{data['PORT']}/ws"
    sensors_map = {
        "11": Adafruit_DHT.DHT11,
        "22": Adafruit_DHT.DHT22,
        "2302": Adafruit_DHT.AM2302,
    }

    data["ADAFRUIT_SENSOR_TYPE"] = sensors_map[str(
        data["ADAFRUIT_SENSOR_TYPE"])]
    data["URL"] = f"http://{data['HOST']}:{data['PORT']}/ws"

    return data


CONFIG = load_config("config.yaml")


async def send_to_socket(data: Any, url: AnyStr) -> None:
    """
    Send data to socket.
    :param data:
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as websocket:
            await websocket.send_json(data)


async def main() -> None:
    """
    Main loop
    :return:
    """
    while True:
        print("Loop through sensors")
        mhz19_data = mh_z19.read()
        humidity, temperature = Adafruit_DHT.read_retry(
            CONFIG["ADAFRUIT_SENSOR_TYPE"], CONFIG["ADAFRUIT_SENSOR_PIN"]
        )
        print("Data received, packing")
        data = {
            "co2": mhz19_data["co2"],
            "temperature": temperature,
            "humidity": humidity,
            "time": datetime.datetime.now().timestamp(),
        }
        async with aiosqlite.connect(CONFIG["DB_PATH"]) as database:
            print("Writing to database")
            await database.execute(
                "INSERT INTO main.testimony VALUES (:co2,:temperature,:humidity,:time)",
                data,
            )
            await database.commit()

        try:
            print(data)
            await send_to_socket(data, CONFIG["URL"])
        except aiohttp.client_exceptions.ClientConnectorError:
            print("Socket not reachable")
            send_string = f"""CO2 level - {mhz19_data['co2']}.\
            Temperature - {temperature}.\
            Humidity - {humidity}"""
            print(send_string)
        print("Sleeping for {}".format(CONFIG["FREQUENCY"]))
        await asyncio.sleep(CONFIG["FREQUENCY"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("LOOP started")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bye!")
