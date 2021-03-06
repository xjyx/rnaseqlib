##
## Unit testing for gene models and calculation of features of genes
##
import os
import sys
import time

import rnaseqlib
import rnaseqlib.tests
import rnaseqlib.tests.test_utils as test_utils
import rnaseqlib.genes.GeneModel as gene_model
import rnaseqlib.tables as tables


class TestGenes:
    """
    Test features of gene models.
    """
    def __init__(self):
        pass


    def test_const_exons(self):
        """
        Test calculation of constitutive exons
        """
        print "Testing constitutive exons"
        genes_to_test = ["ENSG00000135097", "ENSG00000153944",
                         "ENSG00000242866", "ENSG00000187223",
                         "ENSG00000250590"]
        for gene_id in genes_to_test:
            # Load gene table
            gt = tables.GeneTable(os.path.join(test_utils.TESTDIR, "hg19"), "ensGene")
            ensGene_fname = \
                test_utils.load_test_data(os.path.join("hg19",
                                                       "ensGene.hg19.%s.txt" %(gene_id)))
            # Load ensembl genes table into GeneModel objects
            gt.get_ensGene_by_genes(ensGene_fname)
            print "Loaded genes: "
            for g in gt.genes:
                print g, " => ", gt.genes[g]
            assert gene_id in gt.genes, "Could not load %s" %(gene_id)
            gene = gt.genes[gene_id]
            print "Computing constitutive exons..."
            const_exons = gene.compute_const_exons(base_diff=6, frac_const=0.3)
            print "  - const_exons: ", const_exons
            assert len(const_exons) > 0, "Could not find constitutive exons!"
            print "Computing CDS constitutive exons..."
            cds_const_exons = gene.compute_const_exons(cds_only=True)
            print "CDS-only constitutive exons: "
            print "  - cds_const_exons: ", cds_const_exons


if __name__ == "__main__":
    test_g = TestGenes()
    test_g.test_const_exons()
