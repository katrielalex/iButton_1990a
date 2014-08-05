iButton_1990a
=============

Arduino sketch to impersonate an iButton 1990A fob. Based on [OneWireSlave](https://github.com/MarkusLange/OneWireSlave) but heavily modified. The important code is in the OneWireSlave library in lib; the sketch in src just calls its API.

To run, install [ino](http://inotool.org/) and execute

    ino build && ino upload && ino serial

in the repository directory. You'll first need to add a `roms.config` file in `src` with the ID of the fob you want to impersonate; a sample file is already there, or you can read the code off of your own fob using the stock OneWire library.