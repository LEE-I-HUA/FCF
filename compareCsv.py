import pandas as pd
import time as tm
def userChoice():
    print('you have to use \'\'to wrap your inputs') 
    choice = eval(input("Please select the column you want to compare:\n \
    a: vessel's name\n \
    b: IMO\n \
    c: callSign\n \
    d: RFMOs\n \
    Choose:"))
    return choice

def getfile():
    # enter csv user want to compare
    file = eval(input("please entre the file's path:\n \
        ex: 'C:/Users/User/Desktop/Python/iotc/20230612.csv'\nyour path:"))
    file = pd.read_csv(file)
    return file

def pairColumn(choice,data):
    if choice=='a':
        data = data['vessel']
    elif choice=='b':
        data = data['IMO']
    elif choice=='c':
        data = data['callSign']
    else:
        data = data['IOTC']
    return data

# compare current with the leastest one
def compareList(current, least):
    # add: difference in current not in least
    add = list(set(current) - set(least))
    # subtract: difference in least not in current
    subtract = list(set(least) - set(current))
    a = "New vessel(s): {}".format(add) if add else "There is nothing added ~"
    s = "Delisted vessel(s): {}".format(subtract) if subtract else "There is nothing subtracted  ~"
    return a+'\n'+ s

def main():
    choice_list =['a', 'b', 'c', 'd']
    choice = userChoice()
    if choice not in choice_list: 
        print('your input is not available please try again\n')
        main()
    print('\nfirst file:')
    first = getfile()
    print('\nsecond file:')
    second = getfile()
    print('===================================')
    try:
        print(compareList(pairColumn(choice,first), pairColumn(choice,second)))
        tm.sleep(1)
        return 0
        
    except KeyError:
        print('this column doesn\'t exist in the csv you select\n \
            Please try again~\n')
        main()
        
        
main()
input()
    
