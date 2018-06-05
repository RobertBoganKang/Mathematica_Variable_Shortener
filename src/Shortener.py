class Mma:
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

    def vars_dict(self, var):
        """
        convert variables to shorten form
        :param var: list() (variable list)
        :return: list(list()) (map for substitute shorten text form)
        """
        var = list(set(var))
        var.sort()
        var.reverse()
        letters = [chr(ord('a') + x) for x in range(26)]
        letter_nums = [str(x) for x in range(10)] + letters
        result = []
        # less than 26
        i = 0
        while len(var) > 0 and i < 26:
            var_now = var.pop()
            result.append([var_now, letters[i]])
            i += 1
        # more than 26
        current_letter = []
        last_letter = letter_nums
        if len(var) > 0:
            while len(var) > 0:
                for i in range(len(letter_nums)):
                    for j in range(len(last_letter)):
                        if len(var) > 0:
                            built_letter = letters[i] + last_letter[j]
                            current_letter.append(built_letter)
                            var_now = var.pop()
                            result.append([var_now, built_letter])
                        else:
                            break
                    if len(var) == 0:
                        break
                last_letter = current_letter
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
        l = len(word)
        i = 1
        text = "#" + text + "#"
        while i < len(text) - l:
            if text[i] == "\"":
                is_comment = not is_comment

            string = text[i:i + l]
            if not is_comment and string == word and not (text[i - 1].isalpha() and text[i - 1].isalnum()) and not (
                    text[i + l].isalpha() and text[i + l].isalnum()):
                string_builder += sub
                i += l
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
        :param string:
        :return:
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
        ignore = {"[", "]", "{", "}", "_", "=", ""}
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
        subs = self.vars_dict(var)
        content = self.str_substitute(content, subs)
        content = self.remove_comment(content)
        self.write_file("out.txt", content)
        return content
