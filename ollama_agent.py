import ollama
import os
from datetime import datetime


class FileTools:
    @staticmethod
    def read_file(path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
    
    @staticmethod
    def list_files(directory: str = ".") -> str:
        files = os.listdir(directory)
        return "\n".join(files)
    
    @staticmethod
    def get_time() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class OllamaAgent:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.tools = FileTools()
    
    def _is_file_command(self, prompt: str) -> bool:
        return any(cmd in prompt.lower() for cmd in ["read file", "read_file"])
    
    def _is_list_command(self, prompt: str) -> bool:
        return any(cmd in prompt.lower() for cmd in ["list files", "list_files"])
    
    def _is_time_command(self, prompt: str) -> bool:
        return "time" in prompt.lower()
    
    def _extract_filepath(self, prompt: str) -> str:
        words = prompt.split()
        return words[-1] if len(words) > 1 else "."
    
    def _call_ollama(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    
    def execute(self, prompt: str) -> str:
        if self._is_file_command(prompt):
            path = self._extract_filepath(prompt)
            return self.tools.read_file(path)
        
        if self._is_list_command(prompt):
            return self.tools.list_files(".")
        
        if self._is_time_command(prompt):
            return self.tools.get_time()
        
        return self._call_ollama(prompt)


def run_demo():
    agent = OllamaAgent()
    
    tasks = [
        "What time is it?",
        "List files in current directory",
        "Read file requirements.txt",
        "What is Python?"
    ]
    
    for task in tasks:
        print(f"Task: {task}")
        try:
            result = agent.execute(task)
            print(f"Response: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    run_demo()
