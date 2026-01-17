from pathlib import Path
from dotenv import load_dotenv
import os
from src.chat_session import ChatSession
from src.vector_store import VectorStore

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def main():
    load_dotenv(BASE_DIR.parent / ".env")
    api_key = os.getenv("API_KEY")
    model = "llama-3.1-8b-instant"

    store = VectorStore()
    chat = ChatSession(api_key=api_key, model=model)
    chat.system_prompt("You are a helpful assistant that summarizes audio transcriptions concisely and accurately.")       
    ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".m4a", ".webm"}

    transcription = None
    
    print('What do you want to do?')
    while True:
        user_msg = input()

        if user_msg == "/exit":
            break
        
        if user_msg == '/audio':
            while True:
                audio_file = input('Please, give path to your audio file: ')
                if ';' in audio_file:
                    audio_files = [Path(p.strip()) for p in audio_file.split(";") if p.strip()]
                else: 
                    audio_files = [Path(audio_file)]

                transcription = ""
                for file in audio_files:
                    if not file.exists() or file.suffix.lower() not in ALLOWED_EXTENSIONS:
                        print(f"Skipping '{file}' - file not found or invalid format.\n \
                            I work only with .mp3, .mp4, .mpeg, .mpga, .m4a, .wav, .webm.\n")
                        continue
                    else:
                        print('\nTranscription of audio:')
                        current_transcription = chat.transcript_with_whisper(file)
                        transcription += current_transcription + "\n\n"
                        store.add_transcript(current_transcription, str(file), DATA_DIR) 
                break
            continue


        if user_msg.startswith('/'):    
            if not transcription:
                print("The audio file is missing. Could you please provide it?")
                continue

            if user_msg == "/summary":
                print('Summary:\n')
                prompt = f'You have to summarize a transcription.\n \
                        Here is transcription: {transcription}'  
            elif user_msg == "/extract_keywords":
                print('Keywords:\n')
                prompt = f'You have to extract keywords from a transcription.\n \
                        Here is transcription: {transcription}'    
            elif user_msg == "/generate_title":
                print('Title:\n')
                prompt = f'Generate a title for transcription.\n \
                        Here is transcription: {transcription}'
            elif user_msg == "/qna":
                prompt = f'Generate 5 questions for transcription.\n \
                        Here is transcription: {transcription}'
        else:
            index_path = DATA_DIR / "indexes.faiss"
            if not index_path.exists():
                    print("No knowledge base found. Using general knowledge.\n")
                    prompt = user_msg
            else:
                prompt_context = "Use this context to answer question:\n\nContext:\n"
                matches_context = store.search(user_msg, DATA_DIR)
                for i, match in enumerate(matches_context):
                    clean_match = match['text'].replace("passage: ", "")
                    structed_text = f"[{i+1}] {clean_match}"
                    prompt_context += f"\n{structed_text}"
            
                prompt = prompt_context + f"\n\nQuestion: {user_msg}" + "\n\nAnswer: "
        
        chat.add_message(prompt)
        tokens = chat.stream_response(is_stream=True)
        if tokens:
            print(f"[Tokens used: {tokens.total_tokens} | Total so far: {chat.total_tokens}]")
        print('\n')
            
    chat.save_log(BASE_DIR, "md")
    print("See you!")

if __name__ == "__main__":
    main()
