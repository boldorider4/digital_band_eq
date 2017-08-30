#include <vector>
#include "digitalEq.hpp"

int main() {

  params = std::vector<eqParams>;
  params.push_back({1000, 1.3, .8});
  params.push_back({15000, 1.3, 1});

  digitalEq fooEq(44100, 2, params);

  return 0;
}
