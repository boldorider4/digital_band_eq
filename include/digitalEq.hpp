/*******************************************************************************/
/*
   DISCLAIMER: This is completely free software. Do whatever you want with it!
   AUTHOR: Jack Olivieri
   DATE: August 2017
*/
/*******************************************************************************/

#include <vector>

typedef struct {
  unsigned int f_0;
  double Q;
  double G;
} eqParam;

class digitalEq {

public:
  digitalEq(unsigned int f_s, unsigned int n_ch, std::vector<eqParams> params);
  void process_sample(short* eq_y, short* x_n);

private:
  unsigned int f_s;
  unsigned int n_ch;
  unsigned int eq_size;
  /* input history */
  short *x_n_1, *x_n_2;
  /* output history */
  double ** y_n, **y_n_1, **y_n_2;
  /* temp variable for storing gain applied to each channel */
  double* gain_y_n;
  /* filter parameters: beta, lambda, alpha */
  std::vector<double> beta, lambda, alpha;
  /* filter initialization parameters */
  std::vector<eqParams> params;
};
