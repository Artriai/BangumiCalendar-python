import requests
import util
from iCal import iCal
from reptile import data
import os

'''
step 1 通过用户名获取订阅的番组id
step 2 通过番组id获取章节信息
step 3 将信息进行整合导出到ics
'''

if __name__ == '__main__':

    userid = "746322"
    
    # Load bangumi-data for exact broadcast times
    bgm_time_map = {}
    try:
        headers = {'User-Agent': 'Artriai/BangumiCalendar-python(https://github.com/Artriai/BangumiCalendar-python)'}
        bgm_data = requests.get('https://cdn.jsdelivr.net/npm/bangumi-data/dist/data.json', headers=headers, timeout=15).json()
        for item in bgm_data.get('items', []):
            bgm_id = None
            for site in item.get('sites', []):
                if site.get('site') == 'bangumi':
                    bgm_id = str(site.get('id'))
                    break
            if bgm_id and item.get('begin'):
                bgm_time_map[bgm_id] = item.get('begin')
    except Exception as e:
        print("Failed to load bangumi-data:", e)

    data = data(userid)
    # step 1 通过用户名获取订阅的番组id
    data.getsubjects()
    # step 2 通过番组id获取章节信息
    data.geteps()
    # 将信息进行整合导出到ics
    icl = iCal()
    for key in data.subjects:
        for i in data.epdict[key.id]:
            # 判定日历格式是否正确
            if len(i.airdate) == 10:
                # Use precise broadcast time if available
                subject_id_str = str(key.id)
                if subject_id_str in bgm_time_map:
                    event_time = util.genDateTime(i.airdate, bgm_time_map[subject_id_str])
                else:
                    event_time = util.genDate(i.airdate)

                icl.setEvent(summary=util.genSummary(key.name, key.name_cn, i.ep),
                             time=event_time,
                             uuid=util.genUUID(key.id, i.ep, userid))

    icl.write()

