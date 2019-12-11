#!/usr/bin/env python







def getExactData(st):
    #print(st)
    start = st.find('seconds.')+9;
    text=st[start:]
    #print("\n "+text)
    s=text
    tab=[]

    while len(s)>0 :
        start = s.find(':')
        end = s.find('%', start)
        tab.append(s[:start])
        s=s[end+2:]

    #print(tab)
    #print(s)
    return list(set(tab))











if __name__ == '__main__':
    st="""truth_thresh: Using default '1.000000'
Loading weights from yolov3.weights...Done!
data/dog.jpg: Predicted in 0.029329 seconds.
dog: 99%
truck: 93%
bicycle: 99%"""
    print(getExactData(st))

