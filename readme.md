# WikiAssistant
This project uses wikipedia pages in order to generate a 
retrievable database of information. The information is
stored as vectors in *pinecone* and can be retrieved 
using the *query* method from *pinecone* API.

From there we use OpenAI API to generate text based on 
factual information from wikipedia.

## Installation
1. Clone the repository
2. Set up a virtual environment
    - `python -m venv venv`
    - `source venv/bin/activate` for activating
    - `source venv/bin/deactivate` for deactivating
2. Install the requirements.txt file with `pip install -r requirements.txt`
3. Create a .env file with the following variables:
    - PINECONE_API_KEY
    - OPENAI_API_KEY

## Usage
