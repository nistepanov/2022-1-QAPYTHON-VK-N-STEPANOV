import sys
import json

from base_parser import BaseParser

parser = BaseParser('access.log')

if sys.argv[1] == '--json':
    data_json = {}
    total_requests = parser.count_total_number_of_requests()

    data_json["Total requests"] = (str(total_requests))

    requests_separated_by_type = parser.count_total_requests_separate_by_type()

    data_json["Total requests by type"] = []
    for key in requests_separated_by_type:
        data_json["Total requests by type"].append(({"Method": key, "Count": requests_separated_by_type[
            key]}))

    top_requests_by_usage = parser.top_ten_requests_by_usage()

    data_json["Top 10 requests by usage"] = []
    for url in top_requests_by_usage:
        data_json['Top 10 requests by usage'].append(({"Count of usages": url[1], "request": url[0]}))

    top_biggest_requests_ended_client_error = parser.top_five_biggest_requests_ended_client_error()

    data_json['Top 5 requests by response size ended with 4** error'] = []
    for url in top_biggest_requests_ended_client_error:
        data_json['Top 5 requests by response size ended with 4** error'].append(({"Request url": url[0],
                                                                                   "Response size": url[1]}))

    data_json['Top 5 users by count of requests ended with 5** error'] = []
    top_users_by_count_of_requests_ended_server_error = parser.top_five_users_by_count_of_requests_ended_server_error()
    for url in top_users_by_count_of_requests_ended_server_error:
        data_json['Top 5 users by count of requests ended with 5** error'].append(({"Count usages": url[1],
                                                                                    "User IP": url[0]}))

    with open('result_python_parsing.json', 'w') as outfile:
        json.dump(data_json, outfile)

else:
    result_python_parsing = open("result_python_parsing.txt", 'w')

    total_requests = parser.count_total_number_of_requests()

    result_python_parsing.write("Total requests:\n")
    result_python_parsing.write(str(total_requests))
    result_python_parsing.write("\n")

    requests_separated_by_type = parser.count_total_requests_separate_by_type()

    result_python_parsing.write("\nTotal requests by type:\n")
    for key in requests_separated_by_type:
        print(key, "-", requests_separated_by_type[key], file=result_python_parsing)
    result_python_parsing.write("\n")

    result_python_parsing.write("\nTop 10 requests by usage:\n")
    top_requests_by_usage = parser.top_ten_requests_by_usage()
    for url in top_requests_by_usage:
        print(url[1], " ", url[0], file=result_python_parsing)
    result_python_parsing.write("\n")

    result_python_parsing.write("\nTop 5 requests by response size ended with 4** error:\n")
    top_biggest_requests_ended_client_error = parser.top_five_biggest_requests_ended_client_error()
    for url in top_biggest_requests_ended_client_error:
        print(url[0], " ", url[1], file=result_python_parsing)
    result_python_parsing.write("\n")

    result_python_parsing.write("\nTop 5 users by count of requests ended with 5** error:\n")
    top_users_by_count_of_requests_ended_server_error = parser.top_five_users_by_count_of_requests_ended_server_error()
    for url in top_users_by_count_of_requests_ended_server_error:
        print(url[1], " ", url[0], file=result_python_parsing)
    result_python_parsing.write("\n")

    result_python_parsing.close()
