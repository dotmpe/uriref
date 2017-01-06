#!/usr/bin/env bash

set -e

test -z "$Build_Debug" || set -x

test -z "$Build_Deps_Default_Paths" || {

  test -n "$SRC_PREFIX" || {
    test -w /src/ \
      && SRC_PREFIX=/src/ \
      || SRC_PREFIX=$HOME/build
  }

  test -n "$PREFIX" || {
    test -w /usr/local/ \
      && PREFIX=/usr/local/ \
      || PREFIX=$HOME/.local
  }
}

test -n "$sudo" || sudo=
test -z "$sudo" || pref="sudo $pref"
test -z "$dry_run" || pref="echo $pref"

test -n "$SRC_PREFIX" || {
  echo "Not sure where checkout"
  exit 1
}

test -n "$PREFIX" || {
  echo "Not sure where to install"
  exit 1
}

test -d $SRC_PREFIX || ${pref} mkdir -vp $SRC_PREFIX
test -d $PREFIX || ${pref} mkdir -vp $PREFIX


install_docopt()
{
  test -n "$install_f" || install_f="$py_setup_f"
  git clone https://github.com/dotmpe/docopt-mpe.git $SRC_PREFIX/docopt-mpe
  ( cd $SRC_PREFIX/docopt-mpe \
      && git checkout 0.6.x \
      && $pref python ./setup.py install $install_f )
}

install_mkdoc()
{
  test -n "$MKDOC_BRANCH" || MKDOC_BRANCH=master
  echo "Installing mkdoc ($MKDOC_BRANCH)"
  (
    cd $SRC_PREFIX
    git clone https://github.com/dotmpe/mkdoc.git
    cd mkdoc
    git checkout $MKDOC_BRANCH
    ./configure $PREFIX && ./install.sh
  )
  rm Makefile
  ln -s $PREFIX/share/mkdoc/Mkdoc-full.mk Makefile
}




main_entry()
{
  test -n "$1" || set -- all

  case "$1" in all|python|project|docopt)
      # Using import seems more robust than scanning pip list
      python -c 'import docopt' || { install_docopt || return $?; }
    ;; esac

  case "$1" in all|mkdoc)
      install_mkdoc || return $?
    ;; esac

  echo "OK. All pre-requisites for '$1' checked"
}

test "$(basename $0)" = "install-dependencies.sh" && {
  test -n "$1" || set -- all
  while test -n "$1"
  do
    main_entry "$1" || exit $?
    shift
  done
} || printf ""

# Id: uriref/0 install-dependencies.sh
