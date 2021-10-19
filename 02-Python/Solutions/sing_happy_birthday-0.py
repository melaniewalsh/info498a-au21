import sys

def sing_happy_birthday(name='Person'):
    print(f"""
    Happy birthday to you
    Happy birthday dear {name}
    Happy birthday to you""")

user_defined_name = sys.argv[0]

sing_happy_birthday(name=user_defined_name)
