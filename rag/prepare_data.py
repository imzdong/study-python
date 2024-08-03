import os

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file):
    """
    加载PDF、DOC、TXT文档
    :param file:
    :return:
    """
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        loader = UnstructuredFileLoader(file)
    else:
        print('Document format is not supported!')
        return None
    data = loader.load()
    return data


def chunk_data(data, chunk_size=256, chunk_overlap=150):
    """
    将数据分割成块
    :param data:
    :param chunk_size: chunk块大小
    :param chunk_overlap: 重叠部分大小
    :return:
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks
