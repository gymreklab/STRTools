import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..','strtools'))

import utils

# ValidateAlleleFreqs
def test_ValidateAlleleFreqs():
    afreqs = {0:1}
    assert(utils.ValidateAlleleFreqs(afreqs))
    afreqs = {0:0.5, 1:0.5}
    assert(utils.ValidateAlleleFreqs(afreqs))
    afreqs = {}
    assert(not utils.ValidateAlleleFreqs(afreqs))
    afreqs = {0:0.5}
    assert(not utils.ValidateAlleleFreqs(afreqs))
    afreqs = {-1: 1, 1: 1}
    assert(not utils.ValidateAlleleFreqs(afreqs))

# GetHeterozygosity
def test_GetHeterozygosity():
    afreqs = {0:1}
    assert(utils.GetHeterozygosity(afreqs)==0)
    afreqs = {0:0.5, 1:0.5}
    assert(utils.GetHeterozygosity(afreqs)==0.5)
    afreqs = {0:0.5, 1:0.2, 2:0.3}
    assert(utils.GetHeterozygosity(afreqs)==0.62)
    afreqs = {}
    assert(np.isnan(utils.GetHeterozygosity(afreqs)))

# GetHardyWeinbergBinomialTest
def test_GetHardyWeinbergBinomialTest():
    # Try examples that should work
    afreqs = {0:0.5, 1:0.2, 2:0.3}
    gcounts = {(0, 1): 10, (0,0): 20, (1,2):5}
    assert(round(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts), 2)==0.02)
    gcounts = {(0,0):20}
    assert(round(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts), 2)==0.0)
    gcounts = {(0,1):20}
    assert(round(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts), 2)==0.0)
    # Try with genotypes whose alleles not in afreqs
    gcounts = {(3,3): 6}
    assert(np.isnan(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts)))
    gcounts = {(0,3): 6}
    assert(np.isnan(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts)))
    # Try invalid afreqs
    afreqs = {}
    assert(np.isnan(utils.GetHardyWeinbergBinomialTest(afreqs, gcounts)))

# GetHomopolymerRun
def test_GetHomopolymerRun():
    assert(utils.GetHomopolymerRun("AATAAAAAAAAT")==8)
    assert(utils.GetHomopolymerRun("AATAAAAAAT")==6)
    assert(utils.GetHomopolymerRun("AATAAAAAAAATTTTTTTTT")==9)
    assert(utils.GetHomopolymerRun("AATAAAAAAAAGGGGGGGGGGTTTTTTTTT")==10)
    assert(utils.GetHomopolymerRun("")==0)

# GetCanonicalMotif
def test_GetCanonicalMotif():
    assert(utils.GetCanonicalMotif("AGC")=="AGC")
    assert(utils.GetCanonicalMotif("CAG")=="AGC")
    assert(utils.GetCanonicalMotif("TG")=="AC")
    assert(utils.GetCanonicalMotif("AT")=="AT")
    assert(utils.GetCanonicalMotif("T")=="A")
    assert(utils.GetCanonicalMotif("TTGTT")=="AAAAC")
    assert(utils.GetCanonicalMotif("")=="")
    assert(utils.GetCanonicalMotif("cag")=="AGC")

# GetCanonicalOneStrand
def test_GetCanonicalOneStrand():
    assert(utils.GetCanonicalOneStrand("AGC")=="AGC")
    assert(utils.GetCanonicalOneStrand("CAG")=="AGC")
    assert(utils.GetCanonicalOneStrand("TG")=="GT")
    assert(utils.GetCanonicalOneStrand("AT")=="AT")
    assert(utils.GetCanonicalOneStrand("T")=="T")
    assert(utils.GetCanonicalOneStrand("TTGTT")=="GTTTT")
    assert(utils.GetCanonicalOneStrand("")=="")
    assert(utils.GetCanonicalOneStrand("at")=="AT")

def test_ReverseComplement():
    assert(utils.ReverseComplement("CGAT")=="ATCG")
    assert(utils.ReverseComplement("")=="")
    assert(utils.ReverseComplement("CGNT")=="ANCG")
    assert(utils.ReverseComplement("ccga")=="TCGG")
