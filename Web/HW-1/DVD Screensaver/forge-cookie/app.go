package main

import (
    "os"
    "fmt"
    "bufio"
	"github.com/gorilla/securecookie"
)

func main() {
    SECRET_KEY := os.Getenv("SECRET_KEY")
	Codecs := securecookie.CodecsFromPairs([]byte(SECRET_KEY))

    s := bufio.NewScanner(os.Stdin)
    for s.Scan() {

        Values := make(map[interface{}]interface{})
        Values["username"] = s.Text()

        encoded, err := securecookie.EncodeMulti("session", Values, Codecs...)
        if err != nil {
            fmt.Println(err)
            continue
        }
        fmt.Println(encoded)

    }
}
