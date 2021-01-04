/*
1.创建一个基于for的简单的循环。使其循环10次，并且使用fmt包打印出计数器的值
2.用goto改写1的循环。关键字for不可使用
3.再次改写这个循环，使其遍历一个array，并将这个array打印到屏幕上。
*/

package main

import "fmt"

func main() {
    for i := 0; i < 10; i++ {
        fmt.Println(i)
    }
}



