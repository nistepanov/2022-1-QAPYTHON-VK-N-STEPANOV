FROM python:3.8

ADD /requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD / /final_project

WORKDIR /final_project

CMD ["pytest", "-s", "-l", "-v", "-n2", "./code", "--selenoid", "--alluredir", "/tmp/allure"]
