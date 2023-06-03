import os
import fitz
import spacy, spacy_transformers
from flask import Flask, render_template, request

app = Flask(__name__)
nlp = spacy.load("model-best")


def pdf_to_text(file_nm):
  text = " "
  doc = fitz.open(file_nm)

  for page in doc:
    text += str(page.get_text())

  return text 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    try:
      if 'resume' in request.files:
          resume_file = request.files['resume']  
          resume_file.save(os.path.join("files", "user.pdf")) 
          doc = nlp(pdf_to_text("files/user.pdf"))
          
          data = [(ent.label_, ent.text) for ent in doc.ents]
          data = sorted([(label.replace("_", " ").title(), ent) for label, ent in data], key=lambda x:len(x[0]))
          

          if len(data) == 0:
             return render_template("index.html", data=[("Not Found", "Missing desired informations!")], show_summary=True)
          
          return render_template('index.html', data=data, show_summary=True)
    
    except:
      return render_template('index.html', data=[("ERROR", "A courrputed file was uploaded!")], show_summary=True)

if __name__ == '__main__':
    app.run()
