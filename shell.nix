with import <nixpkgs> {};

let MyPython = python3.withPackages(ps: with ps; [
  black
  flask
]);
in
stdenv.mkDerivation {
  name = "fictioning-dev";
  buildInputs = [
    MyPython
  ];
}
