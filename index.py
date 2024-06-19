from flask import Flask, render_template, request, jsonify, redirect
from clips import Environment
import os
import json


class DiseaseDiagnosis:
    def __init__(self):
        self.dataPath = os.path.abspath(os.path.join(os.getcwd(), 'data'))
        self.diseasePath = os.path.join(self.dataPath, 'disease-symptoms.clp')
        self.env = Environment()
        self.load_environment()

    def load_environment(self):
        self.env.clear()                # Clear the environment before reloading
        self.env.load(self.diseasePath)
        print("CLIPS environment loaded with rules from disease-symptoms.clp")

    def reset(self):
        self.env.reset()
        print("CLIPS environment reset.")

    def addSymptom(self, symptom):
        text = f'(assert (has_symptom {symptom}))'
        self.env.eval(text)

    def run(self):
        _ = self.env.run()

    def getDiseases(self):
        diseases = []

        for fact in self.env.facts():
            fact = str(fact)
            if "disease_is" in fact:
                disease = fact[1:-1].split(" ")[1]
                disease = disease.replace("_", " ")
                disease = disease.title()
                diseases.append(disease)
        return diseases


    def getSymptoms(self):
        symptoms = []

        for fact in self.env.facts():
            fact = str(fact)
            if "has_symptom" in fact:
                symptom = fact[1:-1].split(" ")[1]
                symptom = symptom.replace("_", " ")
                symptom = symptom.title()
                symptoms.append(symptom)
        return symptoms

    def getSymptomList(self):
        path = os.path.join(self.dataPath, 'symptoms.txt')
        f = open(path, "r")
        symptoms = []
        for x in f:
            x = x.replace(',', '')
            x = x.replace('\r', '')
            x = x.replace('\n', '')
            x = x.replace('_', ' ')
            x = x.title()
            symptoms.append(x)
        return symptoms
    
    def add_new_symptom(self, rule_name, symptom):
        # Adding to symptoms.txt
        path = os.path.join(self.dataPath, 'symptoms.txt')
        diseasePath = os.path.join(self.dataPath, 'disease-symptoms.clp')
        
        # reading all the symptoms form the txt
        with open(path, "r") as f:
            lines = f.readlines()

        lines[-1] = lines[-1].strip()+",\n"
        lines.append(f"{symptom},\n")
        
        lines.sort()
        print(lines[-1])
        lines[-1] = lines[-1][:-2]
        
        with open(path, "w") as f:
            f.writelines(lines)

        # Adding to CLIP file
        with open(diseasePath, "r") as f:
            lines = f.readlines()
            
        found_disease = False
        new_lines = []
        for line in lines:
            if rule_name.lower() in line.lower():
                found_disease = True
                print(line)
            new_line = line
            if "=>" in line and found_disease:
                new_line = line.replace("=>", f"(has_symptom {symptom})\n\t=>")
                found_disease = False
            new_lines.append(new_line)
        
        # print(new_lines)
        with open(diseasePath, "w") as f:
            f.writelines(new_lines)
        self.load_environment()  # Reload the environment with the updated knowledge base


class DiseaseInfo:
    def __init__(self):
        self.decsriptions = self.getDescriptions()
        self.precautions = self.getPrecautions()

    def detail(self, diseases):
        data = []
        for disease in diseases:
            x = disease.lower().strip().replace(" ", "_")
            oneData = {
                'name': disease,
                'description': self.decsriptions[x],
                'precautions': self.precautions[x]
            }
            data.append(oneData)
        
        print(data)
        return data

    def getDescriptions(self):
        data = {}
        f = open("./data/disease-description.csv", "r")
        counter = 0
        for x in f:
            counter += 1
            if counter <= 1:
                continue
            x = x.strip().split(',')
            x[0] = x[0].lower().strip().replace(" ", "_")
            x[1] = ",".join(x[1:]).replace("\"", "")
            data[x[0]] = x[1]
        return data

    def getPrecautions(self):
        data = {}
        f = open("./data/disease-precaution.csv", "r")
        counter = 0
        for x in f:
            counter += 1
            if counter <= 1:
                continue
            x = x.strip().split(',')
            x[0] = x[0].lower().strip().replace(" ", "_")
            precautions = []
            for i in range(1, len(x)):
                precaution = x[i].strip().capitalize()
                if precaution != "":
                    precautions.append(precaution)

            data[x[0]] = precautions
        return data


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

engine = DiseaseDiagnosis()
engine.load_environment()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', symptomList=engine.getSymptomList())

@app.route('/addNewSymptom', methods=['POST'])
def addNewSym():
    try:
        new_symptom= request.form['new_symptom']
        disease_name= request.form['diseaseName']
        new_symptom = new_symptom.replace(' ', '_').lower()
        disease_name= "is_it_" + disease_name.replace(' ', '_')
        
        print(new_symptom, disease_name)
        engine.add_new_symptom(disease_name, new_symptom)
        return redirect('/')
    except:
        return jsonify({
            'status': 'error'
        })

@app.route('/addNewDisease', methods=['POST'])
def addNewDisease():
    try:
        disease_name = request.json['diseaseName'].strip().replace(' ', '_')
        disease_description = request.json['diseaseDescription'].strip()
        disease_precautions = request.json['diseasePrecautions'].split(',')
        new_symptoms = request.json['newSymptoms'].split(',')

        # Check if disease name already exists
        disease_exists = False
        with open(os.path.join(engine.dataPath, 'disease-symptoms.clp'), "r") as f:
            for line in f:
                if f"(defrule {disease_name}" in line:
                    disease_exists = True
                    break
        
        if disease_exists:
            return jsonify({
                'status': 'error',
                'message': f"Disease '{disease_name.replace('_', ' ')}' already exists."
            })

        # Update symptoms.txt
        with open(os.path.join(engine.dataPath, 'symptoms.txt'), "a") as f:
            for symptom in new_symptoms:
                existing_symptoms = engine.getSymptoms()  # Retrieve existing symptoms
                if symptom not in existing_symptoms:
                    f.write(f"{symptom.strip().replace(' ', '_').lower()},\n")

        # Update disease-description.csv
        with open(os.path.join(engine.dataPath, 'disease-description.csv'), "a") as f:
            f.write(f"{disease_name.replace('_', ' ')},{disease_description}\n")

        # Update disease-precaution.csv
        with open(os.path.join(engine.dataPath, 'disease-precaution.csv'), "a") as f:
            f.write(f"{disease_name.replace('_', ' ')},{','.join(disease_precautions)}\n")

        # Update disease-symptoms.clp
        with open(os.path.join(engine.dataPath, 'disease-symptoms.clp'), "a") as f:
            f.write(f"\n(defrule {disease_name}\n")
            f.write(f"  (disease_is {disease_name})\n")
            f.write(f"  =>\n")
            f.write(f"  (printout t \"{disease_name.replace('_', ' ')}\" crlf)\n")
            f.write(f")\n")

            f.write(f"\n(defrule is_it_{disease_name}\n")
            # f.write(f"  (and")
            for symptom in new_symptoms:
                f.write(f"  (has_symptom {symptom.strip().replace(' ', '_').lower()})\n")
            # f.write(f")\n")
            f.write(f"  =>\n")
            f.write(f"  (assert (disease_is {disease_name}))\n")
            f.write(f")\n")

        # Reload the CLIPS environment
        engine.load_environment()  # Ensure the environment is reloaded

        return jsonify({
            'status': 'success'
        })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error'
        })
    

@app.route('/diagnose', methods=['POST'])
def diagnose():
    engine.reset()
    engine.load_environment()

    try:

        data = request.get_json()  # Use get_json() to parse JSON data
        symptoms = data['symptoms']

        for symptom in symptoms:
            symptom = symptom.replace(' ', '_').lower()
            engine.addSymptom(symptom)

        engine.run()
        diseases = engine.getDiseases()
        info = DiseaseInfo()

        if not diseases:
            return jsonify({
                'status': 'success',
                'diseases': [],
                'message': 'No diseases detected, please add more symptoms.'
            })


        return jsonify({
            'status': 'success',
            'diseases': info.detail(diseases)
            
        })
    except Exception as e:
        print(f"Error during diagnosis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Error during diagnosis: {str(e)}"
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
