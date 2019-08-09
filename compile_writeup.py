# load all numbers to plug
import json, glob


results = {}
for fname in glob.glob('*.json'):
    addl_results = json.load(open(fname))
    assert set(addl_results.keys()) & set(results.keys()) == set(), 'There should be no duplicate keys'
    results.update(addl_results)


# load the template text
text = ''
for fname in ['intro.md', 'methods.md',
              'results.md', 'discussion.md',
              'acknowledgements.md', 'references.md',]:
    with open(fname) as f:
        text_f = f.read()

        # HACK: latex and python f string markup collide, so keep all
        # the latex in methods.md, and keep all the f-string
        # substitution out of it
        if fname != 'methods.md':
            # plug in the numbers
            pass #text_f = text_f.format(**results)

        text += text_f



# create word doc with pandoc
with open('plugged_text.md', 'w') as f:
    f.write(text)

#!pandoc plugged_text.md -o dp_2020_census.docx
# TODO: include references, like JJ did in previous paper
# bib file like this: https://stash.ihme.washington.edu/projects/VA/repos/insilicova/browse/paper/references.bib
# then include references like this:  [@phillips2015crvs] 
# you need a citation style file like this: https://stash.ihme.washington.edu/projects/VA/repos/insilicova/browse/paper/citation-style-springer-vancouver-brackets.csl

# then we can do something like this:
#pandoc --filter pandoc-citeproc --bibliography=$(PAPER_REFS) \
#       --csl $(CITATION_STYLE) $(PAPER_MD) $(PAPER_METADATA) -o $(PAPER_DRAFTS)/$@
