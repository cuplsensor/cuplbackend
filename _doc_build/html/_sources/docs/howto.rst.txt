How To Deploy PSWebApp
======================

Build Web Base
---------------

Navigate to the project root directory and run::

    docker build web_base -t mmackay/web_base:latest

This will build the first base image and install a list of Python packages including Flask.


Build URL Decoder
-----------------

Navigate to the project root directory and run::

    docker build pscodec -t mmackay/urldec_base:latest

This will install the URL Decoder Python package from the PSCodec directory.


Run web image with Docker Compose
----------------------------------

Navigate to the project root directory and run::

    sh go2.sh

