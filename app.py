from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def scrape_images(search_keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    
    # 🔧 Required for Render
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    start_url = f"https://hotnakedwomen.com/ru/search/{search_keyword}/"
    driver.get(start_url)
    time.sleep(5)

    main_html = driver.page_source
    main_soup = BeautifulSoup(main_html, "html.parser")

    hrefs = []
    grid_divs = main_soup.find_all("div", class_="grid")
    for div in grid_divs:
        links = div.find_all("a", href=True)
        for a in links:
            href = a["href"]
            if href.startswith("http"):
                hrefs.append(href)
            else:
                hrefs.append("https://hotnakedwomen.com" + href)
            if len(hrefs) >= 2:
                break
        if len(hrefs) >= 2:
            break

    result = {}
    for idx, link in enumerate(hrefs, start=1):
        driver.get(link)
        time.sleep(5)

        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")

        image_links = []
        grids = page_soup.find_all("div", class_="grid")
        for grid in grids:
            for a in grid.find_all("a", href=True):
                href = a["href"]
                if any(href.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"]):
                    if href.startswith("http"):
                        image_links.append(href)
                    else:
                        image_links.append("https://hotnakedwomen.com" + href)

        image_links = list(dict.fromkeys(image_links))
        result[f"image_set_{idx}"] = image_links

    driver.quit()
    return result

@app.route('/scrape', methods=['POST'])
def scrape_endpoint():
    data = request.get_json(force=True)
    keyword = data.get('keyword')
    if not keyword:
        return jsonify({"error": "Missing 'keyword' in JSON body"}), 400

    try:
        result = scrape_images(keyword)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
