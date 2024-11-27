// generic single qubit gate
gate u(theta,phi,lambda) q { U(theta,phi,lambda) q; }
// phase gate
gate p(lambda) q { U(0,0,lambda) q; }
// sqrt(X)
gate sx a { sdg a; h a; sdg a; }
// inverse sqrt(X)
gate sxdg a { s a; h a; s a; }

// controlled rx rotation
gate crx(lambda) a,b
{
  u1(pi/2) b;
  cx a,b;
  u3(-lambda/2,0,0) b;
  cx a,b;
  u3(lambda/2,-pi/2,0) b;
}
// controlled ry rotation
gate cry(lambda) a,b
{
  ry(lambda/2) b;
  cx a,b;
  ry(-lambda/2) b;
  cx a,b;
}
gate cp(lambda) a,b
{
p(lambda/2) a;
cx a,b;
p(-lambda/2) b;
cx a,b;
p(lambda/2) b;
}
// controlled-sqrt(X)
gate csx a,b { h b; cu1(pi/2) a,b; h b; }
// controlled-U gate
gate cu(theta,phi,lambda,gamma) c, t
{ p(gamma) c;
  p((lambda+phi)/2) c;
  p((lambda-phi)/2) t;
  cx c,t;
  u(-theta/2,0,-(phi+lambda)/2) t;
  cx c,t;
  u(theta/2,phi,0) t;
}
// two-qubit XX rotation
gate rxx(theta) a,b
{
  u3(pi/2, theta, 0) a;
  h b;
  cx a,b;
  u1(-theta) b;
  cx a,b;
  h b;
  u2(-pi, pi-theta) a;
}
// two-qubit ZZ rotation
gate rzz(theta) a,b
{
  cx a,b;
  u1(theta) b;
  cx a,b;
}
// relative-phase CCX
gate rccx a,b,c
{
  u2(0,pi) c;
  u1(pi/4) c;
  cx b, c;
  u1(-pi/4) c;
  cx a, c;
  u1(pi/4) c;
  cx b, c;
  u1(-pi/4) c;
  u2(0,pi) c;
}
// relative-phase 3-controlled X gate
gate rc3x a,b,c,d
{
  u2(0,pi) d;
  u1(pi/4) d;
  cx c,d;
  u1(-pi/4) d;
  u2(0,pi) d;
  cx a,d;
  u1(pi/4) d;
  cx b,d;
  u1(-pi/4) d;
  cx a,d;
  u1(pi/4) d;
  cx b,d;
  u1(-pi/4) d;
  u2(0,pi) d;
  u1(pi/4) d;
  cx c,d;
  u1(-pi/4) d;
  u2(0,pi) d;
}
// 3-controlled X gate
gate c3x a,b,c,d
{
    h d;
    p(pi/8) a;
    p(pi/8) b;
    p(pi/8) c;
    p(pi/8) d;
    cx a, b;
    p(-pi/8) b;
    cx a, b;
    cx b, c;
    p(-pi/8) c;
    cx a, c;
    p(pi/8) c;
    cx b, c;
    p(-pi/8) c;
    cx a, c;
    cx c, d;
    p(-pi/8) d;
    cx b, d;
    p(pi/8) d;
    cx c, d;
    p(-pi/8) d;
    cx a, d;
    p(pi/8) d;
    cx c, d;
    p(-pi/8) d;
    cx b, d;
    p(pi/8) d;
    cx c, d;
    p(-pi/8) d;
    cx a, d;
    h d;
}
// 3-controlled sqrt(X) gate, this equals the C3X gate where the CU1 rotations are -pi/8 not -pi/4
gate c3sqrtx a,b,c,d
{
    h d; cu1(pi/8) a,d; h d;
    cx a,b;
    h d; cu1(-pi/8) b,d; h d;
    cx a,b;
    h d; cu1(pi/8) b,d; h d;
    cx b,c;
    h d; cu1(-pi/8) c,d; h d;
    cx a,c;
    h d; cu1(pi/8) c,d; h d;
    cx b,c;
    h d; cu1(-pi/8) c,d; h d;
    cx a,c;
    h d; cu1(pi/8) c,d; h d;
}
// 4-controlled X gate
gate c4x a,b,c,d,e
{
    h e; cu1(pi/2) d,e; h e;
    c3x a,b,c,d;
    h e; cu1(-pi/2) d,e; h e;
    c3x a,b,c,d;
    c3sqrtx a,b,c,e;
}
// cphase
gate cphase(theta) a, b
{
  U(0, 0, theta / 2) a;
  CX a, b;
  U(0, 0, -theta / 2) b;
  CX a, b;
  U(0, 0, theta / 2) b;
}

// sdag
gate sdag a { sdg a; }
// tdag
gate tdag a { tdg a; }
