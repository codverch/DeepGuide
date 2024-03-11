#!bin/bash

git clone https://github.com/google/HyperCompressBench.git # Clone the HyperCompressBench repository
cd HyperCompressBench # Change to the HyperCompressBench directory
cd source_data # Change to the source_data directory
mkdir Calgary # Create a directory named Calgary
cd Calgary # Change to the Calgary directory
wget http://corpus.canterbury.ac.nz/resources/calgary.tar.gz # Download the calgary.tar.gz file
tar -xvzf calgary.tar.gz # Unzip the calgary.tar.gz file
cd .. # Change to the source_data directory
mkdir Canterbury
cd Canterbury # Change to the Canterbury directory
wget http://corpus.canterbury.ac.nz/resources/cantrbry.tar.gz # Download the artificl.tar.gz file
tar -xvzf cantrbry.tar.gz # Unzip the artificl.tar.gz file
cd .. # Change to the source_data directory
mkmdir Silesia # Create a directory named Silesia
cd Silesia # Change to the Silesia directory
wget https://sun.aei.polsl.pl//~sdeor/corpus/dickens.bz2
bzip2 -d dickens.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/mozilla.bz2
bzip2 -d mozilla.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/mr.bz2
bzip2 -d mr.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/nci.bz2
bzip2 -d nci.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/ooffice.bz2
bzip2 -d ooffice.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/osdb.bz2
bzip2 -d osdb.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/reymont.bz2
bzip2 -d reymont.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/samba.bz2
bzip2 -d samba.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/sao.bz2
bzip2 -d sao.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/webster.bz2
bzip2 -d webster.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/xml.bz2
bzip2 -d xml.bz2
wget https://sun.aei.polsl.pl//~sdeor/corpus/x-ray.bz2
bzip2 -d x-ray.bz2
cd .. # Change to the source_data directory
mkdir Snappy # Create a directory named Snappy
cd Snappy # Change to the Snappy directory
git clone https://github.com/google/snappy.git
cp -r snappy/testdata/* . # Move the contents of the testdata directory to the current directory
cd ../.. # Change to the home directory (HyperCompressBench)
python3 reconstruct.py # To produce the HyperCompressBench benchmarks
  
