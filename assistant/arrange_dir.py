from os import listdir, rename, rmdir
from pathlib import Path
import shutil
from prettytable import PrettyTable


PATH = '/Users/mykhailo/studies/go_it/my_little_assistant/arrange_dir/'
list_type_r = set()
list_type_files = dict(zip(['images', 'video', 'archives', 'documents', 'audio', 'others_file'],
                           [set(), set(), set(), set(), set(), set(), set()]))
dict_arrange = dict(zip(['images', 'video', 'archives', 'documents', 'audio', 'others_file'],
                            [('JPEG', 'PNG', 'JPG', 'SVG'),
                             ('AVI', 'MP4', 'MOV', 'MKV'),
                             ('ZIP', 'GZ', 'TAR'),
                             ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                             ('MP3', 'OGG', 'WAV', 'AMR'),
                             set()
                             ]))
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k",
               "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts",
               "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i",
               "ji", "g")
all_known_type = ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                 'ZIP', 'GZ', 'TAR', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX',
                 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR']
all_unknown_type = set()
duplicates = set()
report = PrettyTable()
report.field_names = ['path_before', 'path_after', 'name_after']


def arrange_dir(dir):
    PATH = dir
    check_name(dir)
    main(dir, PATH)
    print_report()


def main(dir, PATH):
    p = Path(dir)
    check_name(p)
    val = listdir(p)
    for i in dict_arrange:
        try:
            (p / i).mkdir()
        except FileExistsError:
            pass
    for file_name in val:
        q = p / file_name
        if q.is_dir():
            main(q, PATH)
        else:
            list_type_r.add(file_name.split('.')[-1])
            for dir_in, type_f in dict_arrange.items():
                if (file_type := file_name.split('.')[-1].upper()) not in all_known_type: # додаємо розширення до списку відомих розширень
                    all_unknown_type.add(file_name.split('.')[-1])
                if file_type not in all_known_type and file_name not in duplicates:
                    try:
                        move_file(dir, file_name, PATH, 'others_file')
                    except shutil.Error:
                        pass
                    continue
                if file_type in dict_arrange['archives']:
                    unzip(q, PATH + '/' + 'archives' + '/' + file_name.split('.')[0])
                    ad_list_type_files('archives', file_name)
                    add_to_report(dir, str(PATH) + 'archives', file_name)
                    break
                elif file_type in type_f:
                    try:
                        move_file(dir, file_name, PATH, dir_in)
                    except shutil.Error:
                        pass
    del_empy_dir(dir)


def move_file(dir, file_name, PATH, dir_in):
    shutil.move(str(dir) + '/' + file_name,
                str(PATH) + dir_in)
    ad_list_type_files(dir_in, file_name)
    add_to_report(dir, str(PATH) + dir_in + '/', file_name)


def ad_list_type_files(dir_in, file_name):
    list_type_files[dir_in].add(str(file_name))  # додаємо до списку файлів поточний файл


def unzip(file, dir):
    shutil.unpack_archive(file, dir)
    file.unlink()

def translate(name):
    trans = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()
    return name.translate(trans)


def normalize(file_name: str):
    res = ''
    for i in file_name:
        if 96 < ord(i) < 123 or 64 < ord(i) < 91 or i.isdigit() or i == '.':
            res += i
        elif 1039 < ord(i) < 1111:
            res += translate(i)
        else:
            res += '_'
    return res


def check_name(dir):
    val = listdir(dir)
    for i in val:
        j = normalize(i)
        if j != i:
            rename(dir + '/' + i, dir + '/' + j)
    for k in val:
        l = Path(dir)
        p = l / k
        if p.is_dir():
            val2 = listdir(p)
            for i in val2:
                j = normalize(i)
                if j != i:
                    rename(p / i, p / j)


def del_empy_dir(dir):
    val = listdir(dir)
    p = Path(dir)
    for i in val:
        if (p / i).is_dir():
            try:
                rmdir(p / i)
            except OSError:
                pass


def normalise_path(path_1, path_2):
    path_1 = str(path_1).split('/')
    path_2 = str(path_2).split('/')
    for i, j in enumerate(path_1):
        if j != path_2[i]:
            path_1 = '/'.join(path_1[i - 1:])
            path_2 = '/'.join(path_2[i - 1:])
            break
    return path_1, path_2


def add_to_report(path_before, path_after, name_after):
    path_before, path_after = normalise_path(path_before, path_after)
    report.add_row(['..' + path_before, '..' + path_after, name_after])


def print_report():
    print(report)
    string_return = ''
    string_return += f'\nA list of all known script extensions,' \
                     f' which are found in the target folder: \n{list_type_r}\n'
    string_return += f'\nA list of all extensions unknown to the script:' \
                     f'\n{all_unknown_type}'
    print(string_return)


if __name__ == '__main__':
    arrange_dir(PATH)

