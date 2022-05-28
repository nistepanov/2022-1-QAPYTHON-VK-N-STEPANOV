FROM python:3.9
ADD /requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt

ADD vk_api_mock.py  /
ENV VK_URL=0.0.0.0:8787
CMD [ "python3", "./vk_api_mock.py" ]

