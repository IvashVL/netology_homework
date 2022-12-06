class FileGenerator:
    def __init__(self):
        self.files = dict()

    def read_files(self, *files):
        for file in files:
            with open(file, encoding='utf-8') as f:
                text = f.readlines()
                self.files.update({file: {'length': len(text), 'text': "".join(text)}})

    def write_file(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            lengths = [self.files[file]['length'] for file in self.files]
            while len(lengths):
                min_length = min(lengths)
                f.write(f'Файл: {"".join(file for file in self.files if self.files[file]["length"] == min_length)}\n')
                f.write(f'Строк: {min_length}\n')
                f.write("".join(self.files[file]['text'] for file in self.files \
                                if self.files[file]['length'] == min_length))
                lengths.remove(min_length)


generator = FileGenerator()
generator.read_files('1.txt', '2.txt', '3.txt')
generator.write_file('result.txt')