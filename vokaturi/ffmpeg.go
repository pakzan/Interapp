package main

import (
	"fmt"
	"os/exec"
	"path/filepath"
	"strconv"
)

type ffmpeg struct {
	*exec.Cmd
}

const (
	tmpMovieSuffix = ".*"
	segmentTime    = 5
	outputFormat   = "wavs/emo-%s-%%05d.wav"
)

func newFfmpeg(input string, v string) (*ffmpeg, error) {
	cmdPath, err := exec.LookPath("ffmpeg")
	if err != nil {
		return nil, fmt.Errorf("Command Not Found : %v", err)
	}
	// if !isExists(input) {
	// 	return nil, fmt.Errorf("Input File Not Found : %s", input)
	// }
	files, err := filepath.Glob(input + tmpMovieSuffix)
	if err != nil {
		return nil, err
	}
	if len(files) == 0 {
		return nil, fmt.Errorf("Input file is Not Found : %s", input)
	}
	f := ffmpeg{exec.Command(cmdPath, "-i", files[0])}
	f.setSegment(input, fmt.Sprintf(outputFormat, v))
	return &f, nil
}

func (v *ffmpeg) setSegment(input string, output string) {
	v.setArgs("-f", "segment", "-segment_list", input+"-wav.csv", "-segment_time", strconv.Itoa(segmentTime), output)
}

func (v *ffmpeg) setArgs(args ...string) {
	v.Args = append(v.Args, args...)
}
