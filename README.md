# Ollama-SQLite-RAG

## Table of Contents

- [Idea behind the project](#idea)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Libraries used](#libraries)
- [Technical challenges](#challenges)
- [Project structure](#structure)
- [Lessons learned](#learned)
- [Author](#author)
---
## Idea behind the project<a name = "idea"></a>

Project is based on ```Streamlit```.

---
## Getting started <a name = "getting_started"></a>

1. Open project folder in your IDE
2. Before first use, use ```downloads.ipynb``` to download image dataset and image recognition model
3. Run ```main.py```
4. In terminal launch command: streamlit run main.py. Script will provide you with command upon launching
5. Launched streamlit will provide local IP address to open in your browser while also opening it automatically.

If Streamlit does not launch properly, make sure terminal is operating within the ReadML folder.

---
## Usage <a name = "usage"></a>

Upon launching Streamlit app using ```main.py```, file upload widget can be seen. \


---

## Libraries used <a name = "libraries"></a>
- ```Streamlit``` - Provides GUI and ability to use the app in mobile phone - that will come in handy


---
## Technical challenges<a name = "challenges"></a>
Test, ```test``` test.

---
## Project structure<a name = "structure"></a>
```
├───data
│   ├───main-dataset         -dataset of 60 pictures for end-user
│   ├───recognition-model    -contains a script to generate recognition model and the model itself
│   └───result               -scanned files are stored in json file inside this folder
├───drafts                   -experiments, pre-processing tests and visualization methods
├───modules                  -stores all functions used in project
```
---
## Lessons learned<a name = "learned"></a>
Lorem ipsum

---
## Author<a name = "author" />
Mateusz Ratajczak, 2024
