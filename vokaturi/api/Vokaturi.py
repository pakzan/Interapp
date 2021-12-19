# Vokaturi.py
# Copyright (C) 2016 Paul Boersma, Johnny Ip, Toni Gojani
# version 2017-01-02

# This file is the Python interface to the Vokaturi library.
# The declarations are parallel to those in Vokaturi.h.

import ctypes

class Quality(ctypes.Structure):
	_fields_ = [
		("valid",                ctypes.c_int),
		("num_frames_analyzed",  ctypes.c_int),
		("num_frames_lost",      ctypes.c_int)]

class EmotionProbabilities(ctypes.Structure):
	_fields_ = [
		("neutrality",  ctypes.c_double),
		("happiness",   ctypes.c_double),
		("sadness",     ctypes.c_double),
		("anger",       ctypes.c_double),
		("fear",        ctypes.c_double)]

_library = None

def load(path_to_Vokaturi_library):
	global _library

	_library = ctypes.CDLL(path_to_Vokaturi_library)

	_library.VokaturiVoice_create.restype = ctypes.c_void_p
	_library.VokaturiVoice_create.argtypes = [
		ctypes.c_double,                           # sample_rate
		ctypes.c_int]                              # buffer_length

	_library.VokaturiVoice_setRelativePriorProbabilities.restype = None
	_library.VokaturiVoice_setRelativePriorProbabilities.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.POINTER (EmotionProbabilities)]     # priorEmotionProbabilities

	_library.VokaturiVoice_fill.restype = None
	_library.VokaturiVoice_fill.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_double)]          # samples

	_library.VokaturiVoice_extract.restype = None
	_library.VokaturiVoice_extract.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.POINTER (Quality),                  # quality
		ctypes.POINTER (EmotionProbabilities)]     # emotionProbabilities

	_library.VokaturiVoice_reset.restype = None
	_library.VokaturiVoice_reset.argtypes = [
		ctypes.c_void_p]                           # voice

	_library.VokaturiVoice_destroy.restype = None
	_library.VokaturiVoice_destroy.argtypes = [
		ctypes.c_void_p]                           # voice

	_library.Vokaturi_versionAndLicense.restype = ctypes.c_char_p
	_library.Vokaturi_versionAndLicense.argtypes = []

class Voice:

	def __init__(self, sample_rate, buffer_length):
		self._voice = _library.VokaturiVoice_create(sample_rate, buffer_length)

	def setRelativePriorProbabilities(self, priorEmotionProbabilities):
		_library.VokaturiVoice_setRelativePriorProbabilities(self._voice, priorEmotionProbabilities)

	def fill(self, num_samples, samples):
		_library.VokaturiVoice_fill(self._voice, num_samples, samples)

	def extract(self, quality, emotionProbabilities):
		_library.VokaturiVoice_extract(self._voice, quality, emotionProbabilities)

	def reset(self):
		_library.VokaturiVoice_reset(self._voice)

	def destroy(self):
		if not _library is None:
			_library.VokaturiVoice_destroy(self._voice)

def versionAndLicense():
	return _library.Vokaturi_versionAndLicense().decode("UTF-8")

def SampleArrayC(size):
	return (ctypes.c_double * size)()
