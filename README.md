# *.ecmb - The new Comic-Manga-eBook
**Benefits:**
- right to left reading in page-mode for mangas, while scroll-mode is still top-down
- advanced support for double-pages
- content-warnings for using safe-guard
- a bunch of possible meta-data like genres and even the homepage of the publisher ([go to example >](https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/example_full.xml))
- support for sub-chapters and many possibilities for navigation with headlines and page-links ([go to example >](https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/advanced_book/advanced_book.ecmb_unpacked/ecmb.xml))
- validateable via XSD
- published under [MIT License](https://choosealicense.com/licenses/mit/)

## The project ([https://metacreature.github.io/](https://metacreature.github.io/))
**It contains:**
- [definition](https://github.com/metacreature/ecmb_definition) of the file-format and a file-validator
- a [library](https://github.com/metacreature/ecmblib_python) for packing the eBooks
- a [builder](https://github.com/metacreature/ecmb_builder) for building the eBooks from your source-images
- a mobile-app for reading the eBooks is under developement

## About this repository:
**This is the definition of the file-format!**
It also contains a validator done in python for validating *.ecmb - files

## Definition:
Its basically a Zip-file containing a XML-file named "ecmb.xml" for the meta-data and all the images stored in a folder "contents", organized in subfolders.
# File-structure:
```
myfile.ecmb
    ˪ ecmb.xml
    ˪ cover.jpeg
    ˪ contents/
        ˪ chapter1/
            ˪ page1.jpeg
            ˪ page2.jpeg
```
All rules and requirements for "ecmb.xml" are defined in the XSD ([located here >](https://github.com/metacreature/ecmb_definition/tree/master/schema), but unfortunately not everything:
The Navigation-links to the contents are relative!
