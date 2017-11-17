#!/bin/sh
set -e
if [ "$(basename "$(readlink -e .)")" = 'tachibanasite' ]; then
    echo 'Already in TachibanaSite install directory. Installing above.'
    cd ..
fi
if ! which git; then
    git_ver='git-2.9.5'
    git_url="https://www.kernel.org/pub/software/scm/git/${git_ver}.tar.xz"
    if which wget; then
        wget "$git_url"
    elif which curl; then
        curl -OLC - "$git_url"
    else
        echo 'Please install git. Aborting.'
    fi
    tar xf "${git_ver}.tar.xz"
    cd "$git_ver"
    make
    make install
    alias git="$HOME/bin/git"
    cd ..
fi
[ -d tachibanasite ] || \
    git clone https://github.com/NighttimeDriver50000/tachibanasite.git
[ -h autots ] || ln -s tachibanasite/modules/autots/__init__.py autots
./autots install || true
if [ -f build/pip-delete-this-directory.txt ] \
        && [ "$(ls build | wc -l)" = 1 ]; then
    rm -r build
fi
