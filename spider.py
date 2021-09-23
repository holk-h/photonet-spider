import threading

import requests
import os
import multiprocessing

save_path = ''
dataset = 'photonet_dataset.txt'
f = open(dataset)


def download_img(img_url, index):
    print(img_url)
    r = requests.get(img_url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        open(save_path + index + '.jpg', 'wb').write(r.content)
        print("done")
    del r


def download(begin_index, end_index):
    for line in f:
        line = line.strip().split(' ')
        image_index = line[0]

        if int(image_index) < begin_index:
            continue
        elif int(image_index) > end_index:
            break

        if os.path.isfile(os.path.join(save_path, image_index + '.jpg')):
            continue

        image_id = line[1]
        download_img(f"https://www.photo.net/{image_id}-photo.jpg", image_index)
        print('image%s success' % image_index)


if __name__ == '__main__':
    record = []
    lock = multiprocessing.Lock()

    index_list = [i for i in range(1, 20278, 1000)]
    index_list.append(20278)

    for i, j in enumerate(index_list):
        if i < len(index_list) - 1:
            print(index_list[i], index_list[i + 1])
            process = multiprocessing.Process(target=download, args=(index_list[i], index_list[i + 1]))
            process.start()
            record.append(process)

    for process in record:
        process.join()
