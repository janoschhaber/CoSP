import os
from nltk.parse import stanford
from nltk.corpus.reader.bnc import BNCCorpusReader


class BNC_Conversation(object):  # xml.etree.ElementTree.Element):
    """
    Class to represent a conversation (transcript, in SWDA jargon) extracted from the BNC-DEM corpus
    """

    def __init__(self, turns, parser):
        """
        Creates a conversation object
        :param turns: list of xml.etree.ElementTree.Element containing the s labels for each utterance as child
        nodes
        :param parser: nltk.parse.stanford.StanfordParser object to produce sentence stanford parses
        """
        self._turns = turns
        self._parser = parser

    def utterances(self):
        """
        Iterator over BNC_Utterance objects, each representing an u element within a conversation (div) element in
        a BNC-DEM xml file
        """
        for turn in self._turns:  # iterate through turns in a conversation
            speaker = turn.get('who')
            for utterance in turn.findall('s'):  # iterate through utterances in a turn
                yield BNC_Utterance(utterance, speaker, self._parser)


class BNC_Utterance(object):
    """
    Class to represent an utterance extracted from the BNC-DEM corpus. It extracts all words (w element)
    in an utterance (s element) and creates a parse tree for it.
    """

    def __init__(self, element, speaker, parser):
        """
        Creates an utterance object
        :param element: xml.etree.ElementTree.Element containing the w labels in an utterance as child nodes
        :param speaker: speaker id
        :param parser: nltk.parse.stanford.StanfordParser object to produce sentence stanford parses
        """
        self.caller = speaker
        self._pos_words = []
        words = [word.text for word in element.findall('w')]
        self.tree = parser.raw_parse(' '.join(words)).next()
        self._pos_words = words

    def pos_words(self):
        return self._pos_words


class BNC_processor(object):
    """
    A basic BNC corpus processor
    """

    def __init__(self, bnc_root="./2554/2554/download/Texts",
                 classpath='stanford-ner-2017-06-09:stanford-parser-full-2017-06-09:stanford-postagger-2017-06-09',
                 standford_parser='stanford-postagger-2017-06-09/models',
                 parser_pcfg='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'):
        """
        Creates a BNC_processor object to read from a XML BNC folder structure, as downloaded from
        http://ota.ox.ac.uk/text/2554.zip
        :param bnc_root: location of the 'Texts' folder with the BNC xml files
        :param classpath: location of the stanford parser, pos tagger and ner jar files
        :param standford_parser: location of the models (.tagger files) of the stanford pos tagger
        :param parser_pcfg: location of the stanford PCFG definition (englishPCFG.ser.gz file)
        """
        # self.bnc_reader = BNCCorpusReader(root=bnc_root, fileids=r'[A-K]/\w*/\w*\.xml')
        self.bnc_reader = BNCCorpusReader(root=bnc_root, fileids=r'K/K[B-S]/\w*\.xml')
        os.environ['CLASSPATH'] = classpath
        os.environ['STANFORD_PARSER'] = standford_parser
        self.parser = stanford.StanfordParser(model_path=parser_pcfg)
        # sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
        # parser.raw_parse('this is a sentence')

    def conversation_iter(self):
        """
        Iterator over BNC_Conversation objects. Yields only conversations from BNC-DEM with exactly 2 participants
        """
        for filename in self.bnc_reader.fileids():
            root = self.bnc_reader.xml(filename)
            text = root.find('stext')
            if text is None: continue  # this means is not even spoken
            if text.get('type') == 'CONVRSN':  # this means BNC-DEM
                for conversation in text.findall('div'):  # div tags contain conversations
                    turns = conversation.findall('u')
                    if len(set([t.get('who') for t in turns])) == 2:  # exactly 2 speakers
                        yield BNC_Conversation(turns, self.parser)  # conversation, like a transcript

if __name__ == '__main__':
    bnc_processor = BNC_processor()
    for transcript in bnc_processor.conversation_iter():
        for utterance in transcript.utterances():
            print('{}: {}\n\t{}'.format(utterance.caller, ' '.join(utterance.pos_words()), utterance.tree))