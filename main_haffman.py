import pickle
codes   = {}
def compare(orig,small):
    print("-=-=-=-=-=-=-")
    print(f"Needed byte for Original String :{8*(len(orig))}")
    print(f"Needed byte for Huffman code :{len(small)}")
    print("-=-=-=-=-=-=-")

def decodeform():
    try:
        filename = input("enter file name : ")
        with open(f"ttree_{filename}","rb") as x:
            ttreefile = pickle.load(x)
        smallfile = open(f"small_{filename}").read()
        assignCodes(ttreefile)
        print(f"ttree : {ttreefile}")
        print("-------------")
        for t in codes:
            print(f"{t} : {codes[t]}")
        print("-------------")
        print(f"Encode : {smallfile}")
        print(f"Lenth Encode : {len(smallfile)}")
        original = decode(ttreefile, smallfile)
        print(f"Decode : {original}")
        print(f"Lenth Decode : {len(original)}")
        compare(original,smallfile)
    except:
        print("Error !")
        decodeform()

def encodeselectmode():
    mode = input("Select Mode (text or file):")
    strr = getstrr(mode)
    encodeform(strr)

def encodeform(strr):
    try:
        print(f"Lenth Decode : {len(strr)}")
        freqs = frequency(strr)
        tuples = sortFreq(freqs)
        tree = buildTree(tuples)
        ttree = trimTree(tree)
        assignCodes(ttree)
        small = encode(strr)
        print(f"ttree : {ttree}")
        print("-------------")
        for t in codes:
            print(f"{t} : {codes[t]}")
        print("-------------")
        print(f"Encode : {small}")
        print(f"Lenth Encode : {len(small)}")
        compare(strr,small)
        boolsave = input("Save data ?(y or n) : ")
        if boolsave == "y":
            filesave(ttree,small)
    except:
        print("Error !")
        return

def getstrr(mode):
    if mode == "text" or mode == "t":
        strr = input("Enter : ")
        return strr
    else:
        try:
            filename = input("Enter file name : ")
            strr = open(filename).read()
            print(f"text : {strr}")
            return strr
        except:
            print("Error !")
            getstrr(mode)

def frequency (strr) :
    freqs = {}
    for ch in strr :
        freqs[ch] = freqs.get(ch,0) + 1
    return freqs

def filesave(ttree, small):
    filename = input("enter file name : ")
    with open(f"ttree_{filename}","wb")as x:
        pickle.dump(ttree,x)
    smallfile = open(f"small_{filename}","w")
    smallfile.write(small)
    smallfile.close()

def sortFreq (freqs) :
    letters = freqs.keys()
    tuples = []
    for let in letters :
        tuples.append((freqs[let],let))
    tuples.sort()
    return tuples

def buildTree(tuples) :
    while len(tuples) > 1 :
        leastTwo = tuple(tuples[0:2])                  
        theRest  = tuples[2:]                          
        combFreq = leastTwo[0][0] + leastTwo[1][0]     
        tuples   = theRest + [(combFreq,leastTwo)]     
        tuples = sorted(tuples, key=lambda x: x[0])
    return tuples[0]            

def trimTree (tree) :
    p = tree[1]                                    
    if type(p) == type("") : return p              
    else : return (trimTree(p[0]), trimTree(p[1])) 

def assignCodes (node, pat='') :
    global codes
    if type(node) == type("") :
        codes[node] = pat                
    else  :                              
        assignCodes(node[0], pat+"0")    
        assignCodes(node[1], pat+"1")    

def encode (strr) :
    global codes
    output = ""
    for ch in strr : output += codes[ch]
    return output

def decode (ttree, small) :
    output = ""
    p = ttree
    for bit in small :
        if bit == '0' :
            p = p[0]     
        else :
            p = p[1]     
        if type(p) == type("") :     
            output += p              
            p = ttree                 
    return output

def main () :
    mode = input("Select Mode (decode or encode):")
    if (mode == "encode") or (mode == "e"):
        encodeselectmode()
    elif (mode == "decode") or (mode == "d"):
        decodeform()
    else:
        print("Error !")
        main()

while(True):
    main()
