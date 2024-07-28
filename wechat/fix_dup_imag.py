import os
from bs4 import BeautifulSoup
from collections import Counter
import shutil

rootPath = 'D:\\WorkSpace\\idea\\python\\wechat\\html-dup-r'
rootPathdup = 'D:\\WorkSpace\\idea\\python\\wechat\\html-dup-r'

def has_duplicates(lst):
    return len(lst) != len(set(lst))

if __name__ == '__main__':
    file_names = [f for f in os.listdir(rootPath) if os.path.isfile(os.path.join(rootPath, f))]

    print("Files found:")
    #rint(file_names)

    for name in file_names:
        print(f'## {name}')
        file_path = os.path.join(rootPath, name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        dd = soup.find('div', attrs={'id': 'js_content'})
        if dd:
            images = [img for img in dd.find_all('img')]
            image_links = [each.get('data-src') for each in images]

            # 计算每个data-src值出现的次数
            data_src_counts = Counter(image_links)

            # 找出重复的data-src值
            repeated_data_src = [data_src for data_src, count in data_src_counts.items() if count > 1]
            if repeated_data_src:
                #print(repeated_data_src)
                ss = soup.find('img', {'data-src': repeated_data_src})['src']
                #print(ss)
                for img in images:
                    # 检查data-src是否在重复的列表中
                    if 'data-src' in img.attrs and img['data-src'] in repeated_data_src:
                        #img['src'] = ss
                        #print(img['src'])
                        # 替换src属性
                        img['src'] = ss
                #shutil.copy(file_path, rootPathdup+"\\"+name)


        #with open(rootPathdup+'\\'+name, "wt", encoding=("utf-8")) as f:
        #    f.write(soup.prettify())
    print("end")