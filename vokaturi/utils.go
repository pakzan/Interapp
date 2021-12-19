package main

import "os"

func isExists(filename string) bool {
	_, err := os.Stat(filename)
	return err == nil
}
