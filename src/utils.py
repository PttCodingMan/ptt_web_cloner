import os.path

import scrapy


def save_page(domain, response: scrapy.http.Response):
    url = response.url
    if not url.startswith(domain):
        return

    file_name = f"../ptt_web/{url[len(domain):]}"
    if os.path.exists(file_name):
        return

    file_path = file_name[:file_name.rfind('/') + 1]

    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    with open(file_name, 'w') as f:
        f.write(response.text)
