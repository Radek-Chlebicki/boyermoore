import sys; # teststring = "cgtt?gatgccga";
# Radek Chlebicki 29175224

#"                20"
teststringrep = "zarray [ a, b, a, c, a, b, a, c, a, b, a]"
teststring1 = "abacabacaba";
teststring2 = "??acabacaba";
teststring3 = "?bacabacaba"
#
# print(teststringrep);

"""
Strategy 

This uses a modified boyermoore method 

firstly i have implemented the equ function which is a standin for == where if any of the args are ? the return is true

Cases for the consideration of wildcards within the pattern: 
    1) leading wildcards as in ???tgat?ccg? can be ignored as they will match. the three leading wildcards are counted
     and wcf = 3. This means that at the beginning of the comparison when  j = 0 (index in pattern) 
     we can jump straight ahead to j = 3. 
        Thus we will only use the modified z on the remaining tgat?ccg?
    2) wildcards early in the pattern, if while comparing the pattern and the text we have already compared with a
    wildcard and then mismatched, then our good suffix and matched prefix tables are invalid as we have matched the 
    wildcard with an unknown letter and when we shift the pattern it may not match, thus we shift by the bad character
    rule only. 
    
        BAD CHARACTER
        since wildcards are any character they allow for more jumps as one can always jump to a wildcard
    
    3) wildcards late in the pattern, For these wildcards it is likely that we will mismatch before them, thus they 
    improve efficiency as the always match the prefix and increase the likelyhood of there being a good suffix, since 
    the wildcard was not used in matching with an unknown letter in the text but rather as a suffix to the prefix of the
    pattern the shift will not cause the wildcard to match to two different letters
    
    
    
Worst case complexity
    z is O(M) in the worst case
    gs and mp can be done in O(M) 
    boyermoore takes O(NM in the worst case)
    
Average case complexity
    for a text of 398786 chars 
        when there are no wildcards
            pattern: atctgc matches: 113 comparisons: 180385
            pattern: gggcggg matches: 179 comparisons: 152950
            pattern: ggg matches: 11506 comparisons: 223195
        with leading wildcards: 
            pattern: tgacg matches 669 comparisons: 245321
            pattern: ???tgacg matches 669 comparisons: 24520
        with late wildcards 
            pattern tga?g matches 1548 comparisons 254641 
        with early wildcards 
            pattern t?gacg mathces 984 comparisons 478120
    The average case complexity is good. 
    

        
    
    
"""

# this is the == function modified
# this will match when one arg is a ?
def equ(x,y):
    if x == '?':
        return True;
    elif y == '?':
        return True;
    else:
        return x == y;

# this has been modified
# the substring the comparison continues as normal
# ? is safe in the substring because if the text matches a letter in the prefix, the ? would have also matched the same letter
# however a ? in the prefix is not permitted, and the comparison breaks of prematurely (when the ? is encountered)
# this is done because a ? in the prefix will during the text search match a letter and get fixed to a letter, however
# when the naive algorithm was being run it may have matched a different letter, thus this naive algorithm has a safety
# aspect introduced
# here the p is the prefix and the t is the body of the pattern where the substring is
# the complexity is still O(M)
# spce complexity is O(M)



def naive(p, t, pi, ti):
    foq = [0] * len(p);
    if pi >= len(p):
        return 0;
    if ti >= len(t):
        return 0;
    numbersimilar = 0;
    while (pi < len(p)):
        # if there is a ? in the prefix the substring wont always match
        if p[pi] == '?'  and not t[ti] == '?':
            break
        elif equ(p[pi],t[ti]):
            numbersimilar += 1;
        else:
            break;
        pi = pi + 1;
        ti = ti + 1;
        if ti >= len(t):
            break;
    return numbersimilar;



# apart from using the modified naive it is same as boyer moore one,
# the offshoot of using the modified naive is that the substrings found will be short if there is a ? in the prefix
# same complexity as stated in the boyer moore file


# this is the z algorithm O(M) when used on the pattern
#
def z(astring):
    astringlen = len(astring);
    zarray = [0] * astringlen;
    zarray[0] = astringlen;

    # this is the left index of the z box
    l = -1;
    # this is the right index of the z-box
    r = -1;
    for i in range(1,astringlen):
        # case when not in zbox
        if i > r:
            zval = naive(astring, astring, 0, i);
            # print(str(i) + " + " + str(zval))
            # print("naive: " + str(zval) + " i "+ str(i));
            if zval >=1:
                zarray[i] = zval;
                l = i;
                r = i + zval - 1;
        else:
            # case where we fit in zbox
            if zarray[i-l] < r - i + 1:
                zarray[i] = zarray[i-l];
                # zval = naive(astring, astring, 0, i);
                # zarray[i] = zval;
            # case where we exceed the zbox
            else:
                zval = naive(astring, astring, r-i+1, r +1);
                zarray[i] =  zval + r - i + 1
                # zarray[i] = r + 1 + zval  - i
                l = i;
                r = r + 1 +  zval - 1;
                # zval = naive(astring, astring, 0, i);
                # zarray[i] = zval;
        # zarrayr = reversearray(zarray);
    # print("zarray " + str(zarray) )
    return zarray;

# def z(astring):
#     astringlen = len(astring);
#     zarray = [0] * astringlen;
#     zarray[0] = astringlen;
#     l = -1;
#     r = -1;
#     for i in range(1,astringlen):
#         # not in box
#         if i > r:
#             zval = naive(astring, astring, 0, i);
#             # print("naive: " + str(zval) + " i "+ str(i));
#             if zval >=1:
#                 zarray[i] = zval;
#                 l = i;
#                 r = i + zval - 1;
#             else:
#                 # case where we fit in zbox
#                 if zarray[i - l] < r - i + 1:
#                     zarray[i] = zarray[i - l];
#                     # zval = naive(astring, astring, 0, i);
#                     # zarray[i] = zval;
#                 # case where we exceed the zbox
#                 else:
#                     zval = naive(astring, astring, r - i + 1, r + 1);
#                     zarray[i] = zval + r - i + 1 - 1
#                     # zarray[i] = r + 1 + zval  - i
#                     l = i;
#                     r = r + 1 + zval - 1;
#                     # zval = naive(astring, astring, 0, i);
#                     # zarray[i] = zval;
#
#             # zarray[i] = zval;
#         # zarrayr = reversearray(zarray);
#     print("zarray " + str(zarray) )
#     return zarray;
# # z(teststring1)
# z(teststring2)
# z(teststring3)


# creates the bad char array, each cell contains the index of the char to jump to
# this is O(128M).
# and space complexity is O(128M)

# the bad char array needs to specify for each index the position of the next letter requested
def fillbadchars(astring):

    badchars = [[len(astring) for x in range(len(astring))] for y in range(128)];
    for i in range(len(astring)):
        if astring[i] == '?':
            for j in range(128):
                badchars[j][i] = i;
        else:
            badchars[ord(astring[i])][i] = i;
    for j in range(128):
        for i in range(len(astring)-2, -1, -1):
            if badchars[j][i] == len(astring):
                badchars[j][i] = badchars[j][i+1];


    # print(badchars)
    return badchars;





# same as boyermoore file
def goodsuffix(astring):
    zarray = z(astring);
    gs = [0] *(1 + len(zarray));
    #start at the last index which is len as 0th index is the dash space
    for i in range(len(zarray)-1, -1, -1):
        gs[0+zarray[i]] = i;
    # print("gs   : " + str(gs));
    return gs;

# same as boyermoore file
# def matchedprefix(astring):
#     zarray = z(astring);
#     mparray = [0] * len(zarray);
#     mparray =[[0 for x in range(2)] for y in range(len(zarray))];
#     for i in range(len(zarray)-1, 0, -1):
#         # reaches the end is a prefix
#         if zarray[i] + i == len(zarray):
#             mparray[len(zarray) - i][0] = i;
#             fillinit = len(zarray) - i;
#             for j in range(len(zarray) - i , len(zarray)):
#                 mparray[j][0] = i;
#                 mparray[j][1] = fillinit;
#     print("mparray" + str(mparray));
#     return mparray;

def matchedprefix(astring):
    zarray = z(astring);
    # mparray = [0] * len(zarray);
    mparray =[[0 for x in range(2)] for x in range(len(zarray)+1)];
    for i in range(len(zarray)-1, -1, -1):
        # reaches the end is a prefix
        if zarray[i] + i == len(zarray):
            mparray[len(zarray) - i][0] = i;
        else:
            mparray[len(zarray) - i][0] = mparray[len(zarray) - i - 1][0]
            # fillinit = len(zarray) - i;
            # for j in range(len(zarray) - i , len(zarray)):
            #     mparray[j][0] = i;
            #     mparray[j][1] = j;
    # print("mparray" + str(mparray));
    return mparray;

# wcf is an optimization, whereby leading ? are counted and then removed from the pattern
# we know that leading ? will always match whatever they are given, thus they are not compared and the text and the pattern
# can be advanced by the number of ? immediately
# wcff is the flag whereby whenever we reset i and j (text and pattern pointer) we will add the wcf amount to i to
# account for the leading ?
# also since we ignore the leading ? we make the good suffix, matched prefix and z arrays for the remainder of the pattern
# without the leading ?
# since all our good suffix and matched prefix are without the number of leading ? we must add wcf back to the values
#
# O(n+m)
# average case between n/m  and n+m , but closer to n/m as it is still jumping but matching substrings are shorter
#
def mirrorall(astring,apattern):
    # how many to skip forward
    wcf = 0;
    wcff = False;
    for i in range(len(apattern)):
        if apattern[i] == '?':
            wcf +=1 ;
            wcff = True;
        else:
            break;




    # print("wcf " + str(wcf));
    apatternold = "";
    for i in apattern:
        apatternold = apatternold + i;
    apattern = apatternold[wcf:len(apattern)];
    # print(apattern);

    j = 0;
    i = len(astring) - len(apatternold) ;
    # print("." + apatternold + ".")
    badchars = fillbadchars(apattern);
    gs = goodsuffix(apattern);
    mparray = matchedprefix(apattern);
    count = 0;
    countoccurance = 0;
    l = i;
    r = 0;
    gf = False;
    ibc = 0;
    igs = 0;
    qenc = False;

    # print("gs at 0 " + str(i));


    outputarr = [] ;
    while i >= 0:
        # if count == 2:
        #     break


        # if gf and (i == l):
        #     gf = False;
        #     i = i + r;
        #     j = j + r;

        # we know that leading wildcards will match
        if wcff:
            i = i + wcf;
            j = j + wcf;
            wcff = False;
        # print("hi")
        # print([i,j])
        # print(astring[i])
        #
        # print(apattern[j-wcf])
        # print(equ(astring[i], apattern[j-wcf]))

        # pattern is shorter due to not having leading chars

        if equ(astring[i],apattern[j-wcf]):
            if apattern[j-wcf] == '?':
                qenc = True

            j = j + 1;
            i = i + 1;

            if j-wcf == len(apattern):

                # print("pattern found at index = " + str(i - j) + " the pattern is " + astring[i-j:i]);

                outputarr.append(i-j);

                countoccurance += 1;


                # shift 1 char
                # i = i - j - 1;
                # j = 0;
                # wcff = True
                # matched prefix when pattern matches

                # if mparray[j-wcf][0] != 0:
                #     l = i - j;
                #     r = mparray[j-wcf][1] - 1;
                #     i = i - j - mparray[j-wcf][0];
                #     gf = True;
                # wcff = True;

                if mparray[-2][0] != 0 :
                    # l = i - j;
                    # r = mparray[j][1] - 1;
                    i = i - j - mparray[-2][0] -wcf ;
                    jump = 0;
                    j = 0;
                    # gf = True;
                    # print("matched mp ")
                    wcff = True
                else:
                    # we will just shift one to the left in i and reset j if the matched prefix
                    # is not useful
                    i = i - j - 1;
                    jump = 0;
                    j = 0;
                    wcff = True
                    # gf = False;
                    # print("unmatched mp")
                qenc = False;


        else:
            if len(astring) == badchars[ord(astring[i])][j-wcf]:
                ibc = i - j - 1;
            else:
                ibc = i - j - (badchars[ord(astring[i])][j-wcf] - (j-wcf) ) ;
            # print("kvnfjbjfbjfnb")
            # print(astring[i-j:i])
            # print('??' + apattern[0:j-wcf])
            # print(astring[i-j: i-j + 12])
            # print('??' + apattern)
            # print("astring is " + astring[i] + " apattern is " + apattern[j-wcf])
            # print("i: " + str(i))
            # print("j: " + str(j))
            # print("i-j " + str(i-j))
            # print("ibc " + str(ibc))
            # print("fknbjfbjfnvjf")


            # here rewind
            # align in beginning
            if j-wcf == 0:
                igs = i - j - 1

            elif gs[j-wcf] != 0:
                igs = i - j - gs[j-wcf] ;
                # print("gs")
            else:
                if mparray[j-wcf][0] != 0 :
                    igs = i - j - mparray[j-wcf][0]  ;
                    # print("mp")
                else:
                    igs = i - 1 - j;



            # igs = ibc + 1;
            if (qenc or ibc < igs) or True:
                i = ibc;
                # if we used bad character do not use galil optimization
                # print("ibc")
            else:
                i = igs;
                # print("igs")
            # i = ibc;
            j = 0;
            wcff = True;
            qenc = False;
        count += 1;
        # print(i)

    # print(wcf)
    # print("z " + str(z(apattern)))
    # print(gs)
    # print("ran mirrorall " + "count : " + str(count) + " i : " + str(i));
    print("countoccurance all : " + str(countoccurance));
    return outputarr;


# matched prefix, slide 38, only used when good suffix is zero
# what to do when pattern matches
# galils optimization, slide 41
# infile =  open('genomeout.txt', 'r');
# astring = infile.read().replace('\n', '').replace(" ", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "");
# infile.close();
#
# infile =  open('geneout.txt', 'r');
# apattern = infile.read().replace('\n', '').replace(" ", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "");
# infile.close();
#
# apattern = "ggggtg" # 282 - this one does not match
# apatternouter = "cgttgatgccga" # 2
# apatternouter = "?????????cga" # 2

# apatternouter =   "???tgat?ccg?" # 2
# apatternouter = "cgttga?gcc??" # 3
#

# apattern = "gcgcaggg" #20
# apattern = "gcgcaggg" #20

# apattern = "cct" # 6732
#
# astring = astring[1:10000]

# mirrorall(astring, apatternouter);
if __name__ == "__main__":
    textfilename = sys.argv[1];
    # print(textfilename)
    patternfilename = sys.argv[2];
    # print(patternfilename)

    atext = open(textfilename, 'r').read();
    apattern = open(patternfilename, 'r').read();
    print(len(apattern))

    out = open("output_wildcard_matching.txt", 'w');

    outputarr = mirrorall(atext, apattern);
    for i in range(len(outputarr)-1, -1, -1):
        print(str(outputarr[i] + 1), file=out);
    # print("hi", file=out)






# print(equ('?','1'));
# badchars = fillbadchars(teststring);
#
# print(badchars[ord('x')][1])

