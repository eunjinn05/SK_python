
# greeting 관련 모듈
__version__ = 1.0
def print_greeting(name) :
    print(f"{name}님, 안녕하세요")

def print_welcome(name) :
    print(f"{name}님, 환영합니다")

def get_greeting(name) :
    print(f"{name}님 안녕하세요")

class Hello :
    def __init__(self, name) :
        self.name = name

    def kor_greet(self) :
        return f"{self.name}님 안녕하세요"

    def eng_greet(self) :
        return f"Hello! {self.name}"

h = Hello('은딘')
h.kor_greet()


print(__name__) # main / sub 환경 확인

if (__name__ == "__main__") :
    g = get_greeting('링')
    print_welcome('링링')


