import requests
from bs4 import BeautifulSoup

# BBC 6 Minute English的主页URL
url = 'https://www.bbc.co.uk/learningenglish/english/features/6-minute-english/ep-180111'

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890'
}

if __name__ == '__main__':
    # 发送请求并获取页面内容
    response = requests.get(url, proxies=proxies)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有的episode链接
    episodes = soup.find_all('a', class_='download')

    # 遍历每个episode链接，获取PDF和音频地址
    for episode in episodes:
        episode_url = episode['href']
        episode_response = requests.get(episode_url)
        episode_soup = BeautifulSoup(episode_response.content, 'html.parser')

        # 查找PDF下载链接
        pdf_link = episode_soup.find('a', string='Download PDF')
        audio_link = episode_soup.find('a', string='Download Audio')

        if pdf_link and audio_link:
            print(f"Episode: {episode.text.strip()}")
            print(f"PDF URL: {pdf_link['href']}")
            print(f"Audio URL: {audio_link['href']}")
            print()