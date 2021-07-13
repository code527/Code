package main

import (
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var User = "root"
var Pass = "83848521"
var Host = "127.0.0.1"
var Port = 3306
var Name = "test"
var Charset = "utf8"

func main() {
	Dsn := fmt.Sprintf("%s:%s@%s(%s:%d)/%s?%s", User, Pass, "tcp", Host, Port, Name, Charset)
	pool, err := sql.Open("mysql", Dsn)
	if err != nil {
		fmt.Println("Open mysql pool failed, Err:", err.Error())
		return
	}

	pool.SetConnMaxLifetime(100 * time.Second) // 最大连接周期，超过时间的连接就close
	pool.SetMaxOpenConns(5)                    // 设置最大连接数
	pool.SetMaxIdleConns(3)                    // 设置闲置连接数

	fmt.Println("Ping mysql Err:", pool.Ping())

	rows, err := pool.Query("show tables;")
	if err != nil {
		fmt.Println("show tables failed, Err:", err.Error())
	}
	defer rows.Close()

	for rows.Next() {
		var table string
		scanErr := rows.Scan(&table)
		if scanErr != nil {
			fmt.Println("scan is error: ", scanErr.Error())
			continue
		}
		fmt.Println(table)
		if strings.Contains(table, "pet") {
			tmp := strings.Split(table, "_")
			if len(tmp) >= 2 {
				for i, v := range tmp {
					fmt.Println(i, v)
				}

				if strings.Compare(tmp[1], "20210703") <= 0 {
					// 删除表名
					_, err := pool.Exec("drop table " + table)
					if err != nil {
						fmt.Println("drop table: ", table, "error: ", err.Error())
					}
					fmt.Println("drop table ", table)
				}
			}
		}
	}

}
