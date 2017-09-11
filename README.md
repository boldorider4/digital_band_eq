# Digital multi-band Audio EQ

### Description

This project presents an implementation of a multi-band digital audio equalizer, by means of filtering a 16-bit
mono/stereo PCM audio stream through a bank of parallel band-pass filters.

### Project goal

The end-goal of the project is not just having a lightweight equalizer library, but also integrate such a library
in a [jack framework](http://jackaudio.org/), whereby the audio signal of an application can be taken, passed to this
library and ultimately streamed to whatever audio server is available on one's machine (that is up to the developer!).

In my specific case, I want to be able to take the audio from a light-weight audio player (such as [cmus](https://cmus.github.io/))
which lacks audio equalizing capabilities, apply the equalization from this simple library, and route it straight to
CoreAudio on macOS. A similar application is found in this [project](http://djcj.org/jackeq), but only works on Linux and
includes a sophisticated GUI (plus, additional stuff) that I don't require.

[second_order_filter_s]: ./doc/second_order_filter_s.png "Second order S-domain filter"
[second_order_filter_z]: ./doc/second_order_filter_z.png "Second order Z-domain filter"
[second_order_coefficients]: ./doc/second_order_coefficients.png "Second order filter coefficients"

### Filter design

Each equalizer band is implemented by using a second order filter of the following form:

![Second order S-domain filter][second_order_filter_s]

which in turn, after transforming into the Z-domain, becomes:

![Second order Z-domain filter][second_order_filter_z]

Each coefficient can be estimated as follows:

![Second order filter coefficients][second_order_coefficients]

where *Q = f_0/(f_2/f_1)* and *theta_0 = 2\*pi\*(f_0/f_s)*. *f_0* is the center frequency of the band-pass filter and
*f_s* is the sampling frequency of the input signal. *f_1* and *f_2* identify the *stop-band* of the band-pass filter
where the response gain crosses -3 dB (also corresponding to the half-power point).

### Reference EQ implementation

A reference implementation of such an equalizer is realized in python and can be found in

test/python/digitalEq.py

The different parameters used by the filter are 3 arrays of size equal to the number of bands. Each array location
(corresponding to an EQ band) contains:
* f_0: center frequency value
* Q: filter 'Quality' value, detemining its sharpness
* G: band gain value for boosting or ducking the corresponding band

the *test/python/generate_refs.py* file is used to test the reference implementation EQ class and filter a few sample
audio clips with various EQ configurations. By running

python generate_refs.py

one can obtain reference *wav files* that can be used to test the conformance of a C++ implementation of the equalizer.