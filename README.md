# RAGChat

## Requirements
- Node version v23.3.0 (nvm is a helpful tool available to switch Node version.)
- Ollama Deepseek-r1:7b running with API at port 11434.

## Running 
1. Ensure the AI model is running locally (Ollama).
2. `cd backend`
3. Make sure the requirements are installed. A virtual environment for your Python is recommended.
4. `python ./server.py`
5. `cd ../frontend`
6. `npm start`

## Testing
### Backend
Execute `pytest` in the `backend` directory.