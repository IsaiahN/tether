# Third-party notices

Tether uses data and software from the projects below. Each keeps its own licence. Data files derived from them carry the source, sha256 and licence in their own headers (see `library/`). Pictures from ImageNet, and anything computed from them, are kept locally and are not part of this repository.

## ConceptNet 5

Used in: `library/relations.json` (English edges for CapableOf, ReceivesAction, UsedFor, IsA, HasProperty). That file is licensed under the Creative Commons Attribution-ShareAlike 4.0 license (CC BY-SA 4.0), as ConceptNet requires: ConceptNet data may not be combined into a data set under an incompatible licence or with added restrictions such as "non-commercial" or "research use only".

Credit text, verbatim as ConceptNet asks for it (its page licenses the complete data under CC BY-SA 4.0; the credit text it supplies still names 3.0):

> This work includes data from ConceptNet 5, which was compiled by the Commonsense Computing Initiative. ConceptNet 5 is freely available under the Creative Commons Attribution-ShareAlike license (CC BY SA 3.0) from http://conceptnet.io.
>
> The included data was created by contributors to Commonsense Computing projects, contributors to Wikimedia projects, DBPedia, OpenCyc, Games with a Purpose, Princeton University's WordNet, Francis Bond's Open Multilingual WordNet, and Jim Breen's JMDict.

Citation: Robyn Speer, Joshua Chin, and Catherine Havasi. 2017. "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 31.

## WordNet 3.0

Used in: `library/lexicon_imagenet_wordnet.json`, `library/word_map.json`, `library/vocabulary.json`, `library/rdl_preload.json` (and, through ConceptNet and the zaibacu thesaurus, data derived from WordNet).

> WordNet Release 3.0
>
> This software and database is being provided to you, the LICENSEE, by Princeton University under the following license. By obtaining, using and/or copying this software and database, you agree that you have read, understood, and will comply with these terms and conditions.:
>
> Permission to use, copy, modify and distribute this software and database and its documentation for any purpose and without fee or royalty is hereby granted, provided that you agree to comply with the following copyright notice and statements, including the disclaimer, and that the same appear on ALL copies of the software, database and documentation, including modifications that you make for internal use or for distribution.
>
> WordNet 3.0 Copyright 2006 by Princeton University. All rights reserved.
>
> THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT- ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.
>
> The name of Princeton University or Princeton may not be used in advertising or publicity pertaining to distribution of the software and/or database. Title to copyright in this software, database and any associated documentation shall at all times remain with Princeton University and LICENSEE agrees to preserve same.

## VerbNet 3.x

Used in: `library/vocabulary.json` and `library/relations.json` (verb classes, VerbNet 3.4 from https://github.com/cu-clear/verbnet).

VerbNet (Kipper Schuler; Palmer, Bonial, Hwang et al., University of Colorado Boulder) is provided under the VerbNet 3.0 licence, which also applies to VerbNet 3.X versions (https://verbs.colorado.edu/~mpalmer/projects/verbnet/license.3.0.txt). It grants permission to use, copy, modify and distribute the software and database for any purpose without fee or royalty, provided that its copyright notice and statements, including its disclaimer, appear on all copies, including modifications. The database is provided as is, without representations or warranties of any kind.

## ImageNet (ILSVRC 2012, ImageNet-1k)

Used in: `library/lexicon_imagenet_wordnet.json` (the 1000 class labels and their WordNet ids only). The pictures were obtained through Hugging Face (ILSVRC/imagenet-1k) under the ImageNet Terms of Access: non-commercial research and educational use only; the researcher is responsible for their use; the images belong to their owners, not to ImageNet, Princeton University or Stanford University. The pictures, and any memory computed from them (for example AKAZE descriptor memories), are kept locally and are not distributed with this repository.

Citation: Olga Russakovsky et al. 2015. "ImageNet Large Scale Visual Recognition Challenge." IJCV 115(3).

## AKAZE (and akaze-eigen)

The recognition front end (`recognize.py`, when present) uses the AKAZE feature detector and descriptor through OpenCV. AKAZE is the work of Pablo F. Alcantarilla, Jesús Nuevo and Adrien Bartoli ("Fast Explicit Diffusion for Accelerated Features in Nonlinear Scale Spaces", BMVC 2013). The standalone implementation akaze-eigen (https://github.com/sweeneychris/akaze-eigen) is distributed under this licence, reproduced here as it requires:

> Copyright (c) 2014, Chris Sweeney, Pablo Fernandez Alcantarilla, Jesus Nuevo
> All Rights Reserved
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the copyright holders nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

akaze-eigen is not vendored in this repository today. If it is, its LICENSE file goes with it.

## OpenCV

`recognize.py` uses OpenCV (https://opencv.org) as an installed package (`opencv-python-headless`); OpenCV 4.5 and later are licensed under the Apache License 2.0. OpenCV is not redistributed in this repository.

## zaibacu thesaurus

`en_thesaurus.jsonl` (https://github.com/zaibacu/thesaurus) is extracted from WordNet and carries the WordNet licence above. It is used only as a cross-check and is not included in this repository.
