import sys;
# Radek Chlebicki 29175224

"""
General strategy 

SP[x][i] is a 2d array that is an expansion over the SPi array. The columns are the longest proper suffix ending at that 
index i in the pattern while the rows are ascii char numbers. 

Normally the SP[i] value is calculated using the z array as such SP[z[i]+i-1] = z[i] (filling from right to left) 
and the stored values represent the longest proper suffix that finishes at i. 

However the modification is as such: 

    We know the letter after the prefix is apattern[sp[i]]. thus sp[apattern[z[i]]][z[i]+i-1] = z[i]

    If z[i] > 1, we know that shorter suffixes are possible: 
    so we can allow for other shifts if we need a specific letter 
    
    our pattern is abct...abcd
    our text is    abct...abca
    if we want a then we will check sp['a'][9] and we should get 0, then our shift will be 10 - 0 
    our pattern is           abct...abcd
    our text is    abct...abca
    
    our pattern is abct...abcd
    our text is    abct...abcc
    if we want c then we will check sp['c'][9] and we should get 2, then our shift will be 10 - 2
    our pattern is         abct...abcd
    our text is    abct...abcc
    
    Thus the sp[x][i] number helps to bring the desired char in the pattern inline with the mismatched char in the 
    text. 
    
    To perform such a fill we loop from k=0 to z[i]+1, we can set sp[apattern[k]][z[i]+1-1] = k
    We go from left to right because for some letter x, if it occurs at multiple Ks in the prefix, we want
    to overwrite sp[apattern[k]][z[i]+1-1] with the largest k. 
    
    For the remaining letters we set sp[x][z[i] + 1 - 1] = z[i] as we proceed we the normal kmp algorithm when we know 
    that the desired letter does not occur in the prefix. 
    
    Processing the pattern of length M, requires in the worst case 
        1) z algorithm which is O(M) 
        2) filling the sp[x][i] array, which is O(128 M) as for every prefix we find we loop over it to find shorter 
            prefixes, also we must fill the values for 128 ascii chars (actually 128-35), however usually there arent tha 
            many i where there is a matching suffix and prefix, and they are usually short
            so in averge it should be slightly more than 128M 
            
        3) then the KMP algorithm itself is O(MN) 
    In the average case: 
        empirical analysis reveals for a text of  chars,
         501828 comparisons to find 179 instances of the pattern gggcggg
         497484 comparisons to find 11506 instances of the pattern ggg
         453098 comparisons to find 266 instances of the pattern atctc
    thus the average case is no where near the worst case

    space wise the sp 2d array requires 128M space
    
"""



# same as mirrored boyermoore
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

# same as mirrored boyer moore
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


#
#
# def sp(astring):
#     zl = z(astring);
#     ps = [[0 for x in range(len(astring))] for y in range(128)];
#     # ps[0-127][0] should not matter
#     for i in range(len(astring)-1, 0, -1):
#         # this is a special situation where we do not know the next char, thus regardless of what char
#         # is next we will still move forward by i- ps[j][i]
#         if i + zl[i]  == len(astring):
#             # print(zl[i])
#             # raise ValueError('A very specific bad thing happened.')
#             for j in range(35,128):
#                 # ps[j][zl[i]] = zl[i];
#                 ps[j][i+zl[i] - 1] = zl[i];
#
#         else:
#             for j in range(35,128):
#                 ps[j][i + zl[i] - 1] = zl[i]  ;
#
#
#             # spi[x] modification
#             for k in range(0, zl[i] + 1):
#                 ps[ord(astring[k])] [i+zl[i] - 1] = k;
#
#
#     return ps;

def sp(astring):
    zl = z(astring);
    ps = [[0 for x in range(len(astring))] for y in range(128)];
    # ps[0-127][0] should not matter
    for i in range(len(astring)-1, 0, -1):
        # this is a special situation where we do not know the next char, thus regardless of what char


        # the base case where we assume that the mismatched letter we desire is not in the prefix/suffix
        for j in range(35,128):
            ps[j][i + zl[i] - 1] = zl[i]  ;


        # spi[x] values for shifts due to the occurance of the desired letter in the prefix
        # this just fills out various different suffix lengths for shorter prefixes that end in the longer prefix

        for k in range(0, zl[i] + 1):
            ps[ord(astring[k])] [i+zl[i] - 1] = k;


    return ps;


# this is the kmp method that uses the ps array
def kmp(astring, apattern):
    ps = sp(apattern);

    # i is the index in the text
    i = 0 ;
    # j is the index in the pattern
    j = 0;
    # this is the number of loops
    count = 0
    # this is the number of occurances of the pattern
    mcou = 0 ;
    # this stores the indeces where the pattern was discovered
    outputarr = [];
    # this is the number to skip due to galil
    jg = 0;
    jgs = 0;

    # print("hi")
    print(len(astring))
    while i + jg < len(astring) :
        # break;
        # print([i,j])
        count += 1;



        if 0 == j:
            i = i + jg ;
            j = j + jg;
            jg = 0;

        # print([i,j])
        if (astring[i] == apattern[j]):
            i = i + 1;
            j = j + 1;
            # this case has an optimization remaining
            if j == len(apattern):
                outputarr = [(i-j)] + outputarr;
                # print("match found at i " + str(i- j) + " and is "  + str(astring[i-j: i]));

                # if a match occurs then match the prefix of the pattern with the suffix of the pattern
                # the suffix is given by ps[len(apattern)-1]
                jg = ps[47][j-1];
                mcou += 1;

                if j == 0:
                    i = i + 1;
                    j = 0;
                    jg = 0;
                else:
                    i = i - j  + ((j) - ps[47][j-1] ) ;
                    j = 0;


        else:
            # # this is the kmp jump calculation
            if j == 0 :
                i = i + 1;
                jg = 0;
                j = 0;
            else:
                jg = ps[ord(astring[i])][j-1];
                i = i - j + ((j) - ps[ord(astring[i])][j-1] ) ;
                j = 0 ;


    # print("ran all : " + str(count));
    print("countoccurance all : " + str(mcou))
    # print("z  " + str(z(apattern)))
    # print("ps " + str(ps[47]))

    # print(ps)
    return outputarr;





# infile =  open('genomeout.txt', 'r');
# astring = infile.read().replace('\n', '').replace(" ", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "");
# infile.close();
#
# infile =  open('geneout.txt', 'r');
# apattern = infile.read().replace('\n', '').replace(" ", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "");
# infile.close();
#
# apattern = "ggggtg" # 282 - this one does not match
# apattern = "cgttgatgccga" # 2
# apatternouter = "c????????cga" # 2

# apatternouter =   "???tgat?ccg?" # 2
# apatternouter = "cgttga?gcc??" # 3


# apattern = "gcgcaggg" #40
# apattern = "gcgcaggg" #20
# apattern = "cct" # 6732
#
# kmp(astring, apattern )

if __name__ == "__main__":
    textfilename = sys.argv[1];
    # print(textfilename)
    patternfilename = sys.argv[2];
    # print(patternfilename)

    atext = open(textfilename, 'r').read();
    apattern = open(patternfilename, 'r').read();
    # print(len(apattern))

    out = open("output_kmp.txt", 'w');

    outputarr = kmp(atext, apattern);
    for i in range(len(outputarr)-1, -1, -1):
        print(str(outputarr[i] + 1), file=out);
    # print("hi", file=out)
    # sys.exit(len(outputarr))































































































































