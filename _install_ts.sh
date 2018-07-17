#!/bin/sh
#   Copyright 2016 Chris McKinney
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not
#   use this file except in compliance with the License.  You may obtain a copy
#   of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# Exit if a command fails
set -e
# Make sure against ./_install_ts.sh-ing
if [ "$(basename "$(readlink -e .)")" = 'tachibanasite' ]; then
    echo 'Already in TachibanaSite install directory. Installing above.'
    cd ..
fi
# Install git if it isn't
if ! which git; then
    git_ver='git-2.9.5'
    git_url="https://www.kernel.org/pub/software/scm/git/${git_ver}.tar.xz"
    if which wget; then
        wget "$git_url"
    elif which curl; then
        curl -OLC - "$git_url"
    else
        echo 'Please install git. Aborting.'
        exit 1
    fi
    tar xf "${git_ver}.tar.xz"
    cd "$git_ver"
    make
    make install
    alias git="$HOME/bin/git"
    cd ..
fi
# Clone TachibanaSite if it isn't
[ -d tachibanasite ] || \
    git clone https://github.com/NighttimeDriver50000/tachibanasite.git
# Update php-markdown
cd tachibanasite
git submodule update --init --recursive
cd ..
# Convenience symlink
[ -h autots ] || ln -s tachibanasite/modules/autots/__main__.py autots
# Install or execute the provided subcommand
# Do not exit on failure; the next section should always run.
set +e
if [ "$#" = 0 ]; then
    ./autots install
    status=$?
else
    ./autots "$@"
    status=$?
fi
set -e
# Pip creates this directory on failure
if [ -f build/pip-delete-this-directory.txt ] \
        && [ "$(ls build | wc -l)" = 1 ]; then
    rm -r build
fi
# Status is that of the autots invocation
exit "$status"
