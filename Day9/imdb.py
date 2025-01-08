import requests
import urllib.parse
import json
from bs4 import BeautifulSoup
from proxies import get_smart_proxy_agent

def get_smart_proxy_agent():
    username = urllib.parse.quote("xxxxxxxx")  # Replace with your username
    password = urllib.parse.quote("xxxxxxxx")  # Replace with your password
    proxy = "xxxxxxxxxx"  # Proxy address

    return {
        "http": f"http://{username}:{password}@{proxy}",
        "https": f"http://{username}:{password}@{proxy}",
    }

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

def scrape_imdb_with_session():
    proxies = get_smart_proxy_agent()  # Get proxy configuration

    url = "https://m.imdb.com/name/nm0000129/?ref_=nv_sr_srsg_0_tt_0_nm_8_in_0_q_TOM%2520"

    try:
        response = requests.get(url, timeout=10, proxies=proxies, headers=headers)
        if response.status_code == 200:
            print("IMDb Page fetched successfully.")
            with open("test.html", "w", encoding="utf-8") as html_file:
                html_file.write(response.text)
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")
        
        # Extract __NEXT_DATA__ script content
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag:
            script_content = script_tag.string
            json_data = json.loads(script_content)
            
            # Save JSON data to file
            with open("test.json", "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=2)
            
            # Extract specific JSON data
             # Extract specific JSON data
            try:
                caption_text = json_data["props"]["pageProps"]["mainColumnData"]["titleMainImages"]["edges"][6]["node"]["caption"]["plainText"]
                print("Caption Text:", caption_text)
            except KeyError as e:
                print("Key not found in JSON:", e)
            else:
                print("__NEXT_DATA__ script tag not found.")
        else:
            print(f"Failed to fetch IMDb page. Status Code: {response.status_code}")
            print("Response Content:", response.text[:500])  # Display partial response content for debugging
    except requests.exceptions.ProxyError as e:
        print("Proxy Error:", e)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    scrape_imdb_with_session()
            
        