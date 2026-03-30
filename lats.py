from google.generativeai import list_models

for m in list_models():
    print(m.name)