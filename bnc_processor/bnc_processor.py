import nltk
from nltk.corpus.reader.bnc import BNCCorpusReader
from jpype import *
import pandas as pd


class BNC_Conversation(object):  # xml.etree.ElementTree.Element):
    """
    Class to represent a conversation (transcript, in SWDA jargon) extracted from the BNC-DEM corpus
    """

    def __init__(self, turns, filename, parser, nlp, tagger, reader):
        """
        Creates a conversation object
        :param turns: list of xml.etree.ElementTree.Element containing the s labels for each utterance as child
        nodes
        :param parser: nltk.parse.stanford.StanfordParser object to produce sentence stanford parses
        """
        self._turns = turns
        self.filename = filename
        self._parser = parser
        self._nlp = nlp
        self._tagger = tagger
        self._reader = reader

    def utterances(self):
        """
        Iterator over BNC_Utterance objects, each representing an u element within a conversation (div) element in
        a BNC-DEM xml file
        """
        for turn in self._turns:  # iterate through turns in a conversation
            speaker = turn.get('who')
            for utterance in turn.findall('s'):  # iterate through utterances in a turn
                yield BNC_Utterance(utterance, speaker, self._parser, self._nlp, self._tagger, self._reader)


class BNC_Utterance(object):
    """
    Class to represent an utterance extracted from the BNC-DEM corpus. It extracts all words (w element)
    in an utterance (s element) and creates a parse tree for it.
    """

    def __init__(self, element, speaker, parser, nlp, tagger, reader):
        """
        Creates an utterance object
        :param element: xml.etree.ElementTree.Element containing the w labels in an utterance as child nodes
        :param speaker: speaker id
        :param parser: nltk.parse.stanford.StanfordParser object to produce sentence stanford parses
        """
        self.caller = speaker
        self._pos_words = []
        words = [word.text for word in element.findall('w')]

        WhitespaceTokenizer = nlp.process.WhitespaceTokenizer
        tokenizerFactory = WhitespaceTokenizer.newCoreLabelTokenizerFactory()
        text = tokenizerFactory.getTokenizer(reader(' '.join(words))).tokenize()
        tagged_ut = tagger.tagSentence(text)
        # parse the tagged utterance
        parsed_ut = parser.parse(tagged_ut).toString()
        #print('utterance: {}\ntype: {}'.format(parsed_ut, type(parsed_ut)))
        try:
            self.tree = nltk.tree.Tree.fromstring(str(parsed_ut))
        except ValueError:
            self.tree = None
        self._pos_words = words

    def pos_words(self):
        return self._pos_words


class BNC_processor(object):
    """
    A basic BNC corpus processor
    """

    def __init__(self, bnc_root="./2554/2554/download/Texts",
                 stanford_parser='stanford-parser-full-2017-06-09/stanford-parser.jar',
                 tagger_path='edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger',
                 standford_parser_models='stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'):
        """
        Creates a BNC_processor object to read from a XML BNC folder structure, as downloaded from
        http://ota.ox.ac.uk/text/2554.zip
        :param bnc_root: location of the 'Texts' folder with the BNC xml files
        :param stanford_parser: location of the stanford parser jar
        :param tagger_path: location of the model (.tagger) file
        :param stanford_parser_models: location of the stanford models jar
        """
        # self.bnc_reader = BNCCorpusReader(root=bnc_root, fileids=r'[A-K]/\w*/\w*\.xml')
        self.bnc_reader = BNCCorpusReader(root=bnc_root, fileids=r'K/K[B-S]/\w*\.xml')

        startJVM(getDefaultJVMPath(),
                 "-ea",
                 "-mx2048m",
                 "-Djava.class.path={}".format(stanford_parser + ':' +
                                               standford_parser_models))
        # import all needed Java classes
        self.nlp = JPackage("edu").stanford.nlp
        self.reader = java.io.StringReader
        WhitespaceTokenizer = self.nlp.process.WhitespaceTokenizer
        self.tokenizerFactory = WhitespaceTokenizer.newCoreLabelTokenizerFactory()
        # intialize tagger
        self.tagger = self.nlp.tagger.maxent.MaxentTagger(tagger_path)
        # load the parser
        self.parser = self.nlp.parser.lexparser.LexicalizedParser.loadModel()

    def conversation_iter(self, display_progress=True):
        """
        Iterator over BNC_Conversation objects. Yields only conversations from BNC-DEM with exactly 2 participants
        """
        total = len(self.bnc_reader.fileids())
        for i, filename in enumerate(self.bnc_reader.fileids()):
            if display_progress: print('\rfile {}/{}({:.2%})'.format(i, total, i/total)),
            root = self.bnc_reader.xml(filename)
            text = root.find('stext')
            if text is None: continue  # this means is not even spoken
            if text.get('type') == 'CONVRSN':  # this means BNC-DEM
                for conversation in text.findall('div'):  # div tags contain conversations
                    turns = conversation.findall('u')
                    if len(set([t.get('who') for t in turns])) == 2:  # exactly 2 speakers
                        yield BNC_Conversation(turns, filename, self.parser, self.nlp, self.tagger, self.reader)  # conversation, like a transcript

def process():
    bnc_processor = BNC_processor()
    for transcript in bnc_processor.conversation_iter():
        for utterance in transcript.utterances():
            print('{}: {}\n\t{}'.format(utterance.caller, ' '.join(utterance.pos_words()), utterance.tree))


if __name__ == '__main__':
    process()
    #stanford_parse()