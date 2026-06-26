from datetime import datetime, date, timezone, timedelta


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
    begin_jst = begin_utc.astimezone(timezone(timedelta(hours=9)))
    jst_hour = begin_jst.hour
    jst_minute = begin_jst.minute
    air_date = datetime.strptime(airdate_str, "%Y-%m-%d")
    ep_jst = datetime(air_date.year, air_date.month, air_date.day, jst_hour, jst_minute, tzinfo=timezone(timedelta(hours=9)))
    return ep_jst.astimezone(timezone.utc)
