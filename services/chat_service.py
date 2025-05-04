
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import sacrebleu

from core.config import settings  # type: ignore


class ChatService:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )

        # Load and combine documents from both CSV files
        csv_path_1 = "/home/sharan/projects/workspace/interview_task/services/HRM_master_Dataset.csv"
        csv_path_2 = "/home/sharan/projects/workspace/interview_task/services/Work_summary.csv"
        loader_1 = CSVLoader(file_path=csv_path_1)
        loader_2 = CSVLoader(file_path=csv_path_2)
        data_1 = loader_1.load()
        data_2 = loader_2.load()
        self.data = data_1 + data_2  # Combine the data

        # Split combined documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE
        )
        self.docs = self.text_splitter.split_documents(self.data)

        # Create or load vector store
        self.vectorstore = Chroma.from_documents(
            documents=self.docs,
            embedding=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )

        # Initialize LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=settings.GROQ_API_KEY
        )

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # Create conversational chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    def get_response(self, question: str) -> dict:
        """Get response from the chatbot for a given question."""
        result = self.qa_chain({"question": question})
        return result
    def calculate_bleu(reference: str, candidate: str) -> float:
        bleu = sacrebleu.corpus_bleu([candidate], [[reference]])
        return bleu.score