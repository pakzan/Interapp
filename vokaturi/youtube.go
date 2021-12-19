package main

import (
	"fmt"
	"net/url"
	"regexp"
)

const youtubeFormat = "https://www.youtube.com/watch?v=%s"

type youtube struct {
	v         string
	parsedURL string
}

func newYoutube(u string) (*youtube, error) {
	parsedURL, err := url.Parse(u)

	v := parsedURL.Query().Get("v")
	if err != nil {
		return nil, err
	}
	if !checkRegexp(`[A-Za-z0-9]*`, v) && len(v) < 12 {
		return nil, fmt.Errorf("youtube param error : %s", v)
	}

	purl := fmt.Sprintf(youtubeFormat, v)

	return &youtube{v, purl}, nil
}

func checkRegexp(reg, str string) bool {
	return regexp.MustCompile(reg).Match([]byte(str))
}

func (y *youtube) Download() ([]byte, error) {
	if isDownloadCompleted(y.v) {
		return nil, nil
	}

	ydl, err := newYoutubedl(y.parsedURL, y.v)
	if err != nil {
		return nil, err
	}
	return ydl.Output()
}
