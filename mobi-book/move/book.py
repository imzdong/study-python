from ebook import make_ebook

def main():
    tem_destination_directory = "D:\\BaiduNetdiskDownload\\mobile-book\\郭东白的架构课-final"
    destination_directory = "D:\\BaiduNetdiskDownload\\mobile-book\\郭东白的架构课-mobi"
    make_ebook(str(tem_destination_directory), destination_directory, format='mobi');

if __name__ == "__main__":
    main()