from pathlib import Path

from lxml import etree as ET


def main():
    dom = ET.parse(Path(__file__).parent.parent / "data/'9os_Style_Chicken_Salad.xml")
    xslt = ET.parse(Path(__file__).parent.parent / "data/recipe.xsl")
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)
    print(ET.tostring(new_dom, pretty_print=True))

    with open(Path(__file__).parent.parent / "data/tranformed.xml", "wb") as file:
        file.write(ET.tostring(new_dom, pretty_print=True))


if __name__ == '__main__':
    main()
