import re


def count_requests(builder, path):
    count = 0
    http_methods = ['"GET ', '"POST ', '"PUT ', '"PATCH ', '"DELETE ', '"COPY ', '"HEAD ', '"OPTIONS ',
                    '"LINK ', '"UNLINK ', '"PURGE ', '"LOCK ', '"UNLINK ', '"PURGE ', '"LOCK ',
                    '"UNLOCK ', '"PROPFIND ', '"VIEW ']
    with open(path) as file:
        for line in file:
            for iter in http_methods:
                if iter in line:
                    count += 1

    builder.create_count_requests(count)

    return count


def count_requests_type(builder, path):
    count_requests_separated_by_type_dict = {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0,
                                             "PATCH": 0, "OPTIONS": 0, "HEAD": 0, "LINK": 0,
                                             "UNLINK": 0, "PURGE": 0, "LOCK": 0, "UNLOCK": 0,
                                             "PROPFIND": 0, "VIEW": 0}
    count_requests_separated_by_type_not_null = {}
    with open(path) as file:
        for line in file:
            for key in count_requests_separated_by_type_dict.keys():
                if '"' + key + " " in line:
                    count_requests_separated_by_type_dict[key] = count_requests_separated_by_type_dict[key] + 1 if \
                        count_requests_separated_by_type_dict.get(key) else 1

        for key, value in count_requests_separated_by_type_dict.items():
            if value:
                builder.create_count_req_type(key, value)
                count_requests_separated_by_type_not_null.update({key: value})

    return count_requests_separated_by_type_not_null


def count_top_resource(builder, path, count):
    urls_by_usage = {}
    delimiters = ["%", "?", "#"]
    with open(path) as file:
        for line in file:
            url = line.split(" ")[6]
            for sep in delimiters:
                if sep in url:
                    url = url.split(sep)[0]

            if url in urls_by_usage.keys():
                urls_by_usage[url] += 1
            else:
                urls_by_usage[url] = 1

    list_requests = list(urls_by_usage.items())
    list_requests.sort(key=lambda url: url[1], reverse=True)

    top_requests_by_usage = list_requests[0:count]

    for line in top_requests_by_usage:
        builder.create_count_top_res(line[0], line[1])

    return top_requests_by_usage


def top_biggest_requests_ended_client_error(builder, path, count):
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

    top_biggest_requests = list_requests[0:count]

    for line in top_biggest_requests:
        path = line[0].split(' ')[0]
        code = line[0].split(' ')[1]
        ip = line[0].split(' ')[2]
        size = line[1]
        builder.create_count_req_client_error(path=path, code=code, ip=ip, size=size)

    return top_biggest_requests


def top_requests_ended_server_error(builder, path, count):
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

        top_users_by_count_of_requests_ended_server_error = list_requests[0:count]

        for line in top_users_by_count_of_requests_ended_server_error:
            ip = line[0]
            count = line[1]
            builder.create_count_req_server_error(ip=ip, frequency=count)

        return top_users_by_count_of_requests_ended_server_error
