age = int(input('Введите свой возраст:\n'))
# старый способ
# answer = ''
# if age < 18:
#     answer = False
# else:
#     answer = True


# новый способ (тернарный оператор)
answer = True if age >= 18 else False

print(answer)