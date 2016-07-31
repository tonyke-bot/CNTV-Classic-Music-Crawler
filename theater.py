# coding:utf-8
import requests
import re
import json
import os.path
import os
import sys
import pickle


def get_ids(url):
    result = requests.get(url)

    if result:
        html = result.content.decode('utf-8')
        title = ''
        id_list = []

        match = re.search(r'var ids = \[([\s\S]*?)\]', html)
        if match:
            id_list = [{'id': id.strip('\t\r\n"')}
                       for id in match.group(1).split(',')]

        match = re.search(r'<div class="name">\s*?<h1>([\s\S]*?)</h1>', html)
        if match:
            title = match.group(1)

        return title, id_list

    return None, []


def get_audio_info(audio_id):
    url = 'http://vdn.apps.cntv.cn/api/getIpadVideoInfo.do?pid=' + audio_id
    result = requests.get(url)
    if result:
        match = re.search(r'var html5VideoData\s*=\s*\'([\s\S]*)\';',
                          result.content)
        if match:
            info = json.loads(match.group(1).decode(result.encoding))

            rv = {
                'title': info.get('title', ''),
                'url': info.get('video', {}).get('chapters', [{}])[0].get('url')
            }

            return rv


def download_audios(url, directory='.'):
    album_title, id_list = get_ids(url)
    if album_title is None:
        print u'无法获取到该专辑的信息'
        exit(0)
    print u'专辑：%s(%d)' % (album_title, len(id_list))

    base_dir = os.path.join(directory, album_title)
    pickle_path = os.path.join(base_dir, 'pickle.dat')
    try:
        album_title, id_list = pickle.load(open(pickle_path, 'rb'))
    except:
        pass

    try:
        os.mkdir(base_dir)
    except OSError:
        pass

    for info in id_list:
        if info.get('title') is None:
            info.update(get_audio_info(info.get('id')))

        if info.get('complete'):
            print u'　【已完成】' + info['title']
            continue
        else:
            print u'　正在下载：' + info['title'],
        save_path = os.path.join(base_dir, info['title'] + '.mp3')

        failed_times = 3
        while failed_times > 0:
            try:
                audio_data = requests.get(info['url'], headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
                    'X-Requested-With': 'ShockwaveFlash/21.0.0.242',
                    'Connection': 'keep-alive',
                    'Referer': url
                }).content
                with open(save_path, 'wb') as f:
                    f.write(audio_data)
                info['complete'] = True
                print u'【成功】'
                break
            except:
                failed_times -= 1
        if failed_times == 0:
            print u'【失败】'

        pickle.dump((album_title, id_list), open(pickle_path, 'wb'))


if __name__ == '__main__':
    download_audios(sys.argv[1])
