
from re import L


def get_image(url):

    import requests
    from PIL import Image

    return requests.get(url, allow_redirects=True)
    # open(path, 'wb').write(r.content)


def test():

    import pandas as pd
    from time import sleep
    import os

    data = pd.read_excel('wb_foto_knives.xlsx', engine="openpyxl")
    os.mkdir('input')

    for _, row in data.iterrows():

        art_wb = str(row['Артикул WB']).replace('/', '_')
        nomen = str(row['Номенклатура WB'])
        barcode = str(row['ШК'])

        for i in range(1, 10):
            for j in range(1, 11):
                url = f'https://basket-0{i}.wb.ru/vol{nomen[:-5]}/part{nomen[:-3]}/{nomen}/images/big/{j}.jpg'
                r = get_image(url)

                if r.status_code == 200:
                    open(os.path.join('input', f'{barcode}_{j}.jpg'), 'wb').write(
                        r.content)
                    print(r.status_code, url)
                else:
                    break


def create_wb_folder():
    import pandas as pd
    from time import sleep
    import os
    import shutil

    data = pd.read_excel('wb_foto_knives.xlsx', engine="openpyxl")
    os.mkdir('output_2')

    for _, row in data.iterrows():

        art_wb = str(row['Артикул WB']).replace('/', '_')
        art = str(row['Артикул']).replace('/', '_')
        nomen = str(row['Номенклатура WB'])
        barcode = str(row['ШК'])
        target_path = os.path.join('output_2', art)

        src_path = [{"path": os.path.join('output', f'{barcode}_1.jpg'),
                     "file": f'{barcode}_1.jpg'
                     }]

        for file in os.listdir('orig'):
            if file.startswith(f'{barcode}') & (file != f'{barcode}_1.jpg'):
                src_path.append(
                    {"path": os.path.join('orig', file), "file": file})
        try:
            os.mkdir(target_path)
            for file in src_path:
                shutil.copyfile(file.get("path"), os.path.join(target_path, file.get("file")))
        except:
            continue

        print(src_path)


def ozon_folder():
    import pandas as pd
    from time import sleep
    import os
    import shutil

    data = pd.read_excel('wb_foto_knives.xlsx', engine="openpyxl")
    os.mkdir('ozon_orig')
    os.mkdir('ozon_output')

    for _, row in data.iterrows():

        art = str(row['Артикул']).replace('/', '_')
        barcode = str(row['ШК'])

        for file in os.listdir('ozon_orig_raw'):
            if file.startswith(f'{barcode}'):
                shutil.copyfile(os.path.join('ozon_orig_raw', file), 
                                os.path.join('ozon_orig', file.replace(f'{barcode}', art)))

        for file in os.listdir('ozon_output_raw'):
            if file.startswith(f'{barcode}'):
                shutil.copyfile(os.path.join('ozon_output_raw', file), 
                                os.path.join('ozon_output', file.replace(f'{barcode}', art)))

def wb_folder():
    import pandas as pd
    from time import sleep
    import os
    import shutil

    data = pd.read_excel('wb_foto_knives.xlsx', engine="openpyxl")
    os.mkdir(os.path.join('wb', 'wb_orig_1'))

    for _, row in data.iterrows():

        art_wb = str(row['Артикул WB']).replace('/', '_')
        barcode = str(row['ШК'])
        os.mkdir(os.path.join('wb', 'wb_orig_1', art_wb))

        for file in os.listdir('ozon_orig_raw'):
            if file.startswith(f'{barcode}'):
                shutil.copyfile(os.path.join('ozon_orig_raw', file), 
                                os.path.join('wb', 'wb_orig_1', art_wb, file.replace(f'{barcode}_', '')))

def rename_wb_output():
    import os

    for folder in os.listdir('wb_output_1'):
        for file in os.listdir(os.path.join('wb_output_1', folder)):
            os.rename(os.path.join('wb_output_1', folder, file), os.path.join('wb_output_1', folder, file.replace('.png', '.jpg')))

    for folder in os.listdir('wb_output_2'):
        for file in os.listdir(os.path.join('wb_output_2', folder)):
            os.rename(os.path.join('wb_output_2', folder, file), os.path.join('wb_output_2', folder, file.replace('.png', '.jpg')))




rename_wb_output() 
