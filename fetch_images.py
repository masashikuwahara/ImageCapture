import os
import requests
from bs4 import BeautifulSoup

def fetch_images_by_keyword(url, save_folder, keyword):
    # ウェブページのHTMLを取得
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        return

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')

    # キーワードを含むコンテキストを検索
    keyword_tags = soup.find_all(string=lambda text: text and keyword in text)

    # キーワード近くの画像を収集
    img_urls = set()
    for tag in keyword_tags:
        # キーワードを含むタグの親タグを検索
        parent_tag = tag.find_parent()
        if not parent_tag:
            continue
        
        # 親タグ内の画像タグを収集
        img_tags = parent_tag.find_all('img')
        for img in img_tags:
            if 'src' in img.attrs:
                img_urls.add(img['src'])

    # 画像を保存するフォルダを作成
    os.makedirs(save_folder, exist_ok=True)

    # 画像をダウンロードして保存
    for idx, img_url in enumerate(img_urls):
        # 完全なURLを作成
        if not img_url.startswith(('http://', 'https://')):
            img_url = requests.compat.urljoin(url, img_url)
        
        try:
            img_response = requests.get(img_url)
            img_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to download image {img_url}. Error: {e}")
            continue

        # 画像のファイル名を生成して保存
        img_name = os.path.join(save_folder, f'image_{idx + 1}.jpg')
        with open(img_name, 'wb') as f:
            f.write(img_response.content)

        print(f"Image {idx + 1} saved as {img_name}")

if __name__ == "__main__":
    url = input("URLを入力: ")
    save_folder = input("保存するフォルダ名を入力: ")
    keyword = input("何かキーワードがあれば入力: ")
    fetch_images_by_keyword(url, save_folder, keyword)
    input("終了しました")
