# The Pico Portfolio

This project is an attempt to create a maker-friendly keyboard using the same form factor as the original Atari Portfolio keyboard. 

What started out as an attempt to re-use broken atari portfolio keyboards in new/modern projects hit a wall when tryign to remove the keyboard from its original housing. The housing on the actual Atari Portfolio is very custom for the device and case, and doesn't lend itself well to re-modeling, due to the makeup of the matrix, individual keys and rubber membrane. 

There are files here (in original-portfolio-files) that can be used to turn a *real* atari portfolio keyboard into a USB device with a Raspberry Pi Pico, however, the aim of this repo is to simply create a new, custom board that requires no legacy hardware, is maker friendly, and can be customised with only a 3D printer and some circuitpython.

## Why the portfolio?

Because of its form factor, it is somewhere between the very popular 'blackberry' style handheld keyboard, and the smallest ortholiniar keyboards used in maker projects like cyberdecks. This gives a full keyboard with modifier keys, sacrificing 'touch typing' ability for ease of use by someone who is not an expert in multi-layer keyboard setups. 

Also, John Connor hacked an ATM with one in T2 and I have been in love with them ever since. 

## Why the pico? 

Basically, I had a few picow's lying around and I know the device well. It has lots of GPIO pins and pads under the USB port that make it very easy to solder wires to use as a neat form factor for this sort of thing. 

## Why circuitpython

I plan to add a QMK version to this in the future, and I don't think it would be too hard, but when writing my original version of the firmware for the *real* Portfolio keyboard I ended up using CircuitPython because I knew/understood it well, and was able to make progress. My initial attempts at QMK for that build failed, so I've just stuck with it as it makes debugging super easy. I personally prefer it to MicroPython, but if anyone wants to translate it, please be my guest.

However, now that I know the exact matrix setup, I think QMK would be pretty easy to add to this as an option as well. 

# Setup
You will need to flash a Pico with CircuitPython 9.X (at the time of writing I am using 9.2.7 for the PicoW) - once that is done, connect it to your computer and drop all the files/folders in the `device` folder onto the device. That should load up everything required.

Then it is a matter of printing the STLs in the `3d-models -> stls -> buttons` folder or creating your own. I have included backups of my Fusion360 project in `3d-models -> fusion` should anyone wish to modify things and export their own. I will also include models for the circuitboard with switches and pico in place hopefully will help people wanting to make their own.