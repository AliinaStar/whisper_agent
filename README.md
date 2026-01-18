## Whisper Agent
A CLI-based pipeline that takes an audio file, transcribes it and generates a summary or key points using a language model Groq.


### Setup
```
pip install -r requirements.txt
```

Create `.env` file based on `.env.sample`:
```bash
cp .env.sample .env
```

### Usage
To start the chat: 
```bash
python -m src.app  
```

#### Available Commands
- `<your question>` - Ask what you want to know about audio
- `/audio` - Transcribe audio file(s)
    - Supports multiple files separated by `;` (e.g., `file1.mp3;file2.wav`)
    - Supported formats: `.mp3`, `.mp4`, `.mpeg`, `.mpga`, `.m4a`, `.wav`, `.webm`
- `/summary` - Create summary from audio
- `/extract_keywords` - Extract keywords from audio
- `/generate_title` - Generate title to your audio
- `/qna` - Generate 5 questions to your audio
- `/exit` - Exit the application

### Example Output

```
What do you want to do?
/audio
Please, give path to your audio file: ..\src\audio.mp3

Transcription of audio:
 Python, a high-level interpreted programming language famous for its zen-like code...
Token indices sequence length is longer than the specified maximum sequence length for this model (566 > 512). Running this sequence through the model will result in indexing errors
Created 2 chunks
Batches: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.23it/s] 
Created embeddings
/summary
Summary:

Here's a concise and accurate summary of the transcription:

Python is a high-level interpreted programming language renowned for its simplicity, readability, and effectiveness. It was created by Guido Van Rossum in 1991 and is often used for server-side applications, big data analysis, and machine learning. Python's syntax is easy to learn, yet powerful, allowing for efficient declaration of variables, functions, and data structures. Its multi-paradigm nature combines functional, object-oriented, and procedural programming patterns. With a vast ecosystem of libraries and the pip package manager, Python is an ideal language for beginners and professionals alike.
[Tokens used: 726 | Total so far: 726]
```

### Example markdown log
**Full conversation log is in folder src/logs**
```
- Start chat : 2026-01-16 16:51:16.421040
- End chat : 2026-01-16 16:54:05.888175
- Total tokens : 4197
### system
	You are a helpful assistant that summarizes audio transcriptions concisely and accurately.

### user
	You have to summarize a transcription.                         
	Here is transcription:  Python, a high-level interpreted programming language famous for its zen-like code. It's arguably the most popular language in the world because it's easy to learn, yet practical for serious projects. In fact, you're watching this YouTube video in a Python web application right now. It was created by Guido Van Rossum and released in 1991, who named it after Monty Python's Flying Circus, which is why you'll sometimes find spam and eggs instead of foo and bar in code samples. It's commonly used to build server-side applications, like web apps with the Django framework, and is the language of choice for big data analysis and machine learning. Many students choose Python to start learning to code because of its emphasis on readability as outlined by the zen of Python. Beautiful is better than ugly, while explicit is better than implicit. Python is very simple, but avoids the temptation to sprinkle in magic that causes ambiguity. Its code is often organized into notebooks where individual cells can be executed, then documented in the same place. We're currently at version 3 of the language, and you can get started by creating a file that ends in .py, or .ipymb to create an interactive notebook. Create a variable by setting a name equal to a value It strongly typed which means values won change in unexpected ways but dynamic so type annotations are not required The syntax is highly efficient allowing you to declare multiple variables on a single line and define tuples lists and dictionaries with a literal syntax. Semicolons are not required, and if you use them, an experienced Pythonista will say that your code is not Pythonic. Instead of semicolons, Python uses indentation to terminate or determine the scope of a line of code. Define a function with the def keyword, then indent the next line, usually by four spaces, to define the function body. We might then add a for loop to it and indent that by another four spaces. This eliminates the need for curly braces and semicolons found in many other languages. Python is a multi-paradigm language. We can apply functional programming patterns with things like anonymous functions using lambda. It also uses objects as an abstraction for data, allowing you to implement object-oriented patterns with things like classes and inheritance. It also has a huge ecosystem of third-party libraries, such as deep learning frameworks like TensorFlow and wrappers for many high-performance low-level packages like Open Computer Vision, which are most often installed with the pip package manager. This has been the Python programming language in 100 seconds. Hit the like button if you want to see more short videos like this. Thanks for watching, and I will see you in the next one.



### assistant
	Here's a concise and accurate summary of the transcription:

Python is a high-level interpreted programming language renowned for its simplicity, readability, and effectiveness. It was created by Guido Van Rossum in 1991 and is often used for server-side applications, big data analysis, and machine learning. Python's syntax is easy to learn, yet powerful, allowing for efficient declaration of variables, functions, and data structures. Its multi-paradigm nature combines functional, object-oriented, and procedural programming patterns. With a vast ecosystem of libraries and the pip package manager, Python is an ideal language for beginners and professionals alike.
```
