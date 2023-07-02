import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "ZrFkfTBydY20dtmofOmsHmZ1vrlln6bN"

while True:
    orig = input("Ubicación inicial: ")
    if orig == "quit" or orig == "Q":
        break
    dest = input("Destino: ")
    if dest == "quit" or dest == "Q":
        break
    fuelUsed = float(input("Rendimiento del vehículo en km/l: "))

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest, "locale": "es_ES"})
    json_data = requests.get(url).json()
    print("URL: " + url)

    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + str(json_status) + " = Una llamada de ruta exitosa.\n")
        print("=============================================")
        print("Dirección desde " + orig + " a " + dest + ":")
        print("Duración del viaje: " + json_data["route"]["formattedTime"])
        print("Kilómetros:      " + "{:.3f}".format(json_data["route"]["distance"] * 1.61))
        distancia_km = json_data["route"]["distance"] * 1.61
        litros_combustible = distancia_km / fuelUsed * 3.78
        print("Combustible utilizado: " + "{:.3f}".format(litros_combustible))
        print("=============================================")
        narrative = json_data["route"]["legs"][0]["maneuvers"]
        for each in narrative:
            print(each["narrative"] + " (" + "{:.2f}".format(each["distance"] * 1.61) + " km)")
        print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Alguna ubicación no es válida.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; No ha ingresado una o ambas ubicaciones.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print(" https://developer.mapquest.com/documentation/directions-api/status-codes ")
        print("****************************************************************************\n")
