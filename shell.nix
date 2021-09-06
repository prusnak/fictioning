with import <nixpkgs> {};

let MyPython = python3.withPackages(ps: with ps; [ flask ]);
in
stdenv.mkDerivation {
  name = "fictioning-dev";
  buildInputs = [
    MyPython
  ];
}
