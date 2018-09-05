import random

class RandomSampler:
    def __init__(self, urls):
        self.urls = urls
        self.used = []

    def sample_one(self):
        url = random.choice(self.urls)
        self.urls.remove(url)
        self.used.append(url)
        return url
    
    def sample(self, num):
        return [self.sample_one().strip() for _ in range(num)]

if __name__ == "__main__":
    keyword = '_'.join(input().split())
    with open("result_%s.txt" % keyword, "r") as f:
        rs = RandomSampler(f.readlines()[:60])
    while True:
        n = int(input())
        print('\n'.join(rs.sample(n)))
