# RAGChat

## Requirements
- Node version v23.3.0 (nvm is a helpful tool available to switch Node version (`nvm install 23.3.0`, `nvm use 23.3.0`.))
- Ollama Deepseek-r1:7b running with API at port 11434.
- `pyenv` may be required, particularly if you are using MacOS.

## Running 
1. Ensure the AI model is running locally (Ollama).
2. `cd backend`
3. Source the venv: `source venv/bin/activate`, or equivalent on your operating system (see `venv/bin` folder for options.)
4. `python ./server.py`
5. `cd ../frontend`
6. `npm install`
7. `npm start`

## Testing
### Backend
1. Execute `pytest` in the `backend` directory. 
### Frontend
<!-- 0. Go to `frontend/src/renderer/App.tsx` and comment lines `5`, `6`, and `104` ('ldrs' loading animation library), as this is incompatible with Jest for testing. -->
1. `cd frontend`
2. `npm run build:main`
2. `npm run build:renderer`
3. `npm test`

## Correcting Gensim errors in the Installation
Corrections in the venv library folder.
### `gensim/matutils.py`
Replace 'triu' imports with `from numpy import triu`.
### `gensim/corpora/dictionary.py`
Replace `collections` in the Mapping import with `collections.abc`.
### `gensim/models/ldamodel.py`
Replace `from scipy.misc import logsumexp` with `from scipy.special import logsumexp`.