from django.db import models


class NNInfo(models.Model):
    nn_id = models.CharField(max_length=10, blank=False, primary_key=True)       # unique key name (nn00000001)
    category = models.CharField(max_length=10, blank=False)                      # business category
    subcate = models.CharField(max_length=10, blank=False)                       # business sub category
    name = models.CharField(max_length=100, blank=True, default='')              # business name
    desc = models.CharField(max_length=5000, blank=True, default='')             # description for network
    type = models.CharField(max_length=100, blank=True, default='')              # network types
    acc = models.CharField(max_length=5, blank=True, default='')                 # accuracy of model from last training
    train = models.CharField(max_length=1, blank=True, default='')               # if trained model exist
    config = models.CharField(max_length=1, blank=True, default='')              # if config exist
    dir = models.CharField(max_length=200, blank=True, default='')               # path where conf files saved
    table = models.CharField(max_length=100, blank=True, default='')             # table name to get data
    query = models.CharField(max_length=5000, blank=True, default='')            # SQL query to get data
    datadesc = models.CharField(max_length=50000, blank=True, default='')        # column data defination
    datasets = models.CharField(max_length=50000, blank=True, default='')        # specific data strucuture
    created = models.DateTimeField(auto_now_add=True)                            # day created

    def json(self):
        return dict(
            nn_id = self.nn_id,
            category=self.category,
            subcate=self.subcate,
            name=self.name,
            desc=self.desc,
            type=self.type,
            acc=self.acc,
            train=self.train,
            config=self.config,
            dir=self.dir,
            table=self.table,
            query=self.query,
            datadesc=self.datadesc,
            datasets=self.datasets
        )

    def __getitem__(self, item):
        return self.__dict__[item]