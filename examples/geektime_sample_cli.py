# coding=utf8

import pathlib

from ebook import make_ebook

if __name__ == '__main__':
    src_folder = 'D:\\WorkSpace\\Idea\\S\\python\\251\\final\\source'
    dest_folder = 'D:\\WorkSpace\\Idea\\S\\python\\251\\final\\dest'
    make_ebook(str(src_folder), dest_folder, format='mobi')
    #make_ebook(str(src_folder), dest_folder, format='epub')
