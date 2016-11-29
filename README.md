# cache_consist
Cache consistence for different functions

Different cache functions are using the same information.

IOT have consistence result. When the root function is changing his information,
force children that inheritance the information to recompute.

Ex:
x = get_testrequest(<id>) # x.status = 'BUSY'  (cache for 10 s)
y = get_result(<id>) # use the above information  (cache for 20 s)
# change status for x to 'DONE'

# after 10 s
x = get_testrequest(<id>) # rerun because cache expired
y = get_result(<id>) # rerun because status had changed (NOTE: cache still exist)

