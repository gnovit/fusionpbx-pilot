
def create_random_domains(num):
    import random
    import string

    country = [".br", "", ".py", ".uy", ".ar"]
    level2 = [".com", ".org", ".net", ".gov", ".edu", ".mil"]
    level3 = list(string.ascii_lowercase)
    for i in range(num):
        domain = f'{"".join(random.sample(level3, 10))}{random.choice(level2)}{random.choice(country)}'
        f.domain = domain
        print(f.domain)
