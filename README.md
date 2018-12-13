# Rimuru

📖用单元测试自动生成接口文档

## 已适配的客户端

- [x] requests   
- [ ] django.test.client  
- [ ] flask.testing.FlaskClient

## 使用方法

### 用requests模块进行测试

```python
import unittest
import requests as requests_module
from rimuru.core import doc_client, APIDocument

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.api_document = APIDocument()
		self.client = doc_client(self.api_document, requests_module)
       
    def test_api(self):
        url = 'http://127.0.0.1:5000/api/books'
        method = 'GET'
        name = '书籍列表接口'
        
        self.api_document.set_api_name(method=method, url=url, name=name)
        response = self.client.get(url)
        """
        你的测试逻辑
	    self.assertEqual(response.status_code, 200)
	    	...
        """
        self.client.get(url, params={'name': 'A'}, requires={'name': False}, add_response=False)
        
        url = 'http://127.0.0.1:5000/api/books/<int:id>'
        method = 'GET'
        name = '书详情接口'
        self.api_document.set_api_name(method=method, url=url, name=name)
        self.client.get('http://127.0.0.1:5000/api/books/2')
        response = self.client.get('http://127.0.0.1:5000/api/books/4')
        self.assertEqual(response.status_code, 404)
		
        self.api_document.save(file_path='/documents')
```

### 生成文档

`书籍列表接口.md`

~~~markdown
## 书籍列表接口

### 请求地址

`GET`  `http://127.0.0.1:5000/api/books`

### 请求参数

| 参数名   | 类型   | 必填 | 描述 | 默认值 | 参考值 |
| -------- | ------ | ---- | ---- | ------ | ------ |
|name|String|None|||A|

### 返回正确

状态码 `200`

```json
[
    {
        "id": 1,
        "name": "A"
    },
    {
        "id": 2,
        "name": "B"
    },
    {
        "id": 3,
        "name": "C"
    }
]
```

状态码 `200`

```json
[
    {
        "id": 1,
        "name": "A"
    }
]
```
~~~

`书详情接口.md`

~~~markdown
## 书详情接口

### 请求地址

`GET`  `http://127.0.0.1:5000/api/books/<int:id>`

### 返回正确

状态码 `200`

```json
{
    "id": 2,
    "name": "B"
}
```

### 返回错误

状态码 `404`

```json
{
    "msg": "Not Found"
}
```


~~~

