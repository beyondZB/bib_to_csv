from pybtex.database.input import bibtex
import string

# open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file("My Collection.bib")

# tralsator for removing punctuation
translator = str.maketrans('', '', string.punctuation)

# open our output file
f = open('mybibs_new.csv', 'w')

# header row
f.write("Type, Journal/Conference, Year, Authors, Title \n")

# loop through the individual references
for bib_id in bibdata.entries:
    b = bibdata.entries[bib_id].fields
    try:
        # Type
        f.write('"' + bibdata.entries[bib_id].type + '"')
        print(bib_id + " " + bibdata.entries[bib_id].type)

        # Journal/Conference
        f.write(" ,")
        if bibdata.entries[bib_id].type == "article":
            f.write('"' + b["journal"] + '"')
        else:
            f.write('"' + b["booktitle"] + '"')

        # Year
        f.write(" ,")
        f.write(b["year"])
        f.write(" ,")

        # deal with multiple authors
        authors = ""
        for author in bibdata.entries[bib_id].persons["author"]:
            new_author = str(author.first()) + " " + str(author.last())
            new_author = new_author.translate(translator)
            new_author = new_author.replace('{', '')
            new_author = new_author.replace('}', '')
            if len(authors) == 0:
                authors = '"' + new_author
            else:
                authors = authors + ", " + new_author
        f.write(authors + '"')

        # Title
        f.write(" ,")
        title = b["title"]
        title = title.replace('{', '')
        title = title.replace('}', '')
        f.write('"' + title + '"')

    # field may not exist for a reference
    except(KeyError):
        print(bib_id + " error")
        f.write(b["booktitle"])
        f.write("\n")
        continue
    f.write("\n")

# close output file
f.close()
