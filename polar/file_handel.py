import os
import hashlib
import json
import shutil
import base64
from os import walk


def clear_temp():
    for f in os.listdir('./temp/'):
        os.remove(os.path.join('./temp/', f))


def file_handle(files, target_dest):

    file_hash = {}  # save file hash info
    recieved = []  # save recieved files
    file_saved = file_removed = file_recieved = 0  # file counter

    if not os.path.isdir('./archive/%s' % target_dest):
        # new archive
        os.mkdir('./archive/%s' % target_dest)

        for file in files:
            if file.filename == 'file.json':
                continue
            recieved.append(file.filename)
            file_recieved += 1
            file.save('./archive/%s/' % target_dest + file.filename)
            file_saved += 1
            with open('./archive/%s/' % target_dest + file.filename, 'rb')as file_to_hash:
                file_hash[file.filename] = hashlib.md5(
                    file_to_hash.read()).hexdigest()

            print('saving file: %s' % file.filename)

        with open('./archive/%s/' % target_dest + 'file.json', 'w')as json_file:
            json.dump(file_hash, json_file)
            print('creating file hash')

        return (file_saved, file_recieved, file_removed, tuple(recieved))

    with open('./archive/%s/' % target_dest + 'file.json', 'r')as json_file:
        file_hash = json.load(json_file)
        print('loading file hash')

    changed = False

    for file in files:
        if file.filename == 'file.json':
            continue
        file_recieved += 1
        recieved.append(file.filename)

        # saving new file
        if file.filename not in file_hash.keys():
            file.save('./archive/%s/' % target_dest + file.filename)
            file_saved += 1
            with open('./archive/%s/' % target_dest + file.filename, 'rb')as new_file:
                file_hash[file.filename] = hashlib.md5(
                    new_file.read()).hexdigest()
                print('creating new file: %s' % file.filename)
            continue

        # check md5
        file.save('./temp/' + file.filename)
        with open('./temp/' + file.filename, 'rb')as temp_file:
            # if same, pass
            if hashlib.md5(temp_file.read()).hexdigest() == file_hash[file.filename]:
                continue

        with open('./temp/' + file.filename, 'rb')as temp_file:  # update md5
            file_hash[file.filename] = hashlib.md5(
                temp_file.read()).hexdigest()
        file_saved += 1
        os.remove('./archive/%s/' % target_dest + file.filename)
        os.rename('./temp/' + file.filename, './archive/%s/' %
                  target_dest + file.filename)  # replace file
        print('replacing file: %s' % file.filename)
        changed = True

    # remove file here
    remove_list = list(set(recieved) ^ set(file_hash.keys()))
    for x in remove_list:
        file_removed += 1
        # this is wrong, fix itafter come back from lunch -> update:fixed
        file_hash.pop(x)
        os.remove('./archive/%s/' % target_dest + x)

    if changed:  # update hash log
        with open('./archive/%s/' % target_dest+'file.json', 'w')as json_file:
            json.dump(file_hash, json_file)
            print('changing file hash')

    # clear up the temp
    clear_temp()

    return (file_saved, file_recieved, file_removed, tuple(recieved))


def destory_archive(target):
    destory_list = []
    for f in os.listdir('./archive/%s/' % target):
        os.remove(os.path.join('./archive/%s/' % target, f))
        destory_list.append(f)
    shutil.rmtree('./archive/%s' % target)
    return tuple(destory_list)


def fetch_file(target_dir, target_files):
    b64_data = {}
    for file in target_files:
        if file.filename == 'file.json':
            continue
        with open('./archive/%s/%s' % (target_dir, file), 'rb')as temp:
            b64_data[file] = base64.b64encode(temp.read()).decode()
    return b64_data


def add_file(target_dir, target_files):

    file_added = []
    with open('./archive/%s/file.json' % target_dir, 'r')as file_json:
        file_hash = json.load(file_json)

    for file in target_files:
        if file.filename == 'file.json':
            continue

        file.save('./archive/%s/%s' % (target_dir, file.filename))
        file_added.append(file.filename)
        file_hash[file.filename] = hashlib.md5(
            file.read()).hexdigest()

    filenames = next(walk('./archive/%s' % target_dir), (None, None, []))[2]
    for file in filenames:
        if file == 'file.json':
            continue
        with open('./archive/%s/%s' % (target_dir, file), 'rb')as this_file:
            file_hash[file] = hashlib.md5(this_file.read()).hexdigest()
    with open('./archive/%s/file.json' % target_dir, 'w')as file_json:
        json.dump(file_hash, file_json)

    return file_added


def delete_file(target_dir, target_files):
    removed_files = []
    for file in target_files:
        print(file)
        if file == 'file.json':
            continue
        os.remove('./archive/%s/%s' % (target_dir, file))
        removed_files.append(file)

    with open('./archive/%s/file.json' % target_dir, 'r')as file_json:
        file_hash = json.load(file_json)

    file_hash: dict

    for file in removed_files:
        file_hash.pop(file)

    with open('./archive/%s/file.json' % target_dir, 'w')as file_json:
        json.dump(file_hash, file_json)

    return removed_files


def restore_archive(target_dir):
    shutil.make_archive('./temp/archive', 'zip', './archive/%s/' % target_dir)
    with open('./temp/archive.zip', 'rb')as temp_archive:
        b64 = base64.b64encode(temp_archive.read()).decode()
    clear_temp()
    return {target_dir: b64}
