import math

def goertzel(samples, sample_rate, f_start, f_end):
    """
    Implementation of the Goertzel algorithm, useful for calculating individual
    terms of a discrete Fourier transform.
    """
    window_size = len(samples)
    f_step = sample_rate / float(window_size) # JLD: in Hz
    # Calculate which DFT bins we'll have to compute
    k_start = int(math.ceil(f_start / f_step))
    k_end = int(math.floor(f_end / f_step))

    if k_end > window_size - 1: raise ValueError('frequency out of range %s' % k_end)

    # For all the bins between `f_start` and `f_end`, calculate the DFT
    # term
    n_range = range(0, window_size)
    freqs = []
    results = []
    f_step_normalized = 1./window_size # JLD: step in normalized frequency 
    for k in range(k_start, k_end + 1):
        # Bin frequency and coefficients for the computation
        f = k * f_step_normalized # JLD: here you need the normalized frequency
        w_real = 2.0 * math.cos(2.0 * math.pi * f)
        w_imag = math.sin(2.0 * math.pi * f)

        # Doing the calculation on the whole sample
        d1, d2 = 0.0, 0.0
        for n in n_range:
            y  = samples[n] + w_real * d1 - d2
            d2, d1 = d1, y

        # Storing results `(real part, imag part, power)`
        results.append((
            0.5 * w_real * d1 - d2, w_imag * d1,
            d2**2 + d1**2 - w_real * d1 * d2) # removed factor 2: already in w_real!
        )
        freqs.append(f * sample_rate)
    return freqs, results

if __name__ == '__main__':
    # quick test
    import numpy as np
    import pylab

    ##t = np.linspace(0, 1, 44100)
    # JLD: if you do this, the sampling rate is not exactly 44100 anymore:
    #    linspace includes the boundaries 0 and 1, and there are therefore
    #    44100 samples for a bit more than 1 second...
    sample_rate = 44100 # in Hz
    t = np.arange(sample_rate) / np.double(sample_rate) # in seconds
    # JLD: with 1000 samples, a sine at 441Hz leads to a DFT with only one
    # non-nul component:
    sine_wave = np.sin(2*np.pi*441*t)[:1000]  
    freqs, results = goertzel(sine_wave, sample_rate, 0, 22049)
    print(np.array(results))
    pylab.figure()
    pylab.clf()
    pylab.plot(np.array(freqs),
               np.array(results)[:,0]**2 + np.array(results)[:,1]**2,
               marker='x',
               label='computed power')
    pylab.plot(np.array(freqs),
               np.array(results)[:,0]**2 + np.array(results)[:,1]**2,
               linestyle='--',
               marker='o',
               label='returned power')
    pylab.xlim([0,1000])
    pylab.ylabel('Power')
    pylab.xlabel('Frequency (Hz)')
    pylab.legend()
    pylab.show()