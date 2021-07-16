package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	client := &http.Client{}
	// 提交请求
	request, err := http.NewRequest("POST", "http://sso.qa.huohua.cn/oauth/token?grant_type=password&password=ZdqHuohua007&username=zhengdongqi%40huohua.cn", nil)
	if err != nil {
		fmt.Println("error:", err.Error())
		return
	}
	// 增加header选项
	request.Header.Add("Authorization", "Basic aW06aW0=")

	// 处理返回结果
	response, err := client.Do(request)
	if err != nil {
		fmt.Println(" error:", err.Error())
		return
	}
	defer response.Body.Close()
	bodyResp, _ := ioutil.ReadAll(response.Body)
	// respBody := ioutil.NopCloser(bytes.NewReader(bodyResp))
	fmt.Println(string(bodyResp))

	fmt.Println(string(bodyResp))

	// 判断返回状态
	if response.StatusCode == 200 {
		content := map[string]interface{}{}
		// err = json.NewDecoder(respBody).Decode(&content)
		err = json.Unmarshal(bodyResp, &content)
		// if err != nil {
		// 	body, _ := ioutil.ReadAll(respBody)
		// 	fmt.Println("response.Body1:", string(body))
		// 	return
		// }
		// err = json.NewDecoder(respBody).Decode(&content)
		// if err != nil {
		// 	body, _ := ioutil.ReadAll(respBody)
		// 	fmt.Println("response.Body2:", string(body))
		// 	return
		// }
		token := content["access_token"]
		if token != "" {
			fmt.Println("get token:", token.(string))
			return
		}
	} else {
		// reader, _ := ioutil.ReadAll(respBody)
		fmt.Println("response.Bidy3:", string(bodyResp))
	}
}
