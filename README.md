iButton_1990a
=============

Arduino sketch to impersonate an iButton 1990A fob. Based on [OneWireSlave](https://github.com/MarkusLange/OneWireSlave) but heavily modified. The important code is in the OneWireSlave library in lib; the sketch in src just calls its API.

To run, install [ino](http://inotool.org/) and execute

    ino build && ino upload && ino serial

in the repository directory.