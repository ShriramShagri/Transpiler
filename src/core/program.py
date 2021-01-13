from .keywords import K_SET_1

class Program:
    def __init__(self, inputLines):
        self.inputLines = inputLines
        self.comment = False
        self.indent = 0
        self.brackets = []
        self.programlines = []
    
    def __repr__(self):
        return '\n'.join(self.programlines)
    
    def generate(self, path):
        temp = []
        for line in self.inputLines:
            if line == '\n':
                continue
            elif '/*' in line:
                t = line.split('/*')
                temp.extend([t[0], '/*'+t[1]])
            elif '//' in line:
                if line.strip()[:2] == '//':
                    temp.append(line)
                else:
                    count = 0
                    for i in line:
                        if i == ' ':
                            count += 1
                        else:
                            break
                    t = line.split('//')
                    temp.extend([t[0], (' '*count)+'//'+t[1]])
            else:
                temp.append(line)
        self.inputLines = list(filter(lambda x: False if x=='\n' or x == '' else True, temp))
        for line in self.inputLines:
            if self.comment:
                if '*/' in line:
                    self.comment = False
                self.programlines.append(line)
            else:
                if line == '\n' or '//' in line:
                    self.programlines.append(line)
                elif '/*' in line:
                    self.programlines.append(line)
                    self.comment = True
                else:
                    line = line.strip('\n').rstrip()
                    if line == '':
                        continue
                    line = self._indent(line)
                    line, linetype = self._checkKeywords(line)
                    if linetype:
                        line, linetype = self._colon(line)
                        if linetype:
                            line = self._semicolon(line)
        
        if self.indent > 0:
            self.programlines.extend(['}']*int(self.indent))
        
        with open(path.split('.tr')[0] + '.c', 'w') as outfile:
            for line in self.programlines:
                outfile.write(line + '\n')

    
    def _indent(self, line):
        count = 0
        for i in line:
            if i == ' ':
                count += 1
            else:
                break
        if (count/4).is_integer():
            if count/4 < self.indent:
                bracketCount = self.indent - count/4
                self.programlines.extend([' '*(int(self.indent)*4-1) + '}']*int(bracketCount))
                self.indent = count/4
            elif count/4 > self.indent:
                raise SyntaxError()
        return line

    def _checkKeywords(self, line):
        linetype = True
        for words in K_SET_1:
            if words in line:
                linetype = False
                self.programlines.append('#' + line.strip())
                return '#' + line.strip(), linetype
        return line, linetype

    def _semicolon(self, line):
        finalline = line.rstrip() + ';'
        self.programlines.append(finalline)
        return finalline

    def _colon(self, line):
        if line[-1] == ':':
            self.indent += 1
            self.programlines.append(line[:-1])
            self.programlines.append(' '*(int(self.indent)*4-1) + '{')
            return line.replace(':', ''), False
        return line, True