import requests
import json
import time
import ShellyPy
import urllib3


def json_web_query(url):
    """ Retrieve json information from a given URL """
#    import urllib3
#    import requests
    from requests.structures import CaseInsensitiveDict
    
    urllib3.disable_warnings() # avoid InsecureRequestWarning
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer eyJraWQiOiI3ZDEwMDA1ZC03ODk5LTRkMGQtYmNiNC0yNDRmOThlZTE1NmIiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiIxMjIyMDE4NTY3NzQiLCJpc3MiOiJFbnRyZXoiLCJlbnBoYXNlVXNlciI6Im93bmVyIiwiZXhwIjoxNzIwNDE1MjQ5LCJpYXQiOjE2ODg4NzkyNDksImp0aSI6ImQ1ODg2NjgxLTY1MTQtNDM5Yi04NDJkLWI2MjYwNTU4ZGNkZSIsInVzZXJuYW1lIjoidGl0dXNjaGlyaWxhQGdtYWlsLmNvbSJ9.eRKI4NWdxCsopfc4nSsqMD0Cfnc3tT3nQ42E6diixjjJyVuRQFxZEvmU6ADVOOLvG7Y2Y86WsI5oCVH1qORc5A"
    
    resp = requests.get(url, headers=headers, verify=False) # self-signed certificate
    #print(resp.status_code)
    return resp.json()
    
url = 'https://envoy.local/production.json'

# alocam adresele celor 3 switch-uri
adr1 = "192.168.1.31"
adr2 = "192.168.1.32"
adr3 = "192.168.1.33"
sw1 = ShellyPy.Shelly(adr1)
sw2 = ShellyPy.Shelly(adr2)
sw3 = ShellyPy.Shelly(adr3)


# alocam puterile consumatorilor:
pwr1 = 2000
pwr2 = 3000
pwr3 = 6000
dclj = -100
tstp = 53
oprim_tot = 65

# intram in bucla infinita:
while True:
# citim starea celor 3 switch-uri
    time.sleep(1)
    try:
        sw1_on = sw1.relay(0)['output']
        t100 = json.loads(requests.get('http://' + adr1 + '/rpc/Temperature.GetStatus?id=100').content)
        t101 = json.loads(requests.get('http://' + adr1 + '/rpc/Temperature.GetStatus?id=101').content)
        t100v = t100['tC']
        t101v = t101['tC']
        trel = sw1.relay(0)['temperature']['tC']
        print("releu:", trel, "grd.C  ", "retur 40l:", t100v, "grd.C  ", "900l:", t101v, "grd.G")
    except:
        print("nu pot citi 31")
    time.sleep(1)
    try:
        sw2_on = sw2.status()["relays"][0]["ison"]
    except:
        print("nu pot citi 32")        
    time.sleep(1)
    try:
        sw3_on = sw3.status()["relays"][0]["ison"]
    except:
        print("nu pot citi 33")
    time.sleep(1)

    print("sw1:", sw1_on,"   sw2:", sw2_on,"   sw3:", sw3_on)
# citim productia si import/export-ul
# result = requests.get(target_url)
# json_status = json.loads(result.text)
    json_status = json_web_query(url)

    p_now = json_status["production"][1]["wNow"]
    i_now = json_status["consumption"][1]["wNow"]
    print("productie:", p_now, "W")
    if i_now < 0:
        print("\033[1;32m                     export:  ", -i_now, "W")
    else:
        print("\033[1;31m                     import:   ", i_now, "W")

# calculam puterea disponibila:
    if sw1_on is False and sw2_on is False and sw3_on is False:
        disp_power = -i_now

    elif sw1_on is True and sw2_on is False and sw3_on is False:
        disp_power = pwr1 - i_now
    elif sw1_on is False and sw2_on is True and sw3_on is False:
        disp_power = pwr2 - i_now
    elif sw1_on is False and sw2_on is False and sw3_on is True:
        disp_power = pwr3 - i_now
    
    elif sw1_on is True and sw2_on is True and sw3_on is False:
        disp_power = pwr1 + pwr2 - i_now
    elif sw1_on is True and sw2_on is False and sw3_on is True:
        disp_power = pwr1 + pwr3 - i_now
    elif sw1_on is False and sw2_on is True and sw3_on is True:
        disp_power = pwr2 + pwr3 - i_now

    elif sw1_on is True and sw2_on is True and sw3_on is True:
        disp_power = pwr1 + pwr2 + pwr3 - i_now



    print("disponibil:", disp_power, "W")
# incepem calibrarea consumului:
    if t100v < oprim_tot:
        if disp_power < p_now:
# 1 --- 0 0 0
            if disp_power < pwr1-dclj or t101v > tstp:
                if sw1_on is True:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is True:
                    time.sleep(1)            
                    try:
                        sw2.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is True:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 33")
     
# 2 --- 1 0 0
            if disp_power >= pwr1-dclj and disp_power < pwr2-dclj and t101v < tstp:
                if sw1_on is False:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is True:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is True:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 33")

# 3 --- 0 1 0 -- de aici am scos and disp_power < pwr1+pwr2-dclj
            if disp_power >= pwr2-dclj and t101v < tstp:
                if sw1_on is True:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is False:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is True:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 33")

# 4 --- 1 1 0 de aici am scos 'and disp_power < pwr3-dclj'
            if disp_power >= pwr1+pwr2-dclj and t101v < tstp:
                if sw1_on is False:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is False:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is True:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 33")

# 5 --- 0 0 1
            if disp_power >= pwr3-dclj and disp_power < pwr1+pwr3-dclj and t101v < tstp:
                if sw1_on is True:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is True:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is False:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 33")

# 6 --- 1 0 1
            if disp_power >= pwr1+pwr3-dclj and disp_power < pwr2+pwr3-dclj and t101v < tstp:
               if sw1_on is False:
                   time.sleep(1)
                   try:
                       sw1.relay(0, turn=True)
                   except:
                       print("nu-i accesibil 31")

               if sw2_on is True:
                   time.sleep(1)
                   try:
                       sw2.relay(0, turn=False)
                   except:
                       print("nu-i accesibil 32")

               if sw3_on is False:
                   time.sleep(1)
                   try:
                       sw3.relay(0, turn=True)
                   except:
                       print("nu-i accesibil 33")

# 7 --- 0 1 1
            if disp_power >= pwr2+pwr3-dclj and disp_power < pwr1+pwr2+pwr3-dclj and t101v < tstp:
                if sw1_on is True:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=False)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is False:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is False:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 33")

# 8 --- 1 1 1
            if disp_power >= pwr1+pwr2+pwr3-dclj and t101v < tstp:
                if sw1_on is False:
                    time.sleep(1)
                    try:
                        sw1.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 31")

                if sw2_on is False:
                    time.sleep(1)
                    try:
                        sw2.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 32")

                if sw3_on is False:
                    time.sleep(1)
                    try:
                        sw3.relay(0, turn=True)
                    except:
                        print("nu-i accesibil 33")

        else:
            if sw1_on is True:
                time.sleep(1)
                try:
                    sw1.relay(0, turn=False)
                except:
                    print("nu-i accesibil 31")
            if sw2_on is True:
                time.sleep(1)
                try:
                    sw2.relay(0, turn=False)
                except:
                    print("nu-i accesibil 32")
            if sw3_on is False:
                time.sleep(1)
                try:
                    sw3.relay(0, turn=True)
                except:
                    print("nu-i accesibil 33")

    else:
        if sw1_on is True:
            time.sleep(1)
            try:
                sw1.relay(0, turn=False)
            except:
                print("nu-i accesibil 31")
        if sw2_on is True:
            time.sleep(1)
            try:
                sw2.relay(0, turn=False)
            except:
                print("nu-i accesibil 32")
        if sw3_on is True:
            time.sleep(1)
            try:
                sw3.relay(0, turn=False)
            except:
                print("nu-i accesibil 33")
                   
    print("------------------------------------------------------------")
    # secunde pana la ciclul urmator:
    time.sleep(30)
 