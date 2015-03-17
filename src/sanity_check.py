import sys

def main():
    homophones = {'its', "it's", 'your', "you're", 'their', "they're", 'lose', 'loose', 'to', 'too',
                  'Its', "It's", 'Your', "You're", 'Their', "They're", 'Lose', 'Loose', 'To', 'Too'}

    flip = {'its':"it's", "it's":'its', 'your':"you're", "you're":'your', 'their':"they're", 
            'Its':"It's", "It's":'Its', 'Your':"You're", "You're":'Your', 'Their':"They're", 
            "they're":'their', 'lose':'loose', 'loose':'lose', 'to':'too', 'too':'to',
            "They're":'Their', 'Lose':'Loose', 'Loose':'Lose', 'To':'Too', 'Too':'To'}

    errfile = open(sys.argv[1])
    outfile = open(sys.argv[2])

    line_num = 0

    difflines = 0
    difftokens = 0
    candidlines = 0
    candidtokens = 0

    for eline in errfile:
        line_num += 1
        oline = outfile.readline()

        etok = eline.split()
        otok = oline.split()

        num_otok = len(otok)

        if num_otok != len(etok):
            print('line ' + str(line_num) + 'has different number of tokens.')
            continue
            
        if num_otok == 0:
            continue
            
        ecand = [word for word in etok if word in homophones]
        ocand = [word for word in otok if word in homophones]

        num_ocand = len(ocand)

        if num_ocand != len(ecand):
            print('line ' + str(line_num) + 'has different number of homophones.')
            continue
            
        if num_ocand == 0:
            continue
        
        candidlines += 1
        candidtokens += num_ocand

        changes = [1 for i, word in enumerate(ocand) if word != ecand[i]]
        
        if changes:
            difflines += 1
            difftokens += len(changes)

    errfile.close()
    outfile.close()

    print('candidate lines: ' + str(candidlines))
    print('different lines: ' + str(difflines))
    print('candidate tokens: ' + str(candidtokens))
    print('different tokens: ' + str(difftokens))

if __name__ == '__main__':
    main()
