from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from ydata_profiling import ProfileReport

app=Flask(__name__)
app.config['UPLOAD_FOLDER']="uploads/"
app.config['REPORT_FOLDER']="static/reports/"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'],exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
     
        df = pd.read_csv(file_path)
        profile = ProfileReport(df)
        report_path = os.path.join(app.config['REPORT_FOLDER'], 'eda_report.html')
        profile.to_file(output_file=report_path)
        
        return redirect(url_for('show_report'))
    
    return redirect(request.url)

@app.route('/report')
def show_report():
    return redirect(url_for('static', filename='reports/eda_report.html'))

if __name__=="__main__":
    app.run(debug=True)
