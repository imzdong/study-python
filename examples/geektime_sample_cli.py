# coding=utf8

import pathlib

from ebook import make_ebook

if __name__ == '__main__':
    src_folder = 'D:\\Download\\Crawler\\2018-2021\\2018-handler'
    dest_folder = 'D:\\Download\\Crawler\\2018-2021\\dest'
    make_ebook(str(src_folder), dest_folder, format='mobi')
    #make_ebook(str(src_folder), dest_folder, format='epub')
