import requests


class ExternalResourceGetter:

    def __init__(self, url):
        self.url = url
        self.data = None

    def run(self):
        self.data = self.get_data()
        result = self.process_data()
        return result

    def get_data(self):
        response = requests.get(self.url)
        return response.text

    def process_data(self):
        max_length = 0
        for line in self.data.split('\n'):
            if len(line) > max_length:
                max_length = len(line)
        return max_length


if __name__ == '__main__':
    getter = ExternalResourceGetter(url='https://www.jetbrains.com/pycharm/')
    data = getter.run()
    print(data)