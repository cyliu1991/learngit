# coding:utf-8
# 发送get或post请求
# 必传参数：method，请求方法，发送get请求时method='GET',发送post请求时，method='POST'
# 必传参数：url,发送请求的url地址（如：url = 'https://test.data4truth.com/api/questionLib/createClassTest'）
# 选传参数：headers，请求头，为dict格式（如：headers = {'user-agent': 'my-app/0.0.1'}）
# 选传参数：data，请求数据，为dict格式（如：data = {"classID": "0101010011701", "className": "201"}）
import requests
import json

class SendRequests:

    def get_request(self, url, headers, data):
        res = requests.get(url, headers=headers, params=data)
        return res

    def post_request(self, url, headers, data):
        res = requests.post(url, headers=headers, json=data)
        return res

    def send_request(self, method, url, headers=None, data=None):
        if method == 'GET':
            res = self.get_request(url, headers, data)
        else:
            res = self.post_request(url, headers, data)
        return res


if __name__ == '__main__':
    send_request = SendRequests()
    request_headers = {
            'token':  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWYiOjE1NTY1MTc1MjYsImV4cCI6MTU1NzAzNTkyNiwidXNlc'
                      'klkIjoiMDEwMTAxMDAxMTYwMzAyNyIsImlhdCI6MTU1NjQzMTEyNn0.rdLwl2pfVrnd4RkDBfsUP_OIoxE-srIs9py33ZsRPeE'
        }
    request_method1 = 'GET'

    request_url1 = "https://test.data4truth.com/parent/weixin/studyAnalysisPage1"
    # request_data1 = {"phoneNumber": "__", "password": "123456", "openId": "__"}
    # print(type(request_data1))
    request_res1 = send_request.send_request(request_method1, request_url1, headers=request_headers)
    print(request_res1.text)

 #   res = json.loads(text)
    #print(type(res))





