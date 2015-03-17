import sys

def main():
    homophones = {'its', "it's", 'your', "you're", 'their', "they're", 'lose', 'loose', 'to', 'too',
                  'Its', "It's", 'Your', "You're", 'Their', "They're", 'Lose', 'Loose', 'To', 'Too'}

    flip = {'its':"it's", "it's":'its', 'your':"you're", "you're":'your', 'their':"they're", 
            'Its':"It's", "It's":'Its', 'Your':"You're", "You're":'Your', 'Their':"They're", 
            "they're":'their', 'lose':'loose', 'loose':'lose', 'to':'too', 'too':'to',
            "They're":'Their', 'Lose':'Loose', 'Loose':'Lose', 'To':'Too', 'Too':'To'}

    truefile = open(sys.argv[1])
    errfile = open(sys.argv[2])
    outfile = open(sys.argv[3])

    line_num = 0

    err = 0
    fixed = 0
    nerr = 0
    kept = 0

    for tline in truefile:
        line_num += 1
        eline = errfile.readline()
        oline = outfile.readline()

        ttok = tline.split()
        etok = eline.split()
        otok = oline.split()

        num_otok = len(otok)

        if num_otok != len(ttok) or num_otok != len(etok):
            print('line ' + str(line_num) + 'has different number of tokens.')
            continue
            
        if num_otok == 0:
            continue
            
        tcand = [word for word in ttok if word in homophones]
        ecand = [word for word in etok if word in homophones]
        ocand = [word for word in otok if word in homophones]

        num_ocand = len(ocand)

        if num_ocand != len(tcand) or num_ocand != len(ecand):
            print('line ' + str(line_num) + 'has different number of homophones.')
            continue
            
        if num_ocand == 0:
            continue

        # need total number of homophones
        # need number of correct homophones from me

        #right += len([1 for i, word in enumerate(ocand) if word == tcand[i]])
        #total += num_ocand
        enum_ocand = list(enumerate(ocand))
        
        thiserr = len([1 for i, word in enumerate(ecand) if word != tcand[i]])
        err += thiserr
        fixed += len([1 for i, word in enum_ocand if ecand[i] != tcand[i] and word == tcand[i]])
        
        nerr += num_ocand - thiserr
        kept += len([1 for i, word in enum_ocand if ecand[i] == tcand[i] and word == tcand[i]])

    truefile.close()
    errfile.close()
    outfile.close()

    total = err + nerr
    correct = fixed + kept
    accu = correct / total
    fixr = fixed / err
    kepr = kept / nerr
    
    recall = fixr
    bad_changes = nerr-kept
    total_changes = fixed + bad_changes
    precision = fixed / total_changes
    f_score = (2*precision*recall)/(precision+recall)

    print('correct: ' + str(correct))
    print('total: ' + str(total))
    print('accuracy: ' + str(accu))
    print()
    print('fixed: ' + str(fixed))
    print('err: ' + str(err))
    print('fixed rate: ' + str(fixr))
    print()
    print('kept: ' + str(kept))
    print('nerr: ' + str(nerr))
    print('kept rate: ' + str(kepr))
    print()
    print()
    print()
    print('correct changes: ' + str(fixed))
    print('required changes: ' + str(err))
    print('recall: ' + str(recall))
    print()
    print('correct changes: ' + str(fixed))
    print('total changes: ' + str(total_changes))
    print('precision: ' + str(precision))
    print()
    print('f-score: ' + str(f_score))


if __name__ == '__main__':
    main()
