FROM tensorflow/tensorflow:2.3.1-gpu

ARG DEBIAN_FRONTEND=noninteractive

RUN add-apt-repository ppa:apt-fast/stable -y
RUN apt-get update
RUN apt-get install apt-fast -y --no-install-recommends

RUN apt-fast upgrade -y
RUN apt-fast install -yq --no-install-recommends git curl

# ffmpeg

RUN git clone --depth 1 https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
RUN cd nv-codec-headers && make -j`nproc` install

RUN apt-fast -yq --no-install-recommends install \
    autoconf \
    automake \
    build-essential \
    cmake \
    git-core \
    libass-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    pkg-config \
    texinfo \
    wget \
    yasm \
    zlib1g-dev
RUN apt-fast -yq install \
	libopencv-dev \
	libtesseract-dev \
	git \
	cmake \
	build-essential \
	libleptonica-dev
RUN apt-fast -yq install \
	liblog4cplus-dev \
	libcurl3-dev
RUN apt-fast -yq install \
	beanstalkd \
	git

RUN git clone https://github.com/openalpr/openalpr.git && \
	cd openalpr/src && \
	mkdir build && \
	cd build && \
	cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && \
	make && \
	make install
RUN mkdir -p ~/ffmpeg_sources ~/bin
	
#NASM
RUN apt-fast -yq install --no-install-recommends nasm

#libx264
RUN apt-fast install libx264-dev -yq --no-install-recommends


#libx265
RUN apt-fast install libx264-dev -yq --no-install-recommends && \ 
    apt-fast install libx265-dev -yq --no-install-recommends && \ 
    apt-fast install libnuma-dev -yq --no-install-recommends

#libvpx
RUN  apt-fast install libvpx-dev -yq --no-install-recommends

#libfdk-aac
RUN  apt-fast install libfdk-aac-dev -yq --no-install-recommends

#libmp3lame
RUN  apt-fast install libmp3lame-dev -yq --no-install-recommends
#libopus
RUN apt-fast install libopus-dev -yq --no-install-recommends

#libaom
RUN cd ~/ffmpeg_sources && \
    git -C aom pull 2> /dev/null || git clone --depth 1 https://aomedia.googlesource.com/aom && \
    mkdir -p aom_build && \
    cd aom_build && \
    PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED=off -DENABLE_NASM=on ../aom && \
    PATH="$HOME/bin:$PATH" make && \
    make -j`nproc` install

RUN cd ~/ffmpeg_sources && \
    git -C SVT-AV1 pull 2> /dev/null || git clone --depth 1 https://github.com/AOMediaCodec/SVT-AV1.git && \
    mkdir -p SVT-AV1/build && \
    cd SVT-AV1/build && \
    PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF .. && \
    PATH="$HOME/bin:$PATH" make && \
    make -j`nproc` install

RUN apt-fast install -yq libunistring-dev cuda-npp-10-1 \
    cuda-npp-dev-10-1 --no-install-recommends

RUN export PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig/:/usr/local/lib/pkgconfig/ && cd ~/ffmpeg_sources && \
    wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
    tar xjvf ffmpeg-snapshot.tar.bz2 && \
    cd ffmpeg && \
    PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
    --prefix="$HOME/ffmpeg_build" \
    --pkg-config-flags="--static" \
    --extra-cflags="-I$HOME/ffmpeg_build/include" \
    --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
    --extra-libs="-lpthread -lm" \
    --bindir="$HOME/bin" \
    --enable-gpl \
    --enable-gnutls \
    --enable-libaom \
    --enable-libass \
    --enable-libfdk-aac \
    --enable-libfreetype \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libsvtav1 \
    --enable-libvorbis \
    --enable-libvpx \
    --enable-libx264 \
    --enable-libx265 \
    --enable-nonfree \
    --enable-cuda-sdk \
    --enable-libnpp \
    --extra-cflags=-I/usr/local/cuda/include \
    --extra-ldflags=-L/usr/local/cuda/lib64 && \
    PATH="$HOME/bin:$PATH" make && \
    make -j`nproc` install && \
    hash -r

RUN apt-fast install default-jdk default-jre -yq --no-install-recommends

RUN apt-fast install libgstreamer1.0-0 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio -yq --no-install-recommends

RUN echo 'PATH="$HOME/bin:$PATH"' >> ~/.bashrc


# Install useful Python packages using apt-get to avoid version incompatibilities with Tensorflow binary
# especially numpy, scipy, skimage and sklearn (see https://github.com/tensorflow/tensorflow/issues/2034)
# RUN apt-fast update && apt-fast install -yq --no-install-recommends \
#     python3-numpy \
#     python3-scipy \
#     python3-nose \
#     python3-h5py \
#     python3-skimage \
#     python3-matplotlib \
#     python3-pandas \
#     python3-sklearn \
#     python3-sympy &&\
#     apt-get clean && \
#     apt-get autoremove && \
#     rm -rf /var/lib/apt/lists/*





# Install some dependencies
RUN apt-get update && apt-get install apt-utils -y
RUN apt-get update && apt-get install -y \
    bc \
    build-essential \
    cmake \
    curl \
    g++ \
    gfortran \
    git \
    libffi-dev \
    libfreetype6-dev \
    libhdf5-dev \
    libjpeg-dev \
    liblcms2-dev \
    libopenblas-dev \
    liblapack-dev \
    libopenjp2* \
    libpng-dev \
    libssl-dev \
    libtiff5-dev \
    libwebp-dev \
    libzmq3-dev \
    nano \
    pkg-config \
    python-dev \
    software-properties-common \
    unzip \
    vim \
    wget \
    zlib1g-dev \
    qt5-default \
    libvtk6-dev \
    zlib1g-dev \
    libjpeg-dev \
    libwebp-dev \
    libpng-dev \
    libtiff5-dev \
    libopenexr-dev \
    libgdal-dev \
    libdc1394-22-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libtheora-dev \
    libvorbis-dev \
    libxvidcore-dev \
    libx264-dev \
    yasm \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    libv4l-dev \
    libxine2-dev \
    libtbb-dev \
    libeigen3-dev \
    python-dev \
    python-tk \
    python-numpy \
    python3-dev \
    python3-tk \
    python3-numpy \
    ant \
    default-jdk \
    doxygen


# OpenCV dependency

RUN echo "deb http://security.ubuntu.com/ubuntu xenial-security main" | tee -a /etc/apt/sources.list && \
    apt update -y

RUN  apt-fast update && \ 
    apt-fast install cmake g++ python3-dev \
    python3-numpy \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    libgtk-3-dev \
    libpng-dev \
    libjpeg-dev \
    libopenexr-dev \
    libtiff-dev \
    libwebp-dev \
    libtbb2 \
    libtbb-dev \
    libjasper1 \
    libjasper-dev \
    libpq-dev \
    libhdf5-dev -y && \
    apt-fast autoremove 


RUN python3 -m pip install --upgrade pip

# Add SNI support to Python
RUN pip3 --no-cache-dir install \
    pyopenssl \
    ndg-httpsclient \
    pyasn1 \
    setuptools \
    future>=0.17.1 

ENV OPENCV_VERSION=4.5.0
ENV OPENCV_PYTHON_VERSION=9.2

RUN mkdir /temp \ 
    && wget -nv https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip -O /temp/opencvcontrib-${OPENCV_VERSION}.zip \
    && wget -nv https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip -O /temp/opencv-${OPENCV_VERSION}.zip \
    && wget -nv https://github.com/VLAM3D/opencv-python/archive/${OPENCV_PYTHON_VERSION}.zip -O /temp/opencv-python.zip \
    && unzip /temp/opencv-${OPENCV_VERSION}.zip\
    && unzip /temp/opencvcontrib-${OPENCV_VERSION}.zip\
    && unzip /temp/opencv-python.zip

RUN apt-fast install -yq libcudnn7-dev libopenjp2-7-dev libopenjp2-7 libopenjpip7 libopenjpip-dec-server libtiff5-dev libtiff5 libopenjpip-server
#RUN ln -s /usr/local/cuda-10.2/targets/x86_64-linux/lib/libcublas.so.10.2.2.214 /usr/local/cuda-10.2/targets/x86_64-linux/lib/libcublas.so
#RUN apt-fast install -yq qt5-default

RUN apt-fast -yq install cuda-cufft-dev-10-1
RUN apt-fast -yq install libavfilter-dev
#RUN apt-fast -yq install libcublas-dev cuda-cublas-dev-10-0 cuda-cublas-10-0 libcublas-*
RUN apt-fast -yq install cuda-libraries-dev-10-1

RUN echo 'PATH="/usr/local/cuda-10.1/targets/x86_64-linux/lib:$PATH"' >> ~/.bashrc
RUN echo 'PATH="/usr/local/cuda-10.1/targets/x86_64-linux/include:$PATH"' >> ~/.bashrc
RUN echo 'CPATH=/usr/local/cuda-10.1/targets/x86_64-linux/include:$CPATH' >> ~/.bashrc
RUN echo 'LD_LIBRARY_PATH=/usr/local/cuda-10.1/targets/x86_64-linux/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
RUN echo 'LIBRARY_PATH=/usr/local/cuda-10.1/targets/x86_64-linux/lib:$LIBRARY_PATH' >> ~/.bashrc
RUN echo 'PATH=/usr/local/cuda-10.1/bin:$PATH' >> ~/.bashrc

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/libcublas-dev_10.1.0.105-1_amd64.deb && \
    dpkg -i libcublas-dev_10.1.0.105-1_amd64.deb && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/libcublas10_10.1.0.105-1_amd64.deb && \
    dpkg -i libcublas10_10.1.0.105-1_amd64.deb && \
    cp /usr/include/cublas* /usr/local/cuda-10.1/include/ && \
    cp /usr/include/cublas* /usr/local/cuda-10.1/targets/x86_64-linux/lib && \
    cp /usr/lib/x86_64-linux-gnu/libcublas* /usr/local/cuda-10.1/targets/x86_64-linux/lib && \
    cp /usr/lib/x86_64-linux-gnu/libcublas* /usr/local/cuda-10.1/targets/x86_64-linux/lib

RUN source ~/.bashrc && cd /opencv-${OPENCV_VERSION} && mkdir build && cd build && \
    # BUILD SHARED LIBS FOR C++ DEV WITH CUDA
    cmake .. -DBUILD_TIFF=ON \
    -DBUILD_opencv_java=OFF \
    -DCUDA_cufft_LIBRARY=/usr/local/cuda-10.1/targets/x86_64-linux/lib \
    -DCUDA_cublas_LIBRARY=/usr/local/cuda-10.1/targets/x86_64-linux/lib \
    -DCUDA_CUBLAS_LIBRARIES=/usr/local/cuda-10.1/targets/x86_64-linux/lib \
    -DCUDA_CUFFT_LIBRARIES=/usr/local/cuda-10.1/targets/x86_64-linux/lib \
    -DCUDA_INCLUDE_DIRS=/usr/local/cuda-10.1/targets/x86_64-linux/include \
    -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-10.1 \
    -DCUDA_BIN_PATH=/usr/local/cuda-10.1 \
    -DWITH_CUDA=ON \
    -DWITH_CUDNN=ON \
    -DBUILD_SHARED_LIBS=OFF \
    -DOPENCV_DNN_CUDA=ON \
    -DCUDA_ARCH_BIN=7.5 \
    -DCUDA_ARCH_PTX=7.5 \
    -DWITH_CUBLAS=ON \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DWITH_OPENGL=ON \
    -DWITH_OPENCL=ON \
    -DWITH_IPP=ON \
    -DWITH_TBB=ON \
    -DWITH_MKL=ON \
    -DWITH_QT=5 \
    -DMKL_WITH_TBB=ON \
    -DWITH_EIGEN=ON \
    -DBUILD_PROTOBUF=ON \
    -DWITH_V4L=ON \
    -DWITH_FFMPEG=ON \
    -DWITH_GSTREAMER=ON \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_TESTS=OFF \
    -DBUILD_PERF_TESTS=OFF \
    -DBUILD_NEW_PYTHON_SUPPORT=ON \
    -DBUILD_opencv_python3=ON \
    -DHAVE_opencv_python3=ON \
    -DPROTOBUF_INCLUDE_DIR=/protobuf \
    -DPROTOBUF_LIBRARY=/usr/local/lib \
    -DPYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
    -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON \
    -DOPENCV_ENABLE_NONFREE=ON \
    -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-${OPENCV_VERSION}/modules \
    -DBUILD_opencv_legacy=OFF \
    -DCMAKE_BUILD_TYPE=RELEASE \
    -DCMAKE_INSTALL_PREFIX=/usr/local


RUN source ~/.bashrc && cd /opencv-${OPENCV_VERSION}/build && make -j $(nproc) install 


RUN apt --fix-broken install -y

# Install dependencies for Caffe
RUN apt-fast update && apt-fast install \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libhdf5-serial-dev \
    libleveldb-dev \
    liblmdb-dev \
    libopencv-dev \
    libprotobuf-dev \
    libsnappy-dev -y \
    protobuf-compiler && \
    apt-fast clean && \
    apt-fast autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install Caffe
RUN apt-get update && apt-get install caffe-cuda -y


ARG THEANO_VERSION=rel-0.8.2

# Install Theano and set up Theano config (.theanorc) for CUDA and OpenBLAS
RUN pip3 --no-cache-dir install git+git://github.com/Theano/Theano.git@${THEANO_VERSION} && \
    \
    echo "[global]\ndevice=gpu\nfloatX=float32\noptimizer_including=cudnn\nmode=FAST_RUN \
    \n[lib]\ncnmem=0.95 \
    \n[nvcc]\nfastmath=True \
    \n[blas]\nldflag = -L/usr/lib/openblas-base -lopenblas \
    \n[DebugMode]\ncheck_finite=1" \
    > /root/.theanorc


# Install Lasagne
RUN pip3 install -r https://raw.githubusercontent.com/Lasagne/Lasagne/master/requirements.txt
RUN pip3 install https://github.com/Lasagne/Lasagne/archive/master.zip
RUN pip3 install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html


RUN pip3 install mysql-connector \
    && pip3 install sklearn \
    && pip3 install  imutils \
    && pip3 install scipy \
    && pip3 install beautifultable \
    && apt-get install build-essential cmake pkg-config  -y \
    && apt-get install libx11-dev libatlas-base-dev  -y \
    && apt-get install libgtk-3-dev libboost-python-dev  -y \
    && apt-get install python3-dev python3-pip  -y

RUN pip3 install numpy \
    && pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython \
    && apt-get update  \
    && apt-get install build-essential software-properties-common -y  \
    && add-apt-repository ppa:ubuntu-toolchain-r/test -y  \
    && apt-get update  \
    && apt-get install gcc-6 g++-6 -y \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 \
    && gcc -v


#Dlib
RUN git clone https://github.com/davisking/dlib.git \
    && cd dlib \
    && git submodule init \
    && git submodule update \
    && mkdir build \
    && cd build \
    && cmake .. -DLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 .. \
    && cmake --build . --config Release \
    && cd ../ \
    && python3 setup.py install 



RUN  add-apt-repository universe && \
    add-apt-repository multiverse && \
    apt-get update


#Install useful Python packages using apt-get to avoid version incompatibilities with Tensorflow binary
#especially numpy, scipy, skimage and sklearn (see https://github.com/tensorflow/tensorflow/issues/2034)
RUN apt-fast update && apt-fast install -yq --no-install-recommends \
    python3-numpy \
    python3-scipy \
    python3-nose \
    python3-h5py \
    python3-skimage \
    python3-matplotlib \
    python3-pandas \
    python3-sklearn \
    python3-sympy &&\
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*


RUN pip3 install -U scipy psutil scikit-image

RUN apt-get update
RUN apt-get install net-tools openssh-server iptables iputils-ping -y



# docker run --net host  --gpus=all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix  -itd  -v /home/mgscore/hasan:/hasan -v /home/mgscore/tensortest:/test --security-opt apparmor:unconfined  --name mgscontainer  mgsimage

