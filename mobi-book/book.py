from ebook import make_ebook

def main():
    tem_destination_directory = "/Users/admin/Downloads/mobile-book/6"
    destination_directory = "/Users/admin/Downloads/mobile-book/郭东白的架构课-mobi"
    make_ebook(str(tem_destination_directory), destination_directory, format='mobi');

if __name__ == "__main__":
    main()