package main

import "fmt"

func prtthem(numbers ... int) {
    for _, d := range numbers {
        fmt.Println(d)
    }
}

func main() {
    prtthem(1, 4, 5, 7, 4)
    prtthem(1, 2, 4)
}
