package main

import "fmt"

func Map(f func(int) int, l []int) []int {
    j := make([]int, len(l))
    for  k, v := range l {
        j[k] = f(v)
    }
    return j
}

func main() {
    m := []int{1, 3, 4}
    f := func(i int) int {
        return i * i
    }
    fmt.Println(Map(f, m))
}
