import matplotlib.pyplot as plt
import glob
import os
import datetime

def data_input(array):
    if array[-1] == "":
        return array[:-1]
    return array

def divide(array1, array2, ispercent=True):
    array = []
    for i in range(len(array1)):
        if ispercent:
            array.append((array1[i]/array2[i])*100)
        else:
            try:
                array.append(array1[i]/array2[i])
            except:
                pass
    return array

def save():
    name = input("Company Name: ")
    f = open(f"{name}.stock", "w")
    save = []
    data = ["Revenue", "Gross Profit", "Selling, General & Admin", 
    "Research & Development", "Operating Income", "Interest Expense", 
    "Net Income", "EPS (diluted)", "Dividend (if none, put 0)", 
    "Current Assets", "Total Assets", "Current Liabilities", "Long-Term Debt", 
    "Total Liabilities", "Shareholder's Equity", "Price", "Shares outstanding"]
    for i in range(len(data)):
        save.append(data_input(input(f"Input {data[i]}: ").split("\t")))
    for i in range(len(save)):
        for n in range(len(save[i])):
            string = ""
            temp = save[i][n].split(",")
            for j in range(len(temp)):
                string += temp[j]
            save[i][n] = string
    for i in range(len(save)):
        string = ""
        for n in range(len(save[i])):
            string += save[i][n] + ","
        f.write(string[:-1] + "\n")
    f.close()
    print("Data saved successfully.")

def plot():
    ratio = input("Input Ratio: ")
    while ratio == "help":
        print('''List of Ratios
'gpm' for gross profit margin.
'sga' for sga to gross profit.
'rd' for r&d to gross profit.
'interest' for interest expense to operating income.
'npm' for net profit margin.
'eps' for earnings per share.
'div' for dividend.
'cr' for current ratio.
'roa' for return on assets.
'ltd' for long-term debt to net income (how many years of income can pay off debt).
'dte' for debt to equity.
'roe' for return on equity.
'pe' for price to earnings.
'pb' for price to book value.''')
        ratio = input("Input Ratio: ")
    companies = []
    name = 0
    ans = ""
    files = []
    os.chdir(os.getcwd())
    for file in glob.glob("*.stock"):
        files.append(file)
    string = ""
    for i in range(len(files)):
        string += files[i] + ", "
    ans = input(f"Would you like to import the following files: {string[:-2]}? Answer 'yes' or 'no': ")
    if ans == "yes" or ans == "Yes":
        for i in range(len(files)):
            companies.append(files[i][:-6])
    else:
        while name != "" and name != "done":
            name = input("Input Company name/file (do not input '.stock'): ")
            print("Press enter or type 'done' when completed.")
            companies.append(name)
    data = []
    if companies[-1] == "" or companies[-1] == "done":
            companies = companies[:-1]
    for i in range(len(companies)):
        f = open(f"{companies[i]}.stock", "r")
        temp = f.read().splitlines()
        array = []
        for n in range(len(temp)):
            array.append(temp[n].split(","))
        for n in range(len(array)):
            for k in range(len(array[n])):
                array[n][k] = float(array[n][k])
        # Ratios
        if ratio == "gpm":
            data.append(divide(array[1], array[0], True))
        elif ratio == "sga":
            data.append(divide(array[2], array[0], True))
        elif ratio == "rd":
            data.append(divide(array[3], array[0], True))
        elif ratio == "interest":
            data.append(divide(array[5], array[4], True))
        elif ratio == "npm":
            data.append(divide(array[6], array[0], True))
        elif ratio == "eps":
            data.append(array[7])
        elif ratio == "div":
            data.append(array[8])
        elif ratio == "cr":
            data.append(divide(array[9], array[11], False))
        elif ratio == "roa":
            data.append(divide(array[6], array[10], True))
        elif ratio == "ltd":
            data.append(divide(array[12], array[6], False))
        elif ratio == "dte":
            data.append(divide(array[13], array[14], False))
        elif ratio == "roe":
            data.append(divide(array[6], array[14], True))
        elif ratio == "pe":
            data.append(divide(array[15], divide(array[6], array[16], False), False))
        elif ratio == "pb":
            data.append(divide(array[15], divide(array[14], array[16], False), False))
    year = int(input("Input last year of data (This program assumes you have 10 years worth of data, found from stockanalysis.com): "))
    print(f"Now displaying {ratio}.")
    plt.title(f"{ratio.upper()} from {year-9} to {year}")
    plt.xlim(year-9, year)
    plt.xlabel("Years")
    plt.ylabel(ratio.upper())
    plt.grid()
    years = []
    for i in range(10, 1, -1):
        years.append(year-i)
    years.append(year)
    for i in range(len(data)):
        while len(data[i]) < 10:
            data[i] = [0] + data[i]
        plt.plot(years, data[i], linestyle="-", label=companies[i])
    if len(data) > 1:
        average = []
        for n in range(len(data[0])):
            count = 0
            for i in range(len(data)):
                count += data[i][n]
            average.append(count / len(data))
        plt.plot(years, average, linestyle="--", label="Average")
    plt.legend(loc='best')
    plt.show()
    ans = input("Save graph? Type 'yes': ")
    if ans == "yes":
        plt.savefig(f"{ratio}.png", transparent = True, orientation ='landscape')

def screen():
    ratios = ["gpm", "sga", "rd", "interest", "npm", "eps", "div", "cr", "roa", "ltd", 
    "dte", "roe", "pe", "pb"]
    companies = []
    name = 0
    ans = ""
    files = []
    os.chdir(os.getcwd())
    for file in glob.glob("*.stock"):
        files.append(file)
    string = ""
    for i in range(len(files)):
        string += files[i] + ", "
    ans = input(f"Would you like to import the following files: {string[:-2]}? Answer 'yes' or 'no': ")
    if ans == "yes" or ans == "Yes":
        for i in range(len(files)):
            companies.append(files[i][:-6])
    else:
        while name != "" and name != "done":
            name = input("Input Company name/file (do not input '.stock'): ")
            print("Press enter or type 'done' when completed.")
            companies.append(name)
    year = int(input("Input last year of data (This program assumes you have 10 years worth of data, found from stockanalysis.com): "))
    for m in range(len(ratios)):
        ratio = ratios[m]
        data = []
        if companies[-1] == "" or companies[-1] == "done":
            companies = companies[:-1]
        for i in range(len(companies)):
            f = open(f"{companies[i]}.stock", "r")
            temp = f.read().splitlines()
            array = []
            for n in range(len(temp)):
                array.append(temp[n].split(","))
            for n in range(len(array)):
                for k in range(len(array[n])):
                    array[n][k] = float(array[n][k])
            # Ratios
            if ratio == "gpm":
                data.append(divide(array[1], array[0], True))
            elif ratio == "sga":
                data.append(divide(array[2], array[0], True))
            elif ratio == "rd":
                data.append(divide(array[3], array[0], True))
            elif ratio == "interest":
                data.append(divide(array[5], array[4], True))
            elif ratio == "npm":
                data.append(divide(array[6], array[0], True))
            elif ratio == "eps":
                data.append(array[7])
            elif ratio == "div":
                data.append(array[8])
            elif ratio == "cr":
                data.append(divide(array[9], array[11], False))
            elif ratio == "roa":
                data.append(divide(array[6], array[10], True))
            elif ratio == "ltd":
                data.append(divide(array[12], array[6], False))
            elif ratio == "dte":
                data.append(divide(array[13], array[14], False))
            elif ratio == "roe":
                data.append(divide(array[6], array[14], True))
            elif ratio == "pe":
                data.append(divide(array[15], divide(array[6], array[16], False), False))
            elif ratio == "pb":
                data.append(divide(array[15], divide(array[14], array[16], False), False))
        print(f"Now displaying {ratio}.")
        plt.title(f"{ratio.upper()} from {year-9} to {year}")
        plt.xlim(year-9, year)
        plt.xlabel("Years")
        plt.ylabel(ratio.upper())
        plt.grid()
        years = []
        for i in range(10, 1, -1):
            years.append(year-i)
        years.append(year)
        for i in range(len(data)):
            while len(data[i]) < 10:
                data[i] = [0] + data[i]
            plt.plot(years, data[i], linestyle="-", label=companies[i])
        if len(data) > 1:
            average = []
            for n in range(len(data[0])):
                count = 0
                for i in range(len(data)):
                    count += data[i][n]
                average.append(count / len(data))
            plt.plot(years, average, linestyle="--", label="Average")
        plt.legend(loc='best')
        print(f"Saving graph as {ratio}.png.")
        plt.savefig(f"{ratio}.png", transparent = True, orientation ='landscape')
        plt.show()

run = True

while run:
    instruction = input("Instruction: ")
    if instruction == "exit":
        run = False
    elif instruction == "help":
        print('''List of Commands
'exit' to quit the program.
'save' to load in the data of a company.
'plot' to plot a graph of a particular ratio of analysis against other companies.
'help' to print list of commands.''')
    elif instruction == "save":
        save()
    elif instruction == "plot":
        plot()
    elif instruction == "screen":
        screen()
    else:
        print("Instruction not found. To quit, type 'exit'. For help, type 'help'.")