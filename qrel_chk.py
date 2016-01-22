from qres_chk import Qres,ResTpl
import sys
from collections import defaultdict


class QrelTpl:
    """
    Class of qrel tuple. An example of Qrel tuple should be
    301 0 FBIS3-10082 1
    The qrel information are not allowed to be modified.
    """

    def __init__(self, qrel_str):
        """
        init a qrel tuple, split the input string by any white space
        :param qrel_str:
        :return:
        """
        qrel_arr = qrel_str.strip().split()
        if len(qrel_arr) < 4:
            print >> sys.stderr, 'From QrelTuple: Error in format'
        self._qid = qrel_arr[0]
        self._doc = qrel_arr[2]
        self._rel = qrel_arr[3]

    def get_qid(self):
        """
        get qid.
        :return:qid
        """
        return int(self._qid)

    def get_doc(self):
        """
        get document id
        :return:
        """
        return self._doc

    def get_rel(self):
        return self._rel

    def get_str(self):
        return (self._qid + " 0 " + self._doc + " " + self._rel).strip()


class Qrel:
    """
    Read the Qrel from file and form qrel instance
    """

    def __init__(self, fname):
        self._judged = defaultdict(set)
        with open(fname, "r") as fin:
            for line in fin:
                if len(line.strip()) > 1:
                    tpl = QrelTpl(line)
                    self._judged[tpl.get_qid()].add(tpl.get_doc())
        fin.close()

    def get_judged_by_qid(self, qid):
        return self._judged[qid]



def condense_run(qrel,run):
    id_list = run.get_qid_set()
    for id in id_list:
        curr_run = run.get_res_by_id(id)
        curr_qrel = qrel.get_judged_by_qid(id)
        for res_tpl in curr_run:
            if res_tpl.get_doc() in curr_qrel:
                print res_tpl.get_str()


if __name__ == "__main__":
    # use command line as input
    run_name = sys.argv[1]
    rel_name = sys.argv[2]
    run = Qres(run_name)
    qrel = Qrel(rel_name)
    condense_run(qrel,run)