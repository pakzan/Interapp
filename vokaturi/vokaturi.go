package main

import (
	"fmt"
	"os/exec"
)

type vokaturi struct {
	*exec.Cmd
}

func newVokaturi(input string) (*vokaturi, error) {
	cmdPath, err := exec.LookPath("measurewav")
	if err != nil {
		return nil, fmt.Errorf("Command Not Found : %v", err)
	}
	if !isExists(input) {
		return nil, fmt.Errorf("Input File Not Found : %s", input)
	}
	return &vokaturi{exec.Command(cmdPath, input)}, nil
}

func (v *vokaturi) setArgs(args ...string) {
	v.Args = append(v.Args, args...)
}
