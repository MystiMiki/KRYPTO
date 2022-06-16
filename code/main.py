import random

import PyPDF2  # pip install PyPDF2

# počet načítaných stránek
NUM_PAGES = 10
# nepovolené znaky, mazání
DISALLOWED_CHAR = ',.'


# rozdělení slova na jednotlivé znaky
def split(word):
    return [char for char in word]


# načítání pdf knihy, s výběrem šifry
def read_pdf(file, extract):
    with open('C:\\Users\\Mysti\\PycharmProjects\\pythonProject\\venv\\Resources\\' + file + '.pdf', 'rb') as f:
        file_reader = PyPDF2.PdfFileReader(f)
        num_pages = file_reader.numPages
        book = []

        for num in range(8, 8 + NUM_PAGES):
            page = file_reader.getPage(num)
            book.append(page.extractText().split())

    if extract == 1:
        print('THE FIRST LETTER OF THE WORD')
        cipher = first_pdf(book)
    else:
        print('THE COMPLETE WORD')
        cipher = word_pdf(book)

    return cipher


# typy šifry pro pdf:
#   první písmeno slova
def first_pdf(book):
    firsts = []

    for page in book:
        for word in page:
            firsts.append(word[0])

    return firsts


#   celé slovo
def word_pdf(book):
    words = []

    for page in book:
        for word in page:
            words.append(word)

    return words


# načítání txt knihy, s výběrem šifry
def read_txt(file, extract):
    with open('C:\\Users\\Mysti\\PycharmProjects\\pythonProject\\venv\\Resources\\' + file + '.txt', 'r') as f:
        book = f.read()

        if extract == 1:
            print('THE FIRST LETTER OF THE WORD')
            cipher = first_txt(book)
        else:
            print('THE COMPLETE WORD')
            cipher = word_txt(book)

        return cipher


# typy šifry pro pdf:
#   první písmeno slova
def first_txt(book):
    firsts = []

    words = book.split()
    for word in words:
        letters = split(word)
        firsts.append(letters[0])

    return firsts


#   celé slovo
def word_txt(book):
    words = book.split()

    return words


# získání všechn indexů hledaného slova/písmene
def get_index_positions(list_of_elems, element):
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            index_pos = list_of_elems.index(element, index_pos)
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


if __name__ == '__main__':

    # výběr typu načítaného souboru
    print('What type of file is your book?\n Press corresponding number:\n'
          '1 ... pdf\n2 ... txt\n')

    while True:
        try:
            type = int(input())
            if 0 < type < 3:
                break
            else:
                print('That\'s not a corresponding number!')
        except:
            print('That\'s not a valid option!')

    # výběr typu šifry
    print('What extract do you want?\n Press corresponding number:\n'
          '1 ... the first letter of the word\n2 ... the complete word\n')

    while True:
        try:
            extract = int(input())
            if 0 < type < 3:
                break
            else:
                print('That\'s not a corresponding number!')
        except:
            print('That\'s not a valid option!')

    # volba načítání, dle typu souboru
    if type == 1:
        print('PDF')
        key = read_pdf('Bible', extract)

    elif type == 2:
        print('TXT')
        key = read_txt('web', extract)

    # úprava šifry lowercase, mazání nepovolených znaků
    for i in range(len(key)):
        key[i] = key[i].lower()
        for character in DISALLOWED_CHAR:
            key[i] = key[i].replace(character, '')

    # KONTROLA
    # vypsaní do souboru
    with open('cipher.txt', 'w') as f:
        for block in key:
            f.write(block + ' ')

    # načtení textu, co chceme zakódovat
    with open('C:\\Users\\Mysti\\PycharmProjects\\pythonProject\\venv\\Resources\\plain.txt', 'r') as f:
        plain = f.read()

    # rozdělení textu, dle typu šifry
    if extract == 1:
        plain_list = split(plain)
    else:
        plain_list = plain.split()

    # úprava šifrovaného textu lowercase, mazání nepovolených znaků
    for i in range(len(plain_list)):
        plain_list[i] = plain_list[i].lower()
        for character in DISALLOWED_CHAR:
            plain_list[i] = plain_list[i].replace(character, '')

    # získání všech pozic slov/písmen
    encrypt_indexes = []
    for i in range(len(plain_list)):
        encrypt_indexes.append(get_index_positions(key, plain_list[i]))
        if not encrypt_indexes[i]:
            encrypt_indexes[i].append(-1)

    # vybrání náhodné odpovídající pozice slova/písmene, pokud je to možné
    encrypt = []
    for i in range(len(encrypt_indexes)):
        n = random.randint(0, len(encrypt_indexes[i]) - 1)
        encrypt.append(encrypt_indexes[i][n] + 1)

    # zapsání
    with open('encrypt.txt', 'w') as f:
        for block in encrypt:
            f.write(str(block) + ' ')

    # zpětná vazba pro uživatele
    if 0 in encrypt:
        print('Missing letters\n Cannot encrypt!')

    else:
        print('Encryption successful')
        print('For control, is this your plain text?')
        for num in encrypt:
            print(key[num - 1], end =' ')
