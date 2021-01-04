package main

import "fmt"

func main() {
    str := "A"
    for i := 0; i < 100; i++ {
        fmt.Println(str)
        str = str + "A"
    }
}
