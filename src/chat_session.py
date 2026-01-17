from groq import Groq
from pathlib import Path
import json
from datetime import datetime
from termcolor import colored

class ChatSession:
    def __init__(self, api_key: str, model: str):
        self.messages = []
        self.client = Groq(api_key=api_key)
        self.model = model
        self.start_time = datetime.now()
        self.total_tokens = 0
        
    def add_message(self, message: str, role: str = 'user', ):
        message_structured = {'role': role, 'content': message}
        self.messages.append(message_structured)

    def system_prompt(self, user_prompt: str):
        self.add_message(user_prompt, "system")
    
    def stream_response(self, is_stream: bool = True) -> dict | None:
        print(colored("[Assistant is typing...]", "yellow"), end="", flush=True)

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=is_stream
            )
        except Exception as e:
            if any(x in str(e).lower() for x in ["401", "invalid", "unauthorized"]):
                print("Invalid API key!")
            elif "429" in str(e):
                print("Rate limit! Wait and retry.")
            else:
                print(f"Error: {e}")
            return None

        usage = None
        print("\r", end="")
        if is_stream:
            content = "" 
            for chunk in stream:
                part = chunk.choices[0].delta.content
                if part:
                    content += part
                    print(part, end="", flush=True)

                if chunk.usage:
                    usage = chunk.usage
        else:
            content = stream.choices[0].message.content
            print(content)
            usage = stream.usage

        print()

        self.add_message(content, "assistant")

        if usage:
            self.total_tokens += usage.total_tokens
        else:
            print("[Warning: token count unavailable]")

        return usage
    
    def transcript_with_whisper(self, path_to_file):
        with open(path_to_file, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                response_format="text"
            )

        print(transcription)
        return transcription

    def save_log(self, base_dir: str, log_type: str = "json"):
        log_dir = base_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        timestamp = self.start_time.strftime("%Y-%m-%d_%H-%M-%S")

        if log_type == "json":
            file_path = log_dir / f"chat_{timestamp}.json"
            logs = {
                "conversation" : self.messages,
                "tokens": self.total_tokens,
                "start_chat": self.start_time.isoformat(),
                "end_chat": datetime.now().isoformat(),
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)
        else:
            file_path = log_dir / f"chat_{timestamp}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"- Start chat : {self.start_time}\n")
                f.write(f"- End chat : {datetime.now()}\n")
                f.write(f"- Total tokens : {self.total_tokens}\n")
                for message in self.messages:
                    f.write(f"### {message['role']}\n")  
                    content = message.get('content')
                    if isinstance(content, dict):
                        f.write(f"\t{json.dumps(content, indent=2, ensure_ascii=False)}\n\n")
                    else:
                        f.write(f"\t{content}\n\n")
