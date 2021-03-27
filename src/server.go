package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Starting server at port 8080\n")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err) // Fatal if err, which is equal to return value of http.ListenAndServe() is not nil
	}
}
