
def write(filename, words):
    swords = words.keys()
    swords.sort()

    f = file(filename, 'w')
    for word in swords:
        if 'translations' in words[word] or 'related' in words[word] or 'wikipedia' in words[word]:
            f.write('%s\n' % word.encode('utf-8'))

        if 'translations' in words[word] and len(words[word]['translations']) > 0:
            f.write(' '*4 + 'T\n')
            for tr in words[word]['translations']:
                f.write(' '*8 + '%s\n' % tr.encode('utf-8'))
        if 'related' in words[word] and len(words[word]['related']) > 0:
            f.write(' '*4 + 'R\n')
            for tr in words[word]['related']:
                f.write(' '*8 + '%s\n' % tr.encode('utf-8'))
        if 'wikipedia' in words[word] and len(words[word]['wikipedia']) > 0:
            f.write(' '*4 + 'W\n')
            if type(words[word]['wikipedia']) == str or type(words[word]['wikipedia']) == unicode:
                f.write(' '*8 + '%s\n' % words[word]['wikipedia'].encode('utf-8'))
            else:
                for w in words[word]['wikipedia']:
                    f.write(' '*8 + '%s\n' % w.encode('utf-8'))
        if 'required' in words[word]:
            f.write(' '*4 + 'R_E_Q_U_I_R_E_D\n')
    f.close()

def read(filename):
    f = file(filename)

    words = {}
    word = None
    mode = None
    for line in f:
        if line[0] != ' ':
            word = line.strip().decode('utf-8')
            if word not in words:
                words[word] = {'translations': [], 'related': [], 'wikipedia': []}
        else:
            if line[4] == 'T':
                mode = 'translations'
            elif line[4] == 'R':
                mode = 'related'
            elif line[4] == 'W':
                mode = 'wikipedia'
            elif line[4] == ' ':
                if line.strip():
                    words[word][mode].append(line.strip().decode('utf-8'))
            else:
                print 'WTF'
    f.close()

    return words

