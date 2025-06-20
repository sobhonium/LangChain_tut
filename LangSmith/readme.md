First off set the following vars in a ```.env``` file.

```python
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY= "<fille this>"
LANGSMITH_PROJECT="pr-ajar-making-75"

GROQ_API_KEY = "<fille this>"
```

then, run

```python
python3 test.py
```

For the final step, go to ```smith.langchain.com``` and login to see the conversations put by llm and follow the messages.

