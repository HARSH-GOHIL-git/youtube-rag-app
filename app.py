import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEndpointEmbeddings

# --- Page Configuration ---
st.set_page_config(page_title="YouTube Q&A Bot", page_icon="🎥")
st.title("🎥 YouTube Transcript Q&A Bot")
st.markdown("Chat with any YouTube video using Llama-3.1 and LangChain!")

# --- Sidebar: Configuration ---
st.sidebar.header("Configuration")
hf_api_key = st.sidebar.text_input("Enter HuggingFace API Key:", type="password")

if hf_api_key:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_api_key

# Helper function to extract video ID from a full URL
def extract_video_id(url_or_id):
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1][:11]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1][:11]
    return url_or_id # Assume it is already just an ID

# --- Main App: Video Processing ---
video_input = st.text_input("Enter YouTube Video URL or ID:", placeholder="e.g., KGW8bQtcpJg")

if st.button("Process Video"):
    if not hf_api_key:
        st.warning("⚠️ Please enter your HuggingFace API key in the sidebar first.")
    elif not video_input:
        st.warning("⚠️ Please enter a Video ID or URL.")
    else:
        with st.spinner("Fetching transcript and building vector database..."):
            try:
                # 1. Fetch Transcript
                video_id = extract_video_id(video_input)
                transcript_list = YouTubeTranscriptApi().fetch(video_id,
                languages=['en', 'en-US', 'en-GB']
                )
                
                # Extract text from the dictionary format returned by get_transcript
                full_text = " ".join([snippet.text for snippet in transcript_list.snippets])

                # 2. Chunking
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = splitter.create_documents([full_text])

                # 3. Embeddings & Vector Store
                embedding = HuggingFaceEndpointEmbeddings(
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    task="feature-extraction"
                )
                vector_store = FAISS.from_documents(chunks, embedding)
                
                # Save the retriever in session state so it persists across questions
                st.session_state.retriever = vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                )
                
                st.success("✅ Video processed successfully! You can now ask questions below.")
            
            except Exception as e:
                st.error(f"❌ Error processing video: {e}")

# --- Main App: Q&A Interface ---
# Only show this section if a video has been successfully processed
if "retriever" in st.session_state:
    st.divider()
    st.subheader("Ask a Question")
    
    question = st.text_input("What would you like to know about this video?")
    
    if st.button("Get Answer") and question:
        with st.spinner("Generating answer..."):
            try:
                # Initialize LLM
                llm = HuggingFaceEndpoint(
                    repo_id="meta-llama/Llama-3.1-8B-Instruct",
                    # repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                    task="text-generation"
                )
                model = ChatHuggingFace(llm=llm)

                # Define Prompt
                prompt = PromptTemplate(
                    template="""
                    You are a helpful assistant.
                    Answer ONLY from the provided transcript context.
                    If the context is insufficient, just say you don't know.

                    Context: {context}
                    Question: {question}
                    """,
                    input_variables=['context', 'question']
                )

                # Retrieve Context
                context_docs = st.session_state.retriever.invoke(question)
                context_text = " ".join([doc.page_content for doc in context_docs])

                # Generate Answer
                final_prompt = prompt.invoke({"context": context_text, "question": question})
                result = model.invoke(final_prompt)
                
                # Display Answer
                st.info(result.content)
                
            except Exception as e:
                st.error(f"❌ Error generating answer: {e}")