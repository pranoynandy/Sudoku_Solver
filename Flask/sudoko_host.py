from flask import Flask, render_template, request
from solver import sudoku , output, input_grid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("empty_sudoko.html")

@app.route('/solved' , methods=['POST'])
def solved():
        
    data=request.form
    grid = input_grid(data)

    if (sudoku(grid)):
        output(grid)
    
    #print(data)
    return render_template("solved_sudoko.html", result=grid)

app.run(host='0.0.0.0', port=5001)
