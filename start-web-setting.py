from flask import Flask, render_template, request

import os
import json
import urllib3
from multiprocessing import Process

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

DEFAULT_LISTEN_ADDR = "0.0.0.0"
DEFAULT_LISTEN_PORT = 8080


@app.route("/", methods=["POST", "GET"])
def load_data():
    """LOAD data from data.json"""
    data_for_template = open("./static/data/data.json")
    datas = json.load(data_for_template)
    return render_template("webSetting.html", **datas)


@app.route("/formdata", methods=["POST", "GET"])
def get_data():
    if request.method == "POST":
        radioSelectionConnection = request.form.get("connection")
        SSID_Selected = request.form.get("inputSSID")
        PASSWORD_Selected = request.form.get("inputPASS")

        if str(radioSelectionConnection) == "WIFI":
            Connection = "WIFI"
        elif str(radioSelectionConnection) == "LAN":
            Connection = "LAN"
        elif str(radioSelectionConnection) == "WIFILAN":
            Connection = "ALL ACTIVE"

        data = {
            "CONNECTION": Connection,
            "SSID": str(SSID_Selected),
            "PASSWORD": str(PASSWORD_Selected),
        }

        datas_json = json.dumps(data)
        config_file = open("config.json", "w")
        config_file.write(datas_json)
        config_file.close()
        return render_template("save_screen.html", **data)


@app.route("/delete", methods=["POST", "GET"])
def delete_data():
    if os.path.exists("config.json"):
        os.remove("config.json")
        delete = "Config data has been remove"
    else:
        delete = "The Config file does not exist"

    data_delete = {"delete": delete}
    return render_template("delete_screen.html", **data_delete)


@app.route("/process", methods=["POST", "GET"])
def process_data():
    data_for_template = open("./static/data/data.json")
    datas = json.load(data_for_template)
    return render_template("webSetting.html", **datas)


if __name__ == "__main__":
    app.run(host=DEFAULT_LISTEN_ADDR, port=DEFAULT_LISTEN_PORT)
