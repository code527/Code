package main

import (
	"fmt"
	"strings"
)

func main() {
	str := "zhengdongqi;lanhuayi;haorongyue;"
	tmp := strings.Split(str, ";")
	to := make([]string, 0, 10)
	for _, tmpTo := range tmp {
		if len(tmpTo) == 0 {
			continue
		}
		to = append(to, tmpTo)
	}

	fmt.Println(to)
	fmt.Println((len(to)))
}
