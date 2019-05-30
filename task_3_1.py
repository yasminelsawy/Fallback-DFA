import re
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument(
        '--dfa-file',
        action="store",
        help="path of file to take as input to construct DFA",
        nargs="?",
        metavar="dfa_file")
    parser.add_argument(
        '--input-file',
        action="store",
        help="path of file to take as input to test strings in on DFA",
        nargs="?",
        metavar="input_file")

    args = parser.parse_args()

    inputDFAFile = args.dfa_file
    fileTestCases = args.input_file

    file_out = open("task_3_1_result.txt", "a")

    States = "A , B, C, D, DEAD"
    alphas = "x , y"
    startSate = " A "
    acceptSates = "B, D"
    Transdfa = "(A, x, B), (A, y, C), (B, x, DEAD), (B, y, D), (C, x, DEAD), (C, y, DEAD), (D, x, DEAD), (D, y, D), (DEAD, x, DEAD), (DEAD, y, DEAD)"
    StatesLabel = "(A, DEFAULT), (B, x|y), (C, x|y), (D, xy*), (DEAD, DEFAULT)"
    actions = "(x|y, Hello world), (xy*,Bye World), (DEFAULT, Fail!)"
    with open(inputDFAFile, 'r') as f:
        lines = f.readlines()

        States = lines[0].strip()
        States = States.split(",")
        alphas = lines[1].strip()
        alphas = alphas.split(",")

        startSate = lines[2].strip()
        startSate = startSate.replace(' ', '')

        acceptSates = lines[3].strip()
        acceptSates = acceptSates.replace(' ', '')
        acceptSates = acceptSates.split(",")

        Transdfa = lines[4].strip()
        Transdfa = re.findall(r'((?<=\().*?(?=\)))', Transdfa)

        StatesLabel = lines[5].strip()
        StatesLabel = re.findall(r'((?<=\().*?(?=\"\)))', StatesLabel)

        actions = lines[6].strip()
        actions = re.findall(r'((?<=\().*?(?=\"\)))', actions)

        DFATrans = {}
        Labeldict = {}

        def initDicts():
            global DFATrans
            global Labeldict

            for state in States:
                state = state.replace(' ', '')
                DFATrans[state] = {}

            for trans in Transdfa:
                trans = trans.replace(' ', '')
                transArray = trans.split(",")
                DFATrans[transArray[0]][transArray[1]] = transArray[2]

            for labels in StatesLabel:
                labelArray = labels.split(",")
                labelArray[0].replace(' ', '')
                DFATrans[labelArray[0]]["Label"] = labelArray[1][2:]

            for label in actions:
                LabelArrayD = label.split(",")
                LabelArrayD[0].replace(' ', '')
                Labeldict[LabelArrayD[0][1:-1]] = LabelArrayD[1][1:]
            print(Labeldict)
            print(DFATrans)

        def fallBack(stringTape):
            leftHand = 0
            rightHAnd = 0
            stackArray = []
            stackArray.append(startSate)
            while leftHand < len(stringTape):
                currentState = stackArray[-1]
                nextState = DFATrans[currentState][stringTape[leftHand]]
                leftHand += 1
                stackArray.append(nextState)
            counter = 1

            cont = False
            for aa in acceptSates:
                if aa in stackArray:
                    cont = True

            if not cont:
                ss = "" + stringTape[rightHAnd:leftHand] + ", " + Labeldict[
                    DFATrans[stackArray[-1]]['Label']] + " \""
                file_out.write(ss)
                file_out.write("\n")
                return

            lastSate = stackArray.pop()

            while lastSate not in acceptSates:

                if lastSate == startSate:
                    ss = "" + stringTape[rightHAnd:leftHand] + ", " + Labeldict[
                        DFATrans[lastSate]['Label']] + " \""
                    file_out.write(ss)
                    file_out.write("\n")
                    return
                counter += 1
                lastSate = stackArray.pop()
            leftHand = (leftHand - counter)
            labell = Labeldict[DFATrans[lastSate]['Label']]

            vv = "" + stringTape[rightHAnd:leftHand +
                                 1] + ", " + "" + labell + " \""
            file_out.write(vv)
            file_out.write("\n")
            leftHand += 1
            if leftHand < len(stringTape):
                fallBack(stringTape[leftHand:])

        initDicts()

    with open(fileTestCases, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            fallBack(line.strip())
