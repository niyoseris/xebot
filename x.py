import requests
import time
import json
import sys
import sma_indicator
import rsi

headers = {
    "accept": "application/json",
    "Authorization": "Basic xxxxx",
    "Content-Type": "application/json"

}


usdt_balance = 0

#satis katsayisi alis x kar yuzdesi
satKat = 1.05 * 1.002 * 1.002



def get_sma(pair):
    return sma_indicator.sma_indicator(pair)

def get_rsi(pair):
    return rsi.get_rsi(pair, 150, 15)
 
    

    



def piyasa_durumu():
    piyasa = []
    url = "https://api.xeggex.com/api/v2/summary"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            
            # Sort the list of elements based on 'price_change_percent_24h'
            sorted_data = sorted(data, key=lambda x: x.get('base_volume', 0), reverse=True)
            
            """
            # Iterate through and print the sorted list
            for eleman in sorted_data:
                if "_USDT" in eleman["trading_pairs"]:
                    if len(piyasa) < 50:
                        piyasa.append(eleman)
            """

            for eleman in sorted_data:
                if eleman["price_change_percent_24h"] < 5:
                    if "_USDT" in eleman["trading_pairs"]:
                        if len(piyasa) < 100:
                            piyasa.append(eleman)

            return piyasa
        
        else:
            print (f"HTTP Error {response.status_code}: {response.reason} piyasa")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print (f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")


def coin_hemen_sat(ne):
    url = "https://api.xeggex.com/api/v2/summary"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            
            # Sort the list of elements based on 'price_change_percent_24h'
            sorted_data = sorted(data, key=lambda x: x.get('price_change_percent_24h', 0), reverse=True)
            
            # Iterate through and print the sorted list
            for eleman in sorted_data:
                if eleman["trading_pairs"] == ne + "_USDT":
                    return (eleman["highest_bid"])
            
        else:
            print (f"HTTP Error {response.status_code}: {response.reason} { str(response) } hemen sat")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print (f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")




def kese():
    url = "https://api.xeggex.com/api/v2/balances"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            
            # Sort the list of elements based on 'price_change_percent_24h'
            
            # Iterate through and print the sorted list
            for eleman in data:
                if float(eleman["available"]) > 0:
                    yukselenler(eleman["asset"], eleman['available'])
            
        else:
            print (f"HTTP Error {response.status_code}: {response.reason}, {str(eleman)}")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print (f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")


def yukselenler(neyi, ne_kadar):
    url = "https://api.xeggex.com/api/v2/gettrades?symbol=" + neyi + "%2FUSDT&limit=1&skip=0"

    try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Parse the JSON response
                data = json.loads(response.text)
                
                # Sort the list of elements based on 'price_change_percent_24h'
                
                # Iterate through and print the sorted list
                for eleman in data:
                    try:
                        fiyat = float(eleman["price"]) 
                        sat_fiyat = float(fiyat) * satKat
                        sat_fiyat = f"{sat_fiyat:.8f}"
                        print(f"{neyi}/USDT", f"{ne_kadar}", sat_fiyat)

                        float(ne_kadar)
                        sat(f"{neyi}", f"{ne_kadar}", sat_fiyat)
                        time.sleep(3)
                        """
                        if (float(eleman["price"]) * float(ne_kadar) * 1.002) < (float(coin_hemen_sat(neyi)) * float(ne_kadar)) * 0.998 :
                            #print (eleman["market"]["symbol"])
                            sat(neyi, ne_kadar, coin_hemen_sat(neyi))
                            order_sil(neyi)
                        """

                    except:
                        order_sil(neyi)

                        pass                
            else:
                print (f"HTTP Error {response.status_code}: {response.reason}, { str(response) } yükselen")

    except requests.exceptions.RequestException as e:
            # Handle request-related exceptions
            print (f"Request Exception: {e}")

    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")




def sat(market, miktar, fiyat):

    url = "https://api.xeggex.com/api/v2/createorder"

    if market == "XPE":
        return

    data = {
        "userProvidedId": None,
        "symbol": f"{market}/USDT",
        "side": "sell",
        "type": "limit",
        "quantity": f"{miktar}",
        "price": f"{fiyat}",
        "strictValidate": False
    }
    

    try:
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        

        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()
            print(f"{market} satdık biraz...")
        else:
            if not "Missing input" in str(response.json()):
                print(f"HTTP Error {response.status_code}: {response.reason}, { str(response) } sat")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print(f"Request Exception: {e}")



def al(market, miktar, fiyat):

    if order_var_mi(market) == False:

        url = "https://api.xeggex.com/api/v2/createorder"


        data = {
            "userProvidedId": None,
            "symbol": f"{market}/USDT",
            "side": "buy",
            "type": "limit",
            "quantity": f"{miktar}",
            "price": f"{fiyat}",
            "strictValidate": False
        }
        

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            

            if response.status_code == 200:
                # Parse the JSON response
                response_data = response.json()

                time.sleep(5)
                
                print(market)
                print("leddi")
                fiyat = f"{fiyat}" 
                sat_fiyat = float(fiyat) * satKat
                sat_fiyat = f"{sat_fiyat:.8f}"
                print(f"{market}/USDT", f"{miktar}", sat_fiyat)

                for q in range(5):
                    sat(f"{market}", f"{miktar}", sat_fiyat)
                time.sleep(5)
                for q in range(5):
                    sat(f"{market}", f"{miktar}", sat_fiyat)

                order_sil(market)
            else:
                if not "Missing input" in str(response.json()):
                    print(f"HTTP Error {response.status_code}: {str(response)} {market}")

        except requests.exceptions.RequestException as e:
            # Handle request-related exceptions
            print(f"Request Exception: {e}")
    else:
        print(f"order var {market}")


def get_usdt():
    url = "https://api.xeggex.com/api/v2/balances"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            
            # Sort the list of elements based on 'price_change_percent_24h'
            
            # Iterate through and print the sorted list

            for eleman in data:
                if str(eleman["asset"]) == "USDT":
                    usdt = float(eleman["available"]) * 1
                    formatted_usdt = f"{usdt:.10f}"  # Format with 10 decimal places
                    return formatted_usdt   
        else:
            print (f"HTTP Error {response.status_code}: {response.reason}")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print (f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")



def elde_var_mi(ne):

    #order_sil_sat(ne)


    url = "https://api.xeggex.com/api/v2/balances"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            
            # Sort the list of elements based on 'price_change_percent_24h'
            
            # Iterate through and print the sorted list

            for eleman in data:
                if str(eleman["asset"]) == "USDT":
                    usdt = float(eleman["available"]) * 1
                    formatted_usdt = f"{usdt:.10f}"  # Format with 10 decimal places
                    usdt_balance = formatted_usdt

            for eleman in data:
                if str(eleman["asset"]) == ne:
                    if float(eleman["available"]) > 0:
                        return True
                    else:
                        return False
                    
                
        else:
            print (f"HTTP Error {response.status_code}: {response.reason} { str(response) } elde var mı")

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print (f"Request Exception: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print (f"JSON Decode Error: {e}")


def order_var_mi(ne):


    url = f"https://api.xeggex.com/api/v2/getorders?symbol={ne}%2FUSDT&status=active&limit=1&skip=0"

    response = requests.get(url, headers=headers)


    if str(response.text) == "[]":
        return False
    else:
        return True
    

def order_sil_sat(ne):
    url = "https://api.xeggex.com/api/v2/cancelallorders"

    sat_iptal = {
    "symbol": f"{ne}/USDT",
    "side": "SELL"
    }

    response = requests.post(url, headers=headers, data=json.dumps(sat_iptal))

    print("sat iptal: " + str(response.text))




def order_sil(ne):


    url = "https://api.xeggex.com/api/v2/cancelallorders"


    al_iptal = {
    "symbol": f"{ne}/USDT",
    "side": "BUY"
    }


    response = requests.post(url, headers=headers, data=json.dumps(al_iptal))
    
    print("Al iptal: " + str(response.text))


    """responsat = requests.post(url, headers=headers, data=json.dumps(sat_iptal))

    print("Sat iptal: " + ne + str(responsat.text))"""







for z in piyasa_durumu():
    ticker = str(z["trading_pairs"]).replace("_USDT","")

    rr = rsi.get_rsi(ticker, 150, 15)



    if elde_var_mi(ticker) == False:
        if order_var_mi(ticker) == False:
            try:
                print(ticker)
                if float(z['lowest_ask']) / float(z['highest_bid']) < 1.002:
                    kac_usdt = float(get_usdt()) / 10
                    lowest = z["lowest_ask"]
                    kac_usdt = f"{kac_usdt:.10f}"  # Format with 10 decimal places
                    

                    #lowest = f"{lowest:.10f}"  # Format with 10 decimal places

                    mik = float(kac_usdt) / float(z["lowest_ask"])

                    mik = f"{mik:.8f}"
                    print(f"{ticker} --> sma: {get_sma(ticker)}  rsi:{get_rsi(ticker)}")


                    #eldeki usdt miktarina gore lowesttan alim yapar.
                    if float(get_usdt()) > 1:
                        if float(get_rsi(ticker)) < 30 and float(get_sma(ticker)) > 0:
                            print(f"{ticker} --> sma: {get_sma(ticker)}  rsi:{get_rsi(ticker)}")
                            al(ticker, mik, lowest)
                    else:
                        print("baram yoq")
            except:
                pass
kese()
print("\n")
print("over.")
print("\n")
