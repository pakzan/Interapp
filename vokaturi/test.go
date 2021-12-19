package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/k0kubun/pp"
)

func main() {
	var err error
	y, err := newYoutube("https://www.youtube.com/watch?v=KtqFwrHSRr0")
	if err != nil {
		fmt.Println("Youtube Error")
		pp.Print(err)
		return
	}

	// Download
	_, err = y.Download()
	if err != nil {
		fmt.Println("Download Fail")
		pp.Print(err)
		if e2, ok := err.(*exec.ExitError); ok {
			fmt.Print(string(e2.Stderr))
		}
		return
	}

	// Split
	ff, err := newFfmpeg(filepath.Join(tmpDir, y.v), y.v)
	if err != nil {
		fmt.Println("FFmpeg Fail")
		pp.Print(err)
		return
	}
	_, err = ff.Output()
	if err != nil {
		fmt.Println("Convert Fail")
		fmt.Println(err)
		if e2, ok := err.(*exec.ExitError); ok {
			fmt.Print(string(e2.Stderr))
		}
		return
	}

	// vokaturi
	csv, err := os.Open(filepath.Join("tmp", y.v+"-wav.csv"))
	if err != nil {
		fmt.Println("CVS File Open Fail")
		pp.Print(err)
		return
	}

	scanner := bufio.NewScanner(csv)
	for scanner.Scan() {
		file := strings.Split(scanner.Text(), ",")[0]
		voka, err := newVokaturi(filepath.Join("wavs", file))
		if err != nil {
			fmt.Println("Vokaturi Fail")
			pp.Print(err)
			return
		}
		out, err := voka.Output()
		if err != nil {
			fmt.Println("Vokaturi Fail")
			pp.Print(err)
			return
		}
		fmt.Print(string(out))
	}
}
