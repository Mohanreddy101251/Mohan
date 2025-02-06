import os
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
os.environ["OPENAI_API_KEY"] = 'your-api-key'

def main():
    path=r"Test_Hippa.pdf"
    documents= load_split_data(path)
    add_to_db(documents)
    
def load_split_data(path):
    all_chunks=[]
    with pdfplumber.open(path) as pdf:
        
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=90,
            length_function=len
        )
        
        for page_num,page in enumerate(pdf.pages):
            text=page.extract_text()
            if text:
              chunks= text_splitter.split_text(text)
              for chunk in chunks:
              
                  all_chunks.append({"page_content:":chunk, "metadata:":page_num+1})
            
    return all_chunks
    
def add_to_db(documents):
    embedding_func=OpenAIEmbeddings()
    db=Chroma(persist_directory='./chroma_db',embedding_function=embedding_func)
    
    docs_with_ids = [
        Document(page_content=doc['page_content:'], metadata={"id": id})
        for id, doc in enumerate(documents)
    ]
    
    # Add all documents at once
    db.add_documents(docs_with_ids)
    # db.persist() 
    print("Changes are saved and update to Chroma Db")

if __name__=="__main__":
    main()
    