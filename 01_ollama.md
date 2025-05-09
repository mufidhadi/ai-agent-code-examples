# Ollama
## Install Ollama
link: https://ollama.com/download/windows
## download LLM model
- llama3.2:3b
```
ollama pull llama3.2:3b
ollama ls
```
- all-minilm
```
ollama pull all-minilm
ollama ls
```
## test run on CLI
```
ollama run llama3.2:3b
```

# UV
## install UV
- windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
- linux / mac
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```