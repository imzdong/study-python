from langchain_community.document_loaders import PyPDFLoader

if __name__ == '__main__':
    file_path = "lyqd.pdf"
    loader = PyPDFLoader(file_path)

    docs = loader.load()

    print(len(docs))

