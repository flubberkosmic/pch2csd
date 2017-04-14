# pch2csd

The Clavia Nord Modular G2 Patch Convertor Project

## History

We started our project during Summer of 2015. The Project's main objective is to
simulate legendary Clavia Nord Modular G2 synthesizer using Csound language. The
Project was first presented at the The Third International Csound Conference
(2-4 October, St. Petersburg, Russia).

## Why do you need it?

If you are a Nord Modular fan, this software allows you to have your favourite
device ressurected for internal life in the halls of Csound language. You also
can improve the precision of models and use the whole world of Csound
possibilities together with Clavia.

If you are a Csound person, this is a new branch of our journey. This is great
to have some hardware digital synths running on Csound. Once the conversion
project is done, you are able to use hundreds of interesting Clavia's G2 patches
straigth on Csound.

If you discover the world of modular synthesis and algorithmic composition, the
system provides a good way to describe the graphic patches of Clavia.

If you are a developer of alternative Clavia Nord Modular G2 Editor, you could
merge your graphical editor software with the system to produce the sound.

## Implementation

The main idea behind the implementation of a converter is to model all the
modules of Clavia with Csound UDOs. See `Modules` for modules description based
on Csound language. Please notice that models can contain a lot of errors and
typos. Right now we are working at the core part of the code and do not pay a
lot of attention to models accuracy. The module numbers correspond to original
Clavia module IDs. For the IDs table see `ModIDNames.xls`.

The output of our converter is csd file with all used UDO's and two separate
instruments (instr 1 is the VA part and instr 2 is the FX part).

If some module exists in the patch, we have to insert the corresponding Csound
UDO to the output csd file. Please notice that all UDOs have only inputs. They
are patched to each other not directly, but through the zak-space (see Csound
manual on zak-space for more details). It allows us to maintain the orbitrary
order of modules, where Csound typicaly reads the code from top to bottom.

Another remarkable issue is cabling, which is completely different to Csound.

Check `Tables` directory to see mapping for module parameter values. Being MIDI
compatible, Clavia stores all parameters as an 7 bit integers. So it is not
possible to know the real value of Hz or dB. For this purpose we manually
created the mapping tables looking at values at software editor. For the
reference see `clavia_maps.xls`.

`IO` directory contains module input/output tables. The order of inputs/outputs
is strictly fixed.

Several Clavia modules are polymorphous and can run at a-/k-rates depending on
cabling. I.e. any of mixing modules can mix a-rate signals or can mix k-rate
signals (when working in k-rate mode). For such modules see `seludoM` directory
instead of `Modules`.

Check the Status List to find which modules are implemented and which are the
next to-dos by group.   By now the top priorities are oscillators, filters and
envelope generators. Any help is very welcome.

# UDO examples

This is an example of UDO model for Out2 module. Check Csound manual for details
on Csound programming.

```csound-orc
opcode Out2, 0, iiiii                   ; a new UDO definition. 0 - no outputs,;
                                        ; iiiii - five inputs/parameters of i-type

    isource, iMute, iPad, iL, iR xin    ; getting parameter values from the code
                                        ; isource - source selector
                                        ; iMute - mute toggle
                                        ; iPad - padding button
                                        ; iL,iR - numbers of patch cables for the module
                                        
    aL zar iL                           ; Patching iL cable to audio part of zak space
    aR zar iR                           ; Patching iR cable to audio part of zak space
    
    outs aL, aR                         ; output sound
endop                                   ; end of UDO definition
```

## How to start contribute to the development?

1. Read Clavia Nord G2 manual to get familiar with Clavia's modules.

2. Grab your Clavia Nord Modular G2 or Clavia Nord Modular G2 Engine and wipe
off the dust from it (or install a free Clavia Nord Modular G2 Demo, that should
fully work on XP and partly on Win7, there is also OS X version available).

3. Open a patch you would like to convert, or simple make a new one.

4. Use pch2csd utility.

5. Check the consistency of your patch (all modules, maps etc shoudl be present
in a status table).

6. Run your csd with Csound.

If some modules were not converted into Csound UDO's, it means you need to add
them to `Modules` directory. You also need to create input-output routing table
for those modules and place it in`IO` In case there is some parameter error, you
need to add a new mapping table and place it in `Maps`.

## IO Table Syntax

Refer to `Status List.pdf` to discover which modules are already implemented. More
detailed description will appear soon.

## Known Issues

04/02/2017 Gleb - Clavia's ClkGen can be switched into Master Clock Source mode.
In that mode it accepts realtime MIDI start and stop messages. This feature is
not supported by Csound.

## Authors

The project is developed by Gleb G. Rogozinsky (Csound models) and Michael
Chesnokov (core C/C++ coding). Beginning from January 2017 Eugene Cherny joined
the development. Gleb's email: gleb.rogozinsky@gmail.com

## Credits

The credits go to Michael Dewberry for very useful info on pch2 format structure
http://www.dewb.org/g2/pch2format.html and Iain McCurdy for his bright and
revolutionary ideas on some models.
