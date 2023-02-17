import os
from jinja2 import Environment, FileSystemLoader
from solver import Sudoku,input_validator

def input_grid(data):
    initial=[[' ' for i in range(9)] for j in range(9)]
    grid = [[0 for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            ind_name=str(row)+"_"+str(col)
            if(data[ind_name] != None and data[ind_name].isnumeric()):
                x=data[ind_name]
                grid[row][col]=int(x)
                initial[row][col]=x
    # grid = [[2, 2, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 1]]
    return initial,grid

def get_sudoku_data_from_request(body):
    initial=[[' ' for i in range(9)] for j in range(9)]
    elements = body.split("&")
    elements = elements [:-1]
    for ele in elements:
        temp = ele.split("=")
        ind_name = temp[0] if temp[0] != None else None
        val = temp[1] # if ( temp[1] != None and temp[1] != '' )  else ' '
        initial[int(ind_name.split("_")[0])][int(ind_name.split("_")[1])] = val
    return initial

def get_sudoku_grid(initial_data):
    grid = [[0 for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            if(initial_data[row][col] == '' or initial_data[row][col] == ' ' or initial_data[row][col] == None):
                grid[row][col] = 0
            elif(initial_data[row][col].isnumeric() == False or int(initial_data[row][col]) == 0):
                grid[row][col] = -1
            else:
                grid[row][col] = int(initial_data[row][col])
    return grid


def empty_sudoku_page():
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("empty_sudoku.html")
    html = template.render()
    return {
        'statusCode': 200,
        'body': html ,
        "headers": {
            'Content-Type': 'text/html;'
        }
    }

def invalid_sudoku_page(mes):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("invalid.html")
    html = template.render(message = mes)
    return {
        'statusCode': 200,
        'body': html ,
        "headers": {
            'Content-Type': 'text/html;'
        }
    }

def solved_sudoku_page(initial_data, sudoku_grid):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))
    template = env.get_template("solved_sudoku.html")
    html = template.render(initial=initial_data, result=sudoku_grid)
    return {
        'statusCode': 200,
        'body': html ,
        "headers": {
            'Content-Type': 'text/html;'
        }
    }

def lambda_handler(event, context):
    
    print("In Sudoku Lambda Solver")

    method = event['httpMethod']

    if(method.upper() == "GET"):
        print("Returning the empty Sudoko page")
        return empty_sudoku_page()
    elif(method.upper() == "POST"):
        try:
            initial_data = get_sudoku_data_from_request(event["body"])
            sudoku_grid = get_sudoku_grid(initial_data)
            valid = input_validator(sudoku_grid)
            if(valid == True):
                print("Solving the Sudoku")
                Sudoku(sudoku_grid,0 ,0)
                return solved_sudoku_page(initial_data, sudoku_grid)
            else:
                print("Invalid Input")
                return invalid_sudoku_page("Invalid Input")
        except Exception as e:
            print("Invalid Request")
            print(e)
            return invalid_sudoku_page("Invalid Request")
