import random

print("""Please provide AI some data to learn...
The current data length is 0, 100 symbols left""")
print('Print a random string containing 0 or 1:\n')

list_of_symbols = []

while len(list_of_symbols) < 100:
    user_input = input()
    for x in user_input:
        if x == '0' or x == '1':
            list_of_symbols.append(x)
        else:
            pass
    if len(list_of_symbols) < 100:
        print(f'Current data length is {str(len(list_of_symbols))}, {str(100 - len(list_of_symbols))} symbols left')
        print('Print a random string containing 0 or 1:\n')

final_string = ''.join(list_of_symbols)
print(final_string)

list_of_triads = []

for i in range(len(final_string) - 2):
    triad = final_string[i:i + 3]
    list_of_triads.append(triad)
print('\nFinal data string:')
print(f"{final_string}\n")
print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!\n""")
print('Print a random string containing 0 or 1:')
final_string = ''.join(list_of_symbols)
ist_of_triads = list(set(list_of_triads))
dec_list_of_triads = []
for x in list_of_triads:
    dec_of_number = int(x[0]) * 4 + int(x[1]) * 2 + int(x[2]) * 1
    dec_list_of_triads.append(dec_of_number)

reordered_list_of_triads = [None] * len(list_of_triads)

for i in range(len(list_of_triads)):
    reordered_list_of_triads[dec_list_of_triads[i]] = list_of_triads[i]

counts_0 = {}
counts_1 = {}

for i in range(len(final_string) - 3):
    triada = final_string[i:i + 3]
    if final_string[i + 3] == '1':
        if triada not in counts_1:
            counts_1[triada] = 0
        counts_1[triada] = counts_1[triada] + 1
    if final_string[i + 3] == '0':
        if triada not in counts_0:
            counts_0[triada] = 0
        counts_0[triada] = counts_0[triada] + 1

for triad in reordered_list_of_triads:
    count_0 = counts_0[triad] if triad in counts_0 else 0
    count_1 = counts_1[triad] if triad in counts_1 else 0

list_of_a_new_string = []
new_list_of_triads = []

new_string_input = input()
balance = 1000


while True:
    if all(c not in '01' for c in new_string_input) or len(new_string_input) < 4:
        if new_string_input == 'enough':
            print('Game over!')
            break
        else:
            print('Print a random string containing 0 or 1:\n')
            new_string_input = input()
            continue
    triad_counts = {}
    for i in range(len(final_string) - 3):
        triad = final_string[i:i + 3]
        what_letter = final_string[i + 3]

        if triad not in triad_counts:
            triad_counts[triad] = {'0': 0, '1': 0}

        triad_counts[triad][what_letter] += 1

    prediction_string = ''

    for i in range(len(new_string_input) - 3):
        triad = new_string_input[i:i + 3]
        if triad_counts[triad]['0'] > triad_counts[triad]['1']:
            prediction_string += '0'
        elif triad_counts[triad]['0'] < triad_counts[triad]['1']:
            prediction_string += '1'
        else:
            prediction_string += str(random.choice([0, 1]))

    print('predictions:')
    print(prediction_string)

    guessed_symbols = 0
    for a, b in zip(new_string_input[3:], prediction_string):
        if a == b:
            guessed_symbols += 1
        else:
            pass

    total = len(new_string_input) - 3
    not_guessed = total - guessed_symbols
    print(
        f'Computer guessed {guessed_symbols} out of {total} symbols right ({round(((guessed_symbols / total) * 100), 2)} %)')
    if guessed_symbols > (not_guessed):
        balance -= guessed_symbols - not_guessed

    else:
        print(balance, guessed_symbols, not_guessed)

        balance += not_guessed - guessed_symbols

    print(f'Your balance is now ${balance}\n')

    print('Print a random string containing 0 or 1:\n')
    new_string_input = input()
    continue
