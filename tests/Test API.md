## Test API



### 请求地址

`GET`  `/api/test`



### 请求头

| 参数名  | 必填 | 参考值                           |
| ------- | ---- | -------------------------------- |
|Authorization|True|JWT eyJ0eXAiOiJKV...63XjrurF1bDlv478|

### 请求参数

| 参数名   | 类型   | 必填 | 描述 | 默认值 | 参考值 |
| -------- | ------ | ---- | ---- | ------ | ------ |
|test|String|True|||test|



### 返回正确



状态码 `200`

```json
{"msg": "success"}
```




### 返回错误



状态码 `400`

```json
{"msg": "fail"}
```




