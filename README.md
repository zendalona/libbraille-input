libbraille-input
======

Braille input engine for IBus-Braille and Sharada-Braille-Writer
This engine can convert braille input events to text and call asociated callback functions. 
Here braille input means inputing text in Perkins-like way, i.e. braille patterns. 
It supports several braille tables, contracted braille and abbreviations.

Features
======

1. Works with two back translation engines (Liblouis, Built-in).
2. Support Grade-1 and Grade-2 braille input for many languages.
3. Supports Nemeth-code for Mathmatic Braille.
4. functions for setting user abbreviations.
5. functions for setting line limiting and auto newline.
6. functions for setting auto capitalization.
7. functions for toggle between Braille input and system default input.

Installing
======
Dependency list : python3, python3-speechd, espeak, python3-enchant

git clone https://github.com/zendalona/libbraille-input.git

cd libbraille

./configure --prefix=/usr
make
make install

Links
======

Home Page : https://github.com/zendalona/libbraille-input
Sharada-Braille-Writer : https://zendalona.com/sbw/

Disclaimer
======
    
    This project is funded by State Council of Educational Research and Training (S.C.E.R.T) Kerala 
    Developed by Zendalona(2021-2022) and Keltron(2012-2014)

    All rights reserved . Redistribution and use in source and binary forms, with or without modification,
    
    are permitted provided that the following conditions are met: 

    Redistributions of source code must retain the below copyright notice, 

    this list of conditions and the following disclaimer. 

    Redistributions in binary form must reproduce the below copyright notice, 

    this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 

    Neither the name of the nor the Lios team names of its 

    contributors may be used to endorse or promote products derived from this software without specific prior written permission. 

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
    OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE." 

FREE SOFTWARE FREE SOCIETY

 
