from django.db import models

class Basesite(models.Model):
    rs = models.IntegerField()
    addresses = models.TextField()
    num_mnc_digits = models.IntegerField()
    latitude = models.FloatField()
    ul_bandwidth = models.IntegerField()
    ci1 = models.IntegerField()
    mcc = models.IntegerField()
    ci2 = models.CharField(max_length=100)
    deviceId = models.CharField(max_length=128)
    lac = models.IntegerField()
    dl_bandwidth = models.IntegerField()
    freq_band_ind = models.IntegerField()
    creatTime = models.CharField(max_length=64)
    serv_rssnr = models.IntegerField()
    cell_rsrp = models.IntegerField()
    pci = models.IntegerField()
    tac = models.IntegerField()
    cell_rsrq = models.IntegerField()
    id = models.CharField(max_length=128, primary_key=True)
    earfcn = models.IntegerField()
    longitude = models.FloatField()
    serving_cell_id = models.IntegerField()
    mnc = models.IntegerField()
    ch = models.IntegerField()
    cell_pci = models.IntegerField()
    nonce = models.BigIntegerField()
    userId = models.CharField(max_length=128)
    cell_idle_srxlev = models.IntegerField()
    cell_rssi = models.IntegerField()
    reportTime = models.DateTimeField()

    def __str__(self):
        return "%d-%d-%d-%d-%d" % (self.mcc, self.mnc, self.lac, self.ci1, self.rs)


class Celllocation(models.Model):
    mcc = models.IntegerField()
    mnc = models.IntegerField()
    lac = models.IntegerField()
    ci1 = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    coverage = models.TextField(blank=True)

    def __str__(self):
        return "%d-%d-%d-%d: %05f, %05f" % (self.mcc, self.mnc, self.lac, self.ci1, self.latitude, self.longitude)