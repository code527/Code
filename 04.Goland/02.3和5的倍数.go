/*
编写一个程序，打印从 1 到 100 的数字。当是三的倍数就打印 “Fizz” 代替数字，当是5的倍数就打印 “Buzz”。当数字同时是3和5的倍数时，打印 “FizzBuzz”
*/

package main

import "fmt"

func main() {
    const (
        FIZZ = 3
        BUZZ = 5
    )
    var p bool
    for i := 1; i < 100; i++ {
        p = false
        if i % FIZZ == 0 {
            fmt.Println("Fizz")
            p = true
        }
        if i %  BUZZ == 0 {
            fmt.Println("Buzz")
            p = true
        }
        if  !p {
            fmt.Println(i)
        }
        fmt.Println()
    }
}

