package main

import "fmt"

func max(l []int) (max int) {
    max = l[0]
    for _, v := range l{
        if v > max {
            max = v
        }
    }
    return 
}

func min(l []int) (min int) {
    min = l[0]
    for _, v := range l {
        if  v  < min {
            min = v
        }
    }
    return 
}

func main() {
    l := []int{1, 2, 3, 4, 5}
    fmt.Println(max(l))
    fmt.Println(min(l))
}
