import os
from filter_move_file import copy_html_files
from fill_insert_toc import generate_toc
from final_html import move_files_to_target
from ebook import make_ebook

def main():

    base_path = "/Users/admin/Downloads/"
    # 定义源目录和目标目录
    source_directory = base_path + "212-100099801-专栏课-郭东白-郭东白的架构课（完结）"
    
    temp_directory = base_path + "/mobile-book/郭东白的架构课"
    tem_destination_directory = "/Users/admin/Downloads/mobile-book/郭东白的架构课-123"
    destination_directory = "/Users/admin/Downloads/mobile-book/郭东白的架构课-mobi"

    
    # 1. 首先执行文件过滤和移动
    print("Step 1: 开始过滤和移动文件和重命名文件...")
    copy_html_files(source_directory, temp_directory)
    print("文件过滤和移动和重命名文件完成\n")

    # 2. 生成目录结构
    print("Step 2: 开始生成目录结构...")
    generate_toc(temp_directory)
    print("目录结构生成完成")

    # 3. Generate final HTML
    print("Step 3: Generating final HTML...")
    move_files_to_target(temp_directory, tem_destination_directory)
    print("Final HTML generation completed")

    # 4. Generate mobi
    print("Step 4: Generating mobi...")
    #make_ebook(str(tem_destination_directory), destination_directory, format='mobi')
    print("mobi generation completed")

    # 5.删除临时目录
    print("Step 5: 删除临时目录...")
    #os.system(f"rm -rf {temp_directory}")
    #os.system(f"rm -rf {tem_destination_directory}")
    print("All steps completed!")

if __name__ == "__main__":
    main()