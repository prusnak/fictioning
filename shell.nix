with import <nixpkgs> {};

let MyPython = python3.withPackages(ps: with ps; [
  black
  flask
  gunicorn
]);
in
stdenv.mkDerivation {
  name = "fictioning-dev";
  buildInputs = [
    MyPython
  ];
}
