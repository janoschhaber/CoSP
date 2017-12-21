from bnc_processor import BNC_processor
import numpy as np
import pickle
import time

COLLECTOR_VERBOSE = False


class UtteranceWrapper:
    def __init__(self, speaker, text, length, depth, width):
        self.speaker = speaker
        self.text = text
        self.length = length
        self.depth = depth
        self.width = width
        self.ntd = None
        self.ntw = None

    def set_ntd(self, ntd_const):
        self.ntd = self.depth / float(ntd_const)

    def set_ntw(self, ntw_const):
        self.ntw = self.width / float(ntw_const)

    def get_all_measures(self):
        return [self.length, self.depth, self.width, self.ntd, self.ntw]

    def get_array(self):
        return np.asarray(self.get_all_measures())

def collect_transcript_data():
    """
    Collects a list of lists that cotains the utterance wrappers for all transcripts in the SWDA time dataset
    :return: a list of lists that cotains the utterance wrappers for all transcripts in the SWDA time dataset
    """
    transcripts_list = []
    corpus = BNC_processor()
    counter = 0
    start = time.clock()
    for transcript in corpus.conversation_iter(display_progress=True):
        conversation_list = []
        for utterance in transcript.utterances():

            #         sub_utterance = utterance.subutterance_index
            #         print(sub_utterance)

            speaker = utterance.caller
            if COLLECTOR_VERBOSE: print(speaker)
            text = utterance.pos_words()
            if COLLECTOR_VERBOSE: print(text)
            if utterance.tree:
                # TODO: Currently only considering the first tree # # # # # # # # #
                tree = utterance.tree
            else:
                # TODO: Handle cases where no tree is found # # # # # # # # # # # #

                # print("WARNING: Utterance {} has no tree!".format(utterance.pos_words()))
                # This only prints full stops
                continue

            if COLLECTOR_VERBOSE: tree.pretty_print()
            subtrees = tree.subtrees()

            # Collect syntactic complexity metrics
            # Sentence length
            sentence_length = len(text)
            if COLLECTOR_VERBOSE: print(sentence_length)

            # Tree depth
            tree_depth = tree.height()
            if COLLECTOR_VERBOSE: print(tree_depth)

            node_count = 0
            branching_sum = 0
            # Branching factor
            for t in subtrees:
                if COLLECTOR_VERBOSE: print(t)
                num_children = len(t.leaves())
                if COLLECTOR_VERBOSE: print(num_children)
                node_count += 1
                branching_sum += num_children

            tree_width = branching_sum / float(node_count)
            if COLLECTOR_VERBOSE: print(tree_width)

            #         pos = utterance.pos_lemmas()
            #         print(pos)

            wrapper = UtteranceWrapper(speaker, text, sentence_length, tree_depth, tree_width)
            conversation_list.append(wrapper)
        counter += 1
        transcripts_list.append(conversation_list)
        if counter % 30 == 0:  # every 30 out of 234 files...
            with open('transcript_list.pickle', 'wb') as save_file:
                pickle.dump((counter, transcripts_list), save_file)
            print('saved at iteration {}, file {}, at {:.2f} minutes runtime'.format(
                counter, transcript.filename, (time.clock() - start)/60.0
            ))

    return transcripts_list


if __name__ == '__main__':
    transcripts_list = collect_transcript_data()