function t1(x, a, b) {
  b = (Math.random()-0.5) * 0.25 + 0.25/2;
  if (a < 0) { b += .75; }
  return a*x + b;
}

var opts = {
  nbars: [1,2,5,10],
  weight: [0],//.5, .75, .9, 1],
  time: [4],
  a: [-.75, 0, .75]
};
