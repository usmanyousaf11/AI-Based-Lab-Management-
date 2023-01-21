from django.db import models
#import ncbi


class Clone(models.Model):
    """
    Represents DNA for a clone identified by a unique name and living in a
    cellular environment like a bacterium or yeast.
    """
    name = models.CharField(max_length=100)
    accessions = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_accessions(self):
        if not self.accessions:
            #self.accessions = u"".join(ncbi.search_clone_by_name(self.name))
            #self.save()
            self.accessions = []

        return self.accessions


class SequencedClone(models.Model):
    """
    Represents a sequenced clone from NCBI's CloneDB reports.
    """
    gi = models.IntegerField(blank=True, null=True)
    clonename = models.CharField(max_length=100, db_index=True)
    stdn = models.CharField(max_length=1)
    chrom = models.CharField(max_length=5)
    phase = models.IntegerField(blank=True, null=True)
    clonestate = models.CharField(max_length=5)
    gcenter = models.CharField(max_length=100)
    accession = models.CharField(max_length=20, db_index=True)
    seqlen = models.IntegerField(blank=True, null=True)
    libabbr = models.CharField(max_length=10, db_index=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.clonename, self.accession)
