package main

import (
	"fmt"
	"os/exec"
	"path/filepath"
)

const (
	movieSuffix = ".mp4"
	tmpDir      = "tmp"
)

type youtubedl struct {
	*exec.Cmd
}

func newYoutubedl(targetURL string, output string) (*youtubedl, error) {

	cmdPath, err := exec.LookPath("youtube-dl")
	if err != nil {
		return nil, fmt.Errorf("Command Not Found : %v", err)
	}
	// if !isExists(input) {
	// 	return nil, fmt.Errorf("Input File Not Found : %s", input)
	// }
	// if isExists(output + tmpMovieSuffix) {
	// 	return nil, fmt.Errorf("Output File is Already Exist : %s", output+tmpMovieSuffix)
	// }
	return &youtubedl{exec.Command(cmdPath, "-o", filepath.Join(tmpDir, output+movieSuffix), targetURL)}, nil
}

func (v *youtubedl) setArgs(args ...string) {
	v.Args = append(v.Args, args...)
}

func isDownloadCompleted(v string) bool {
	return isExists(filepath.Join(tmpDir, v+movieSuffix))
}
