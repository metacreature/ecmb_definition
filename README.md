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
Its basically a Zip-file containing a XML-file named "ecmb.xml" for the meta-data and all the images stored in a folder "content", organized in subfolders for using chapters. The cover-images are stored in the root of the Zip-file.
Beside the meta-data, the "ecmb.xml" contains the spine and of course a navigation which gives you many opportunities.
### File-structure:
```
myfile.ecmb
    ˪ ecmb.xml
    ˪ cover.jpeg
    ˪ content/
        ˪ chapter1/
            ˪ page1.jpeg
            ˪ page2.jpeg
```
### ecmb.xml
All rules and requirements for "ecmb.xml" are defined in the XSD ([located here >](https://github.com/metacreature/ecmb_definition/tree/master/schema)), but unfortunately not everything:

***The navigation-links to the contents are relative!*** An example says more than 1000 words ... [go to example >](https://github.com/metacreature/ecmb_definition/blob/master/examples/v1.0/advanced_book/advanced_book.ecmb_unpacked/ecmb.xml)
To clarify that more: a chapter links to a folder, that the reader-app can display which chapter you are currently reading. Of course you want to click on the chapter and the reader-app and therefore you have to provide a link to an image (href) which has to be part of the chapter. To enforce this the link to the image is relative to the chapter's folder. Btw. you can link to the 2nd image (or any you want as long its part of the chapter's folder), if eg. the first one is a spacer-image. Sub-chapters and items are also relative to its parent.

I know its a bit complicated, but its a no-go to mix content with navigation and the programs which should build the eBook would have massive problems, if you want to place links to highlights before the content is added.
Unfortunately I couldn't find a possibility tho validate that directly with XSD. If you have an idea blease post ite here: [https://stackoverflow.com/questions/77667931/cross-validation-of-contents-in-an-xml-using-xsd](https://stackoverflow.com/questions/77667931/cross-validation-of-contents-in-an-xml-using-xsd)

If you link to a double-page-image you have to address the src-attribute, and have to specify either #auto, #left or #right while its forbidden to do so if you link to a single-page-image
