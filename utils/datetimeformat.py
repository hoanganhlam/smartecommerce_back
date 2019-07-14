import datetime
import dateutil.parser


def dtmValidate(date_text):
    isValid = True
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        validate = True
    except ValueError:
        validate = False
    finally:
        return isValid


def orderDursationASC(lstDur, format="%Y-%m-%d %H:%M:%S"):
    res = []
    if not isinstance(lstDur, list):
        return res
    else:
        for duration in lstDur:
            start = datetime.datetime.strptime(duration['start'], format).time()
            end = datetime.datetime.strptime(duration['end'], format).time()
            # FIXME: fix now
            # if end < start:
            #     end = end + datetime.timedelta(days=1)
            res.append({
                'start': start,
                'end': end,
            })

        __len = len(res)
        for i in range(__len - 1):
            for j in range(i + 1, __len):
                start_i = res[i]['start']
                start_j = res[j]['start']
                if start_i > start_j:
                    temp = res[i]
                    res[i] = res[j]
                    res[j] = temp
                else:
                    continue

        # Cause for json encode to match
        for duration in res:
            duration['start'] = str(duration['start'])
            duration['end'] = str(duration['end'])

        return res

def date2str(date, format='%Y-%m-%d'):
    try:
        res = date.strftime(format)
        return res
    except:
        return None

def str2DateTime(sTime, sFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(sTime, sFormat)

def changeDateTimeFormat(sTime, sFormat='%Y-%m-%d %H:%M:%S'):
    timeTmp = dateutil.parser.parse(sTime)
    return timeTmp.strftime(sFormat)