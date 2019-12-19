---
title: install PyPy
---

## Install PyPy
```
pyenv install pypy3.6-7.2.0
```


## Install NumPy, Pandas
``` bash
apt-get install libblas-dev liblapack-dev
pip install cython
pip install numpy
pip install pandas
```

## Install SciPy
``` bash
apt-get install gfortran pybind11-dev
```
(鳖pip intall pybind11，会导致其他包编译不了，未知原因)
or on macOS X
``` bash
brew install gcc
# and then set symbol links by yourself
```

```
export MACOSX_DEPLOYMENT_TARGET=10.10
```

export LDFLAGS="-L/usr/local/opt/libffi/lib"

export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig"

``` bash
pip install "scipy==1.3.3"
```

(1.4.0暂时安装不了)