import os
import hashlib
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain.globals import set_verbose

# Set verbosity level
set_verbose(True)

# Initialize the local model
llm = OllamaLLM(model="mistral")

# Function to hash the PDF file based on its contents
def hash_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        file_data = f.read()
        return hashlib.md5(file_data).hexdigest()

# Load PDF data from file paths
def load_pdf_data(pdf_file_paths):
    documents = []
    for pdf_file_path in pdf_file_paths:
        print(f"Attempting to load file: {pdf_file_path}")
        try:
            if not os.path.exists(pdf_file_path):
                print(f"File does not exist: {pdf_file_path}")
                continue

            loader = PyMuPDFLoader(pdf_file_path)
            docs = loader.load()

            if not docs:
                print(f"No content found in {pdf_file_path}. Please check the file.")
            else:
                print(f"Successfully loaded: {pdf_file_path}")
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading {pdf_file_path}: {str(e)}")
    return documents

# Function to check if vector data for a PDF exists in the vectorstore using metadata
def check_existing_vectors(pdf_hash, vectorstore):
    results = vectorstore.similarity_search_with_score(pdf_hash, k=1)
    return len(results) > 0

# Function to retrieve vectors by PDF hash
def retrieve_vectors(pdf_hash, vectorstore):
    return vectorstore.similarity_search(pdf_hash, k=1)

# Initialize session-like state for chat history
chat_history = []

# PDF file to load 
pdf_files = ['1003000265.pdf']

# Hash the PDF file
pdf_hash = hash_pdf(pdf_files[0])

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200, add_start_index=True)

# Initialize embeddings and vector store
embedding = OllamaEmbeddings(model="nomic-embed-text")

# Specify the directory for persistent storage
PERSISTENT_DIR = "./chroma_vectors"
# Initialize the Chroma vector store with persistent storage
vectorstore = Chroma(embedding_function=embedding, persist_directory=PERSISTENT_DIR)

# Check if vectors for this PDF already exist in the vector store
if not check_existing_vectors(pdf_hash, vectorstore):
    # Load and process the PDFs
    docs = load_pdf_data(pdf_files)
    if docs:
        all_splits = text_splitter.split_documents(docs)

        # Add the new document's splits into the vectorstore with metadata
        vectorstore.add_texts([doc.page_content for doc in all_splits], metadatas=[{"pdf_hash": pdf_hash}] * len(all_splits))

        print(f"New vectors added and stored for {pdf_files[0]}")
    else:
        print(f"Failed to load any valid content from {pdf_files[0]}")
else:
    print(f"Vector data already exists for {pdf_files[0]}, skipping reprocessing.")
    # Retrieve existing vectors for this PDF
    all_splits = retrieve_vectors(pdf_hash, vectorstore)

# Contextualization chain
contextualize_q_system_prompt = """Given a chat history and the latest user question 
which might reference context in the chat history, formulate a standalone question 
which can be understood without the chat history. Do NOT answer the question, 
just reformulate it if needed and otherwise return it as is."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

# Question-answering chain
qa_system_prompt = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.\n\n{context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def contextualized_question(input: dict):
    if input.get("chat_history"):
        return contextualize_q_chain
    else:
        return input["question"]

# Combine retriever and question-answering into a single chain
rag_chain = (
    RunnablePassthrough.assign(context=contextualized_question | vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10}) | format_docs)
    | qa_prompt
    | llm
)

# Allow the user to keep asking questions until they type 'exit'
while True:
    question = input("Ask a question about the textbook (or type 'exit' to quit): ")

    if question.lower() == "exit":
        print("Exiting the program. Goodbye!")
        break

    # Process user question
    if question.strip():
        try:
            # Get AI response
            ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history})
            print("AI Response:", ai_msg)

            # Update chat history
            chat_history.append(HumanMessage(content=question))
            chat_history.append(AIMessage(content=ai_msg))
        except Exception as e:
            print(f"Error generating response: {str(e)}")
    else:
        print("Please enter a question before submitting.")