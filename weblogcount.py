from operator import itemgetter

logs = ["[01/Aug/1995:00:54:59 -0400] ""GET /images/opf-logo.gif HTTP/1.0"" 200 32511",
"[01/Aug/1995:00:55:04 -0400] ""GET /images/ksclogosmall.gif HTTP/1.0"" 200 3635",
"[01/Aug/1995:00:55:06 -0400] ""GET /images/ksclogosmall.gif HTTP/1.0"" 403 298",
"[01/Aug/1995:00:55:09 -0400] ""GET /images/ksclogosmall.gif HTTP/1.0"" 200 3635",
"[01/Aug/1995:00:55:18 -0400] ""GET /images/opf-logo.gif HTTP/1.0"" 200 32511",
"[01/Aug/1995:00:56:52 -0400] ""GET /images/ksclogosmall.gif HTTP/1.0"" 200 3635"]

entries = {}

#class to turn web log entries into objects
class LogRequest:

    def __init__(self, query_path, bytes):
        self.query_path = query_path
        self.bytes = bytes

#pull out the important data from each entry in the web log
def parse_log(request):
    parsed = request.split(" ")
    return parsed[3], parsed[5], parsed[6]

#create a dict that keeps count of the amount of times and bytes each query_path is asked for
for request in logs:
    request_data = parse_log(request)
    if request_data[1] == "200":
        log = LogRequest(request_data[0], request_data[2])
        if log.query_path in entries.keys():
            count = entries[log.query_path][0]
            bytes = int(entries[log.query_path][1])
            entries[log.query_path] = (count + 1, bytes + int(log.bytes))
        else:
            entries[log.query_path] = (1, log.bytes)

#find and return the 10 most queried paths and amount of bytes requested
top_ten = sorted(entries.items(), key=itemgetter(1), reverse=True)[:10]
for request in top_ten:
  print request[0], request[1][1]
