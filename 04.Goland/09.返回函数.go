package main

import "fmt"

func main() {
    p2 := plusTwo()
    fmt.Println(p2(2))
}

func plusTwo() func(int) int {
    return func(x int) int { return x + 2 }
}
