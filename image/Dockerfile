FROM ubuntu:18.04
RUN apt-get update -y && apt-get install curl git npm -y && apt-get autoremove && apt-get autoclean && \
    (curl -L "https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb" > /tmp/pandoc.deb) && \
    dpkg -i /tmp/pandoc.deb && \
    pandoc --version && \
    (curl -o- -L https://yarnpkg.com/install.sh | bash) && \
    export PATH=$HOME/.yarn/bin:$PATH && \
    npm --version && \
    npm install -g hexo hexo-cli && \
    npm install 
