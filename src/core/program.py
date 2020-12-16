class Program:
    def __init__(self, trLines):
        self.trLines = trLines
        self.indent = 0
        self.flowerBracket = False
    
    def __repr__(self):
        return r'\n'.join(self.programlines)
    
    def generate(self, path):
        cLines = []
        for lines in self.trLines:
            if lines == '\n':
                cLines.append(lines)
            else:
                currentLine = self._translate(lines, '"' in lines)
                if type(currentLine) == list:
                    cLines.extend(currentLine)
                elif type(currentLine) == str:
                    cLines.append(currentLine)
                if self.flowerBracket:
                    cLines.extend(['}']*self.bracketCount)
                    self.bracketCount = 0
                    self.flowerBracket = False
        if self.indent > 0:
            cLines.extend(['}']*self.indent)    
        
        with open(path.split('.tr')[0] + '.c', 'w') as outfile:
            for line in cLines:
                outfile.write(line + '\n')
    
    def _translate(self, line, quote):
        newLine = ''
        self._checkIndent(line)
        line = line.strip().strip('\n')
        if line[-1] == ':':
            newLine = self.rreplace(line, ':') + '\n{'
            self.indent += 1
            return newLine
        if 'include' in line:
            newLine += '#include<' + line.split(' ')[1].strip('\n') + '>'
            return newLine
        return line

    def _checkIndent(self, line):
        count = 0
        for i in line.strip('\n'):
            if i == ' ':
                count += 1
        if (count/4).is_integer():
            if count/4 < self.indent:
                self.flowerBracket = True
                self.bracketCount = self.indent - count/4
                self.indent = count/4
            elif count/4 > self.indent:
                raise SyntaxError()

    
    def rreplace(self, s, old):
        li = s.rsplit(old, 1)
        return ''.join(li)
