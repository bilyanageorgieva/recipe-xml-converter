# Recipe XML Converter
- [Recipe XML Converter](#recipe-xml-converter)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Components](#components)
    - [Transformers](#transformers)
    - [Orchestrator](#orchestrator)
    - [User interface](#user-interface)
      - [CLI](#cli)
      - [REST API](#rest-api)
      - [Web](#web)
## Introduction
This application converts [RecipeML](http://www.formatdata.com/recipeml/) files into 
[MyCookbook XML](https://cookmate.blog/my-cookbook-xml-schema/) files and optionally combines multiple
RecipeML files into a single MyCookbook XML. The code is part of the final project of my 
BSc in Computer Science from Goldsmiths University of London. The application is hosted on 
Heroku and you can find it [here](https://recipe-xml-converter.herokuapp.com/).

## Installation
First things first, you need to clone the repository.
```shell
git clone https://github.com/bilyanageorgieva/recipe-xml-converter.git
```
Make sure you install an appropriate Python version. Currently the project runs on Python 
3.10 and higher.
Then to install the project's dependencies you can use poetry or pip. If you have poetry 
installed you simply need to navigate to the project's directory and run 
```shell
poetry install
```
With pip, I would suggest you first create a virtual environment and then inside it run
```shell
pip install -r requirements.txt
```
Once that is completed you are ready to go.

## Components
The project uses XSLT to transform files from RecipeML to MyCookbook XML. In Python, this is
achieved with the help of the lxml library. To achieve the transformations the code is split
into multiple components described in detail below.

### Transformers
The Transformer classes are used to transform an XML file using an sequence of XSLT 
stylesheets. A dedicated Transformer class instance is needed for a single file transformation.
Each Transformer child class is defined by the stylesheets required for its target
transformations, and those are defined as abstract properties in the base class. The only
method the Transformer class exposes externally is `transform_and_save()` that transforms
the input file and saves the result to a predefined target path.

### Orchestrator
The Orchestrator implements the general workflow around the transformation and combining
of multiple files. It is an abstract class and its child classes define the transformer
classes to use for the individual file transformations, and the combining of the already
transformed files. The only method it exposes externally is `orchestrate()` that 
transforms and combines the input files as needed, saves the resulting files to a zip
archive, and finally returns the path to said archive. 

### User interface
Users can transform their RecipeML files in three ways - running the code from the 
command line, through a REST API, or on the web. Each of the options are discussed in detail
below. The REST API and the Web interfaced are developed with FastAPI.

#### CLI
To transform files from the command line, users only need to run a single function. 
Start by installing the project as described above and then run the following command
 in the command line from the project's folder to see the documentation of the CLI.
```shell
python run recipe_xml_converter/cli.py --help
```

#### REST API
You can read the documentation of the REST API [here](https://recipe-xml-converter.herokuapp.com/docs).
Once again it exposes only one function that takes as parameters multiple XML files and 
returns a zipped archive of the files transformed. Once you install the project,
you can also run the REST API locally with the following command
```shell
uvicorn recipe_xml_converter.api:app --reload
```

#### Web
The application is deployed on the web with a simple frontend accessible [here](https://recipe-xml-converter.herokuapp.com/).
Once you run the server as described above you can see the frontend by pointing your 
browser to `localhost:8000`.
