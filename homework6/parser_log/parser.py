import re


def count_requests(builder, path):
    count = 0
    with open(path) as file:
        for line in file:
            if ('"GET ' in line) or ('"POST ' in line) or ('"PUT ' in line) \
                    or ('"PATCH ' in line) or ('"DELETE ' in line) or ('"COPY ' in line) \
                    or ('"HEAD ' in line) or ('"OPTIONS ' in line) or ('"LINK ' in line) \
                    or ('"UNLINK ' in line) or ('"PURGE ' in line) or ('"LOCK ' in line) \
                    or ('"UNLOCK ' in line) or ('"PROPFIND ' in line) or ('"VIEW ' in line):
                count += 1

    builder.create_count_requests(count)


def count_requests_type(builder, path):
    with open(path) as file:
        count = {}
        for line in file:
            if '"GET ' in line:
                count['GET'] = count['GET'] + 1 if count.get('GET') else 1
            elif '"POST ' in line:
                count['POST'] = count['POST'] + 1 if count.get('POST') else 1
            elif '"PUT ' in line:
                count['PUT'] = count['PUT'] + 1 if count.get('PUT') else 1
            elif '"PATCH ' in line:
                count['PATCH'] = count['PATCH'] + 1 if count.get('PATCH') else 1
            elif '"DELETE ' in line:
                count['DELETE'] = count['DELETE'] + 1 if count.get('DELETE') else 1
            elif '"COPY ' in line:
                count['COPY'] = count['COPY'] + 1 if count.get('COPY') else 1
            elif '"HEAD ' in line:
                count['HEAD'] = count['HEAD'] + 1 if count.get('HEAD') else 1
            elif '"OPTIONS ' in line:
                count['OPTIONS'] = count['OPTIONS'] + 1 if count.get('OPTIONS') else 1
            elif '"LINK ' in line:
                count['LINK'] = count['LINK'] + 1 if count.get('LINK') else 1
            elif '"UNLINK ' in line:
                count['UNLINK'] = count['UNLINK'] + 1 if count.get('UNLINK') else 1
            elif '"PURGE ' in line:
                count['PURGE'] = count['PURGE'] + 1 if count.get('PURGE') else 1
            elif '"LOCK ' in line:
                count['LOCK'] = count['LOCK'] + 1 if count.get('LOCK') else 1
            elif '"UNLOCK ' in line:
                count['UNLOCK'] = count['UNLOCK'] + 1 if count.get('UNLOCK') else 1
            elif '"PROPFIND ' in line:
                count['PROPFIND'] = count['PROPFIND'] + 1 if count.get('PROPFIND') else 1
            elif '"VIEW ' in line:
                count['VIEW'] = count['VIEW'] + 1 if count.get('VIEW') else 1

        for key, value in count.items():
            builder.create_count_req_type(key, value)


def count_top_resource(builder, path):
    urls_by_usage = {}
    with open(path) as file:
        for line in file:
            url = line.split(" ")[6]
            if url in urls_by_usage.keys():
                urls_by_usage[url] += 1
            else:
                urls_by_usage[url] = 1

    list_requests = list(urls_by_usage.items())
    list_requests.sort(key=lambda url: url[1], reverse=True)

    top_ten_requests_by_usage = list_requests[0:10]

    for line in top_ten_requests_by_usage:
        builder.create_count_top_res(line[0], line[1])


def top_five_biggest_requests_ended_client_error(builder, path):
    endpoints = {}
    with open(path) as file:
        for line in file:
            code = line.split(" ")[8]
            if re.match("4\d\d", code):
                url = line.split(" ")[6]
                response_size = line.split(" ")[9]
                ip_address = line.split(" ")[0]
                key = url + " " + code + " " + ip_address
                if (key in endpoints.keys()) and (int(response_size) > int(endpoints[key])):
                    endpoints[key] = int(response_size)
                elif key not in endpoints.keys():
                    endpoints[key] = int(response_size)

    list_requests = list(endpoints.items())
    list_requests.sort(key=lambda url: url[1], reverse=True)

    top_biggest_requests_ended_client_error = list_requests[0:5]

    for line in top_biggest_requests_ended_client_error:
       path = line[0].split(' ')[0]
       code = line[0].split(' ')[1]
       ip = line[0].split(' ')[2]
       size = line[1]
       builder.create_count_req_client_error(path=path, code=code, ip=ip, size=size)


def top_five_requests_ended_server_error(builder, path):
    with open(path) as file:
        urls_by_usage = {}
        for line in file:
            code = line.split(" ")[8]
            if re.match("5\d\d", code):
                ip_address = line.split(" ")[0]
                if ip_address in urls_by_usage.keys():
                    urls_by_usage[ip_address] += 1
                else:
                    urls_by_usage[ip_address] = 1

        list_requests = list(urls_by_usage.items())
        list_requests.sort(key=lambda url: url[1], reverse=True)

        top_users_by_count_of_requests_ended_server_error = list_requests[0:5]

        for line in top_users_by_count_of_requests_ended_server_error:
            ip = line[0]
            count = line[1]
            builder.create_count_req_server_error(ip=ip, frequency=count)
