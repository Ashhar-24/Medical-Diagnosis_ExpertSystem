# Medical-Diagnosis_ExpertSystem

<!-- Intro -->
## Introduction

Welcome to the Disease Diagnosis Expert System project! This project is an intelligent, web-based application designed to assist users in diagnosing potential diseases based on their reported symptoms. Utilizing the power of CLIPS (C Language Integrated Production System), a robust expert system shell, this application leverages a rule-based approach to identify and suggest possible health conditions.

The primary goal of this project is to provide a user-friendly interface where users can input their symptoms and receive a list of potential diseases along with their descriptions and precautionary measures. Additionally, the system allows users to contribute by adding new diseases and their associated symptoms, enriching the knowledge base for future diagnoses.

## Features

- Interactive Web Interface: A clean and responsive web interface built with HTML, CSS, and JavaScript for easy symptom input and result display.

- Rule-Based Inference Engine: Utilizes CLIPS to implement an expert system that processes user inputs and infers possible diseases.

- Symptom Management: Allows users to add, reset, and manage their symptoms dynamically.
    
- Disease Contribution: Users can add new diseases along with their descriptions, precautions, and symptoms, expanding the system's diagnostic capabilities.
    
- Real-Time Diagnosis: Provides instant feedback and probable disease diagnoses based on the symptoms provided by the user.

## Getting Started

To run this project locally, follow these steps:

1. Clone the Repository:
```
git clone https://github.com/Ashhar-24/Medical-Diagnosis_ExpertSystem.git
cd Medical-Diagnosis_ExpertSystem
```

2. Set Up the Environment (ubuntu):
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Run the Flask Server:
```
python index.py
```

4. Open the Web Application:

Open your web browser and navigate to http://127.0.0.1:5000/ to start using the expert system.

## How It Works

1. User Input: 
The user selects symptoms from a predefined list and submits them through the web interface.

2. Inference Engine: 
The submitted symptoms are processed by the CLIPS-based inference engine, which applies predefined rules to infer potential diseases.

3. Diagnosis Result: 
The system returns a list of probable diseases, their descriptions, and recommended precautions, which are displayed to the user.

4. New Disease Addition: 
Users can contribute to the system by adding new diseases, enhancing the system's diagnostic knowledge base.

## Contributions

I welcome contributions from the community! Whether you want to add new features, improve existing functionality, or simply fix bugs, your help is appreciated. Feel free to fork the repository, make your changes, and submit a pull request.