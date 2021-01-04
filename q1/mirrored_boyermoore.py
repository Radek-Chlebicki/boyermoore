
import sys;
# Radek Chlebicki 29175224

'''
comments before functions 

Average case
        empirical analysis reveals for a text of  chars,
         151768 comparisons to find 179 instances of the pattern gggcggg
         221163 comparisons to find 11506 instances of the pattern ggg
         157063 comparisons to find 266 instances of the pattern atctc
    thus the average case is no where near the worst case in fact 
    for these cases it is less than n + m 

'''


# this is the naive implementation it will compare the letters of pattern p and letters of text t starting at index
# ti and pi. in worst case this will be O(M), the length of the pattern
def naive(p, t, pi, ti):
    if pi >= len(p):
        return 0;
    if ti >= len(t):
        return 0;
    numbersimilar = 0;
    while (pi < len(p)):
        if p[pi] == t[ti]:
            numbersimilar += 1;
        else:
            break;
        pi = pi + 1;
        ti = ti + 1;
        if ti >= len(t):
            break;
    return numbersimilar;

# print(naive(teststring, teststring, 0,0));

# unused
# def reversearray(alist):
#     rlist = [0] * len(alist);
#     for i in range(len(alist)):
#         rlist[len(alist)-i-1] = alist[i];
#     return rlist;

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
    print("zarray " + str(zarray) )
    return zarray;


# creates the bad char array, each cell contains the index of the char to jump to
# this is O(128M).
# and space complexity is O(128M)

# the bad char array needs to specify for each index the position of the next letter requested
def fillbadchars(astring):

    badchars = [[len(astring) for x in range(len(astring))] for y in range(128)];
    for i in range(len(astring)):
        badchars[ord(astring[i])][i] = i;
    for j in range(128):
        for i in range(len(astring)-2, -1, -1):
            if badchars[j][i] == len(astring):
                badchars[j][i] = badchars[j][i+1];



    return badchars;





# create goodsuffix array
# uses zarray to make goodsuffix, O(M)
# in my case the goodsuffix array takes the index at which the mismatch occurs and
# returns  the index in the pattern where the good suffix begins
# space complexity O(M)
def goodsuffix(astring):
    zarray = z(astring);
    gs = [0] *(1 + len(zarray));
    #start at the last index which is len as 0th index is the dash space
    for i in range(len(zarray)-1, -1, -1):
        # if gs[zarray[i]] < i : # and i > zarray[i]:
        gs[0+zarray[i]] = i;
    print("gs: " + str(gs));
    return gs;

# print("goodsuffix")
# print(goodsuffix(teststring));
# print(goodsuffix("acababacaba"))


# matched prefix 1:16 of ian, it is same as last q of tute 02


# uses z array to find prefixes and matching suffix
# given the index of the mismatch the matchedprefix array returns the index where the suffix begins
# it is O(M)
# the space complexity is  O(M)
def matchedprefix(astring):
    zarray = z(astring);
    # mparray = [0] * len(zarray);
    mparray =[0 for x in range(len(zarray) +1)];
    for i in range(len(zarray)-1, -1, -1):
        # reaches the end is a prefix
        if zarray[i] + i == len(zarray):
            mparray[len(zarray) - i] = i;
        else:
            mparray[len(zarray) - i] = mparray[len(zarray) - i -1]
            # fillinit = len(zarray) - i;
            # for j in range(len(zarray) - i , len(zarray)):
            #     mparray[j][0] = i;
            #     mparray[j][1] = j;
    print("mparray" + str(mparray));
    return mparray;
# print(goodsuffix("GCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGGCGGG"))
#
# print(matchedprefix("GCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGGCGGG"))

# this is the full boyer moore implementation
# avg case is n/m
# O(n+m)

def mirrorall(astring,apattern):
    j = 0;
    # i points to the position in the text where we start comparing
    # since we start at the right end of the text, i will move to 0 slowly (move to the left)
    # however we compare with pattern left to right thus i will move to the right, until there
    # is a match or a mismatch then i will be decremented again
    i = len(astring) - len(apattern);
    badchars = fillbadchars(apattern);
    # print("hi")
    # print(badchars[ord('t')][5])
    gs = goodsuffix(apattern);
    mparray = matchedprefix(apattern);
    count = 0;
    countoccurance = 0;

    # l = i;
    # r = 0;
    # gf is the galil flag, when true it means that matched prefix or good suffix have been used
    # when the gf is true the length of the substring skipped is added to i and j, so that we skip
    # comparing them again
    gf = False;

    # ibc is the new candidate i position according to the bad character array
    ibc = 0;
    # igs is the new candidate i position according to the good suffix and matched prefix array
    igs = 0;
    outputarr = [];
    jump = 0;
    its = 0;
    mpc = False;
    while i >= 0:
        # break;

        # galils optimization step
        # if gf and (i == l):
        #     gf = False;
        if i == its:
            i = i + jump;
            j = j + jump;
            jump = jump-jump;
            its = 0;
        #
        # i = i + jump;
        # j = j + jump;
        # jump = jump - jump;
        # print([i, j])
        # if j<0:
        #     # print(jump)
        #     break

        # print([i,j])
        # check if the chars in the pattern and in the text match
        if astring[i] == apattern[j]:
            j = j + 1;
            i = i + 1;
            # print("jvnfnjjfnv")

            # check if we have found the pattern
            if j == len(apattern):
                # print("pattern found at index = " + str(i - j) + " the pattern is " + astring[i-j:i]);
                outputarr.append(i-j);
                countoccurance += 1;

                # matched prefix when pattern matches
                if mparray[-2] != 0:
                    # l = i - j;
                    # r = mparray[j][1] - 1;
                    i = i - j - mparray[-2];
                    jump = 0;
                    j = 0;
                    # gf = True;
                    # print("matched mp ")
                else:
                    # we will just shift one to the left in i and reset j if the matched prefix
                    # is not useful
                    i = i - j - 1;
                    jump = 0;
                    j = 0;
                    # gf = False;
                    # print("unmatched mp")

        # this is the case where the match did not occur
        else:

            #using the badchar array to find the new i position
            if len(astring) == badchars[ord(astring[i])][j]:
                ibc = i - j - 1;
                jump = 0;
            else:
                ibc = i - j - (badchars[ord(astring[i])][j] - j) ;
                jump = 0;

            # using the good suffix array to find the new i position
            if gs[j] != 0:
                # l = i - j;
                # r = j;
                igs = i - j - gs[j] ;

                # gf = True;
                if j > 0:
                    jump = j - 1 ;
                    its = i - j;
                    # jump = 0;
                # print("j: " + str(j) + " " + "i: " + str(i) + " " + " gs[j] " + str(gs[j]));

            # if there is no good suffix, then we shall see if we can use the matched prefix
            else:
                if mparray[j] != 0:
                    # l = i - j;
                    # r = mparray[j][1] - 1;
                    igs = i - j - mparray[j];
                    # gf = True
                    jump = 0;
                    mpc = True;

                    # print("mp")
                # if there is no matched prefix then we shall just move one char
                else:
                    igs = i - 1 - j;
                    jump = 0;
                    # print("igs else");
                    # gf = False;
            # here we will choose between igs and ibc and take the one that gives the better jump
            # ibc = igs + 1;
            # igs = ibc + 1;

            # if not mpc:
            # if j == 0:
            #     print(j)

            if ibc < igs  :
                i = ibc;
                jump = 0;
                its = 0;
                # print('bc')
                # if gf == True:
                #     gf = False;
            else:
                i = igs;
            # else:
            #
            #
            #     if ibc > igs:
            #         i = ibc;
            #         jump = 0;
            #         # if gf == True:
            #         #     gf = False;
            #     else:
            #         print("mpc chose igs")
            #         i = igs;

            j = 0;
            mpc = False;
        count += 1;

    # print(z("GCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGGCGGG"))
    # print(gs)
    # print(mparray)
        # print(i)

    print("ran mirrorall " + "count : " + str(count) + " i : " + str(i));
    print("countoccurance all : " + str(countoccurance));
    (z(apattern))
    # print(gs)
    # print(mparray)
    # print(badchars)
    return outputarr;





if __name__ == "__main__":
    textfilename = sys.argv[1];
    # print(textfilename)
    patternfilename = sys.argv[2];
    # print(patternfilename)

    atext = open(textfilename, 'r').read();
    apattern = open(patternfilename, 'r').read();
    # print(len(apattern))

    out = open("output_mirrored_boyermoore.txt", 'w');

    outputarr = mirrorall(atext, apattern);
    for i in range(len(outputarr)-1, -1, -1):
        print(str(outputarr[i] + 1), file=out);
    # print("hi", file=out)
    # print("hi", file=out)