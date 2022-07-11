class ListStream:
    def __init__(self):
        self.data = []
        self.new_line = True

    def write(self, s: str):
        if not s:
            return
        new_lines = s.count('\n')
        # if \n end
        if s[-1] == '\n':
            # multiple new lines
            if new_lines > 1:
                for line in s[:-1].split('\n'):
                    self.write_line(line)
                    self.new_line = True
            # one new line
            elif len(s) > 1:
                self.write_line(s[:-1])

            self.new_line = True
        else:
            # single string with multiple \n
            if new_lines > 1:
                for line in s.split('\n'):
                    self.write_line(line)
                    self.new_line = True
            else:
                # single string
                self.write_line(s)
            self.new_line = False

    def write_line(self, s):
        if self.new_line:
            self.data.append(s)
        else:
            self.data[len(self.data) - 1] += s

    def flush(self, *args):
        pass
