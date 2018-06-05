class MmaShortener:
    def one_line(self, text):
        """
        remove line breaks
        :param text: str
        :return: str
        """
        new_text = ""
        for i in range(len(text)):
            c = text[i]
            if c == "\n":
                continue
            new_text += c
        return new_text

    def open_file(self, file):
        """
        open file to get content
        :param file: str (file path)
        :return: str (text content)
        """
        with open(file, 'r') as f:
            content = f.read()
        return content

    def write_file(self, file, text):
        """
        write text to file
        :param file: str (destination file path)
        :param text: str (file content)
        :return: none
        """
        with open(file, 'a') as f:
            f.seek(0)
            f.truncate()
            f.write(text)

    def contains_vars(self, text, word):
        """
        test content contains target variable
        :param text: str (text content)
        :param word: str (target variable)
        :return: bool (True: contains)
        """
        is_comment = False
        wl = len(word)
        i = 1
        text = "#" + text + "#"
        while i < len(text) - wl:
            if text[i] == "\"":
                is_comment = not is_comment
            if text[i] == "(" and text[i + 1] == "*":
                while not (text[i] == "*" and text[i + 1] == ")"):
                    i += 1
                i += 2
            if i >= len(text) - wl:
                break
            string = text[i:i + wl]
            if not is_comment and string == word and not (text[i - 1].isalpha() or text[i - 1].isalnum()) and not (
                    text[i + wl].isalpha() or text[i + wl].isalnum()):
                return True
            i += 1
        return False

    def vars_dict(self, text, var):
        """
        convert variables to shorten form
        :type text: str
        :param var: list() (variable list)
        :return: list(list()) (map for substitute shorten text form)
        """
        var = list(set(var))
        var.sort()
        var.reverse()
        letters = [chr(ord('a') + x) for x in range(26)]
        letter_nums = [str(x) for x in range(10)] + letters + [chr(ord('A') + x) for x in range(26)]
        result = []
        ignore_vars = []
        used_vars = []
        # less than letters length
        i = 0
        while len(var) > 0 and i < len(letters):
            if self.contains_vars(text, letters[i]):
                ignore_vars.append(letters[i])
                i += 1
                continue
            result.append([var.pop(), letters[i]])
            used_vars.append(letters[i])
            i += 1
        # more than letters
        current_letter = []
        last_letter = letters
        if len(var) > 0:
            while len(var) > 0:
                for j in range(len(last_letter)):
                    for i in range(len(letter_nums)):
                        built_letter = last_letter[j] + letter_nums[i]
                        current_letter.append(built_letter)
                        if self.contains_vars(text, built_letter):
                            ignore_vars.append(built_letter)
                            continue
                        if len(var) > 0:
                            result.append([var.pop(), built_letter])
                            used_vars.append(built_letter)
                        else:
                            break
                    if len(var) == 0:
                        break
                last_letter = current_letter
        # replace the ignored vars
        while len(ignore_vars) > 0:
            result.append([used_vars.pop(), ignore_vars.pop()])
        return result

    def str_replace(self, text, word, sub):
        """
        replace string for MMA
        :param text: str (content text)
        :param word: str (word)
        :param sub: str (substitute for word)
        :return: str
        """
        is_comment = False
        string_builder = ""
        wl = len(word)
        i = 1
        text = "#" + text + "#"
        while i < len(text) - wl:
            if text[i] == "\"":
                is_comment = not is_comment
            if text[i] == "(" and text[i + 1] == "*":
                while not (text[i] == "*" and text[i + 1] == ")"):
                    i += 1
                i += 2
            if i >= len(text) - wl:
                break
            string = text[i:i + wl]
            if not is_comment and string == word and not (text[i - 1].isalpha() or text[i - 1].isalnum()) and not (
                    text[i + wl].isalpha() or text[i + wl].isalnum()):
                string_builder += sub
                i += wl
            else:
                string_builder += text[i]
                i += 1
        while i < len(text) - 1:
            string_builder += text[i]
            i += 1
        return string_builder

    def str_substitute(self, text, subs):
        """
        substitute all vars with shorten form
        :param text: str (content text)
        :param subs: list(list()) (map for substitute shorten text form)
        :return: str (result text)
        """
        for i in range(len(subs)):
            text = self.str_replace(text, subs[i][0], subs[i][1])
        return text

    def str2list(self, string):
        """
        var strings to list for python
        :param string: str
        :return: list() (variable list)
        """
        lst = []
        word = ""
        for i in range(len(string)):
            c = string[i]
            if c in {"{", "}", " ", "\n"}:
                continue
            if c != ",":
                word += c
            else:
                lst.append(word)
                word = ""
        lst.append(word)
        return lst

    def remove_comment(self, string):
        """
        remove the comments
        :param string: str
        :return: str
        """
        result = ""
        i = 0
        while i < len(string) - 1:
            if string[i] == "(" and string[i + 1] == "*":
                while i < len(string) - 1 and not (string[i] == "*" and string[i + 1] == ")"):
                    i += 1
                i += 2
            else:
                result += string[i]
                i += 1
        if string[-1] != ")":
            result += string[-1]
        return result

    def shorten(self, file, var):
        """
        main for shorten operation
        :param file: str (file path)
        :param var: list (variable list)
        :return: str (shortened text)
        """
        var = self.str2list(var)
        content = self.open_file(file)
        content = self.one_line(content)
        content = self.remove_comment(content)
        subs = self.vars_dict(content, var)
        content = self.str_substitute(content, subs)
        self.write_file("out.txt", content)
        return content
