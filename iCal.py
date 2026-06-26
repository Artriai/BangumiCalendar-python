from datetime import datetime, date, timedelta

from icalendar import Calendar, Event


class iCal:
    def __init__(self):
        g = open("template.ics", "rb")
        self.cal = Calendar.from_ical(g.read())

    def display(self):
        print(self.cal.to_ical().decode("utf-8").replace('\r\n', '\n').strip())
        return self

    def setEvent(self, summary, time, uuid):
        event = Event()
        event.add('dtstamp', datetime.today().date(), parameters={'VALUE': 'DATE'})
        event.add('uid', uuid)
        if isinstance(time, datetime):
            event.add('dtstart', time)
            event.add('dtend', time + timedelta(minutes=30))
        else:
            event.add('dtstart', time, parameters={'VALUE': 'DATE'})
        event.add('class', 'PUBLIC')
        event.add('summary', summary)
        event.add("TRANSP", "TRANSPARENT")
        event.add("X-APPLE-UNIVERSAL-ID", "42902458-1dd4-5105-04d0-2dccc0194c5f")
        self.cal.add_component(event)
        return self

    def write(self):
        f = open("target.ics", "wb")
        f.write(self.cal.to_ical())
        f.close()
        return self


if __name__ == '__main__':
    iCal().display().write()
