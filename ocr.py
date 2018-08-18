from aip import AipOcr



def get_file_content(filePath):
    with open(filePath, 'rb') as f:
        return f.read()




def trans_from_img(filePath):
    """ 你的 APPID AK SK """
    APP_ID = '10812973'
    API_KEY = 'lIWFVf7R7qgsi2mnUBmUf7jU'
    SECRET_KEY = 'tzTii0BYQIyereSVSXL5ESqZltCl3lXd'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    
    image = get_file_content(filePath)

    result = client.basicGeneral(image)
    text_line = result['words_result']
    res = ''
    for line in text_line:
        res += (line['words'])# + '\n')
    return res
