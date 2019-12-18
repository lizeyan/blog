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