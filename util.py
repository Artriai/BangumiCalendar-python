from datetime import datetime, date, timezone, timedelta
from zoneinfo import ZoneInfo


def genUUID(projectId, epsId, userid) -> str:
    return str(projectId) + "-" +str(epsId) + "-" + str(userid)


def genSummary(name, name_cn, ep) -> str:
    if name_cn != "":
        return name_cn + " " + str(ep)
    else:
        return name + " " + str(ep)


def genDec(summary, epname) -> str:
    str(epname).replace("/n","\n")
    return "「"+epname+"」" + "\n" + "\n"+ "\n"+ summary


def genDate(time) -> date:
    format = "%Y-%m-%d"
    date = datetime.strptime(time, format)
    return date.date()


def genDateTime(airdate_str, begin_iso_str) -> datetime:
    iso_str = begin_iso_str.replace('Z', '+00:00')
    begin_utc = datetime.fromisoformat(iso_str)
    jst_tz = timezone(timedelta(hours=9))
    begin_jst = begin_utc.astimezone(jst_tz)
    
    # Calculate day offset between the JST actual date and the database programming date
    begin_prog_date_str = begin_iso_str[:10]
    begin_prog_date = datetime.strptime(begin_prog_date_str, "%Y-%m-%d").date()
    day_offset = begin_jst.date() - begin_prog_date
    
    # Apply offset to the episode airdate
    air_date = datetime.strptime(airdate_str, "%Y-%m-%d")
    ep_air_date_adjusted = air_date + day_offset
    
    ep_jst = datetime(
        ep_air_date_adjusted.year,
        ep_air_date_adjusted.month,
        ep_air_date_adjusted.day,
        begin_jst.hour,
        begin_jst.minute,
        tzinfo=jst_tz
    )
    return ep_jst.astimezone(ZoneInfo('Asia/Shanghai'))


