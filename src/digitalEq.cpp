/*******************************************************************************/
/*
   DISCLAIMER: This is completely free software. Do whatever you want with it!
   AUTHOR: Jack Olivieri
   DATE: September 2017
*/
/*******************************************************************************/

#include <vector>
#include <stdexcept>
#include <cmath>
#include <algorithm>
#include <numeric>
#include "digitalEq.hpp"

digitalEq::digitalEq(unsigned int f_s, unsigned int n_ch, std::vector<eqParams> params) {

  /* number of bands */
  this->eq_size = static_cast<unsigned int>(params.size());
  this->params = params;

  /* equalizer parameters */
  this->f_s = f_s;
  this->n_ch = n_ch;

  /* channel in/output allocation */
  x_n_1 = new short[n_ch];
  x_n_2 = new short[n_ch];
  y_n   = new double*[n_ch];
  y_n_1 = new double*[n_ch];
  y_n_2 = new double*[n_ch];

  /* band output allocation */
  for (unsigned int ch = 0; ch < n_ch; ch++) {
    y_n[ch]   = new double[eq_size];
    y_n_1[ch] = new double[eq_size];
    y_n_2[ch] = new double[eq_size];
  }

  for (auto param : params) {
    double theta = 2 * M_PI * (param.f_0 / f_s);
    /* beta */
    double tempParam = (1 - std::tan(theta/(2*param.Q))) /  \
      (2*(1 + std::tan(theta/(2*param.Q))));
    beta.push_back(tempParam);
    /* lambda */
    tempParam = (.5 + tempParam) * std::cos(theta);
    lambda.push_back(tempParam);
    /* alpha */
    tempParam = (.5 - tempParam) / 2;
    alpha.push_back(tempParam);
  }
}

void digitalEq::process_sample(short* eq_y, short* x_n) {

  /* process each band */
  for (unsigned int band = 0; band < eq_size; band++) {
    /* process each channel */
    for (unsigned int ch = 0; ch < n_ch; ch++) {
      y_n[ch][band] = 2*(alpha[band] * (x_n[ch]-x_n_2[ch]) + \
                                          lambda[band]*y_n_1[ch][band] - \
                                          beta[band] * y_n_2[ch][band]) / eq_size;
    }
  }

  /* update input and output history */
  std::copy(x_n_1, x_n_1+n_ch, x_n_2);
  std::copy(x_n, x_n+n_ch, x_n_1);
  for (unsigned int ch = 0; ch < n_ch; ch++) {
    std::copy(y_n_1[ch], y_n_1[ch]+eq_size, y_n_2[ch]);
    std::copy(y_n[ch], y_n[ch]+eq_size, y_n_1[ch]);
  }

  /* apply gain and accumulate for each channel */
  for (unsigned int ch = 0; ch < n_ch; ch++) {
    gain_y_n[ch] = 0;
    for (unsigned int band = 0; band < eq_size; band++) {
      gain_y_n[ch] += y_n[ch][band]*params[band].G;
    }
    /* convert back to short */
    eq_y[ch] = static_cast<short>(gain_y_n[ch]);
  }
}
