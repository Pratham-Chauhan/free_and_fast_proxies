import os.path
import time
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
import csv

lock = threading.Lock()

def download_free_proxies():
    proxysourcebox = [
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt']

    headersproxy = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'}

    lis = []
    # get free proxies
    for y in proxysourcebox:
        # , verify=False)
        pageprox = requests.get(url=y, timeout=200, headers=headersproxy)
        soupprox = BeautifulSoup(pageprox.content, 'lxml')

        print("Proxy Source:", pageprox.url)
        for i in soupprox.text.split('\n'):
            lis.append('http://' + i)
    return lis



# Another way - https://geonode.com/free-proxy-list
def download_free_proxies2():
    lis = []
    df = pd.read_csv("./Free_Proxy_List.csv")
    for i, row in df.iterrows():
        url = "{}://{}:{}".format(row['protocols'], row['ip'], row['port'])
        lis.append(url)

# proxies = pd.read_csv('./fast_proxies_list.csv', header=None)[0].to_list()
proxies = download_free_proxies()


def measure_proxy_speed(proxy_url):
    global c, failed
    c += 1
    print(f"Thread Started: {c}/{proxy_num} | Found: {len(res)} | Failed: {failed}", end="\r")

    # Set the proxy URL
    proxy = {
        "http": proxy_url,
        "https": proxy_url
    }
    # print(proxy['http'])

    start_time = time.time()

    for _ in range(n):
        try:
            response = requests.get('https://example.com/', proxies=proxy, timeout=tolerate_time)
            if response.status_code != 200:
                failed += 1
                return
        except Exception as e:
            failed += 1
            # print(e)
            return
        
    end_time = time.time()
    diff = end_time - start_time
    diff = diff/n

    # Save the data to a CSV file
    with lock:
        with open('fast_proxies.csv', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([proxy_url, diff])

    print(f"Proxy: {proxy_url:^30}, Response Time: {diff:^20.3f} seconds")
    res.append((proxy_url, diff))


''' MAIN '''
print("Proxy Count:", len(proxies), '\n')

# Create the CSV file
with open('fast_proxies.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

c = 0  # thread counter
failed = 0 # failed count
n = 2 # successive number of requests
tolerate_time = 10  # in seconds
proxy_num = 5000

if proxy_num > len(proxies):
    proxy_num = len(proxies)

res = []    # good proxies list

random_sub_proxies = random.sample(proxies, proxy_num)

with ThreadPoolExecutor(16) as executor:
    executor.map(measure_proxy_speed, random_sub_proxies)

# for i in random_sub_proxies:
#     measure_proxy_speed(i)

print(f"Thread Started: {c}/{proxy_num} | Found: {len(res)} | Failed: {failed}")

if res:
    df = pd.read_csv('fast_proxies.csv', header=None)
    df = df.sort_values(1)

    # fast_proxies = df[0].to_list()
    df.reset_index(drop=True, inplace=True)
    df.to_csv('fast_proxies.csv', index=False, header=False)
