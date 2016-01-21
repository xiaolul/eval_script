import warnings, sys, collections
import run_tpl as runtpl


class Run:
    """class of run in qres"""

    def __init__(self, fname):
        self.res_set = collections.defaultdict(list)
        self._load_file(fname)

    def _load_file(self, fname):
        f = open(fname, 'r')
        for line in f:
            curr_tpl = runtpl.RunTpl(line)
            self.res_set[curr_tpl.qid].append(curr_tpl)
        f.close()

    def _check_score_tie(self):
        dup_dict = collections.defaultdict(list)
        for k in self.res_set.keys():
            prev_score = sys.maxint
            for tpl in self.res_set[k]:
                if prev_score == sys.maxint:
                    prev_score = tpl.score
                else:
                    if tpl.score == prev_score:
                        dup_dict[k].append(tpl)
                    prev_score = tpl.score
        self.score_tie = dup_dict

    def _check_rank_order(self):
        abnormal_rank = collections.defaultdict(list)
        for k in self.res_set.keys():
            prev_rank = -1
            for tpl in self.res_set[k]:
                if prev_rank == -1:
                    prev_rank = tpl.rank
                else:
                    if int(tpl.rank) - int(prev_rank) != 1:
                        abnormal_rank[k].append(tpl)
                    prev_rank = tpl.rank
        self.abnormal_rank = abnormal_rank

    def get_score_tie_info(self):
        self._check_score_tie()
        if len(self.score_tie) == 0:
            print "No ties on score are found \n"
        else:
            # print "Scores are tied \n"
            for k in self.score_tie.keys():
                 print str(k)+"\n"
                # for tie_tpl in self.score_tie[k]:


    def get_rank_order(self):
        self._check_rank_order()
        if len(self.abnormal_rank) == 0:
            print "Rank orders are correct \n"
        else:
            for k in self.abnormal_rank.keys():
                print str(k) + "\n"
            #     for tpl in self.abnormal_rank[k]:
            #         print str(k) + " " + tpl.get_str() + "\t"


if __name__ == "__main__":
    # use command line as input
    fname = sys.argv[1]
    curr_run = Run(fname)
    print "Checking ties in score"
    curr_run.get_score_tie_info()
    print  "Checking rank orders"
    curr_run.get_rank_order()
