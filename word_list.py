from faker import Faker

fake = Faker()

def words(): 
    for _ in range(5):
        word = fake.words()
    return word
# print(words())
    
